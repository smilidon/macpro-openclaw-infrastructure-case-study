#!/usr/bin/env python3
"""OpenAI-compatible image endpoint for OpenClaw's LiteLLM image provider (http://localhost:4000).

Two kinds of models:
  * local-flux-klein-4b  -> stable-diffusion.cpp on the two FirePro D700s (free, offline, default).
                            Supports /v1/images/generations and /v1/images/edits (reference-image edit).
  * flux-*, lucid-origin, phoenix-1.0 -> Cloudflare Workers AI (generation only), used to refine.

Listens on 127.0.0.1 only. Reads CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID from ~/.openclaw/.env.
Set up 2026-11-21. Run as a user service. Originally named cf-image-shim on the source host.

Local notes (Thumbo, GCN1 Tahiti cards):
  * flash attention MUST be on for the diffusion model: without it, anything above 256x256 is grey noise.
  * kernel param amdgpu.lockup_timeout=60000 is required, or long GPU jobs hang the machine.
  * the local chat model (llama-router :8081) is unloaded first so the image model fits in VRAM.
  * all local GPU media jobs (this service and ~/.local/bin/local-video) share one flock.
"""
import base64, fcntl, json, os, re, subprocess, tempfile, uuid, urllib.request, urllib.error
from email.parser import BytesParser
from email.policy import HTTP
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ENV = os.path.expanduser("~/.openclaw/.env")
MODELS = {  # OpenAI-style name -> (Workers AI model, input style)
    "flux-1-schnell": ("@cf/black-forest-labs/flux-1-schnell", "json"),
    "flux-2-dev": ("@cf/black-forest-labs/flux-2-dev", "multipart"),
    "flux-2-klein-4b": ("@cf/black-forest-labs/flux-2-klein-4b", "multipart"),
    "flux-2-klein-9b": ("@cf/black-forest-labs/flux-2-klein-9b", "multipart"),
    "lucid-origin": ("@cf/leonardo/lucid-origin", "json"),
    "phoenix-1.0": ("@cf/leonardo/phoenix-1.0", "json"),
}
LOCAL = {"local-flux-klein-4b"}
DEFAULT = "local-flux-klein-4b"

HOME = os.path.expanduser("~")
SD_CLI = f"{HOME}/stable-diffusion.cpp/build/bin/sd-cli"
SD_DIR = f"{HOME}/models/sd"
GPU_LOCK = f"{HOME}/models/.gpu-media.lock"
ROUTER = "http://127.0.0.1:8082"  # router directly, not the GPU gate (we already hold the lock)
LOCAL_MAX_SIDE = 640   # 512 takes ~105 s; bigger gets slow fast on these cards
LOCAL_TIMEOUT = 900


def env():
    vals = {}
    for line in open(ENV):
        m = re.match(r"^([A-Z0-9_]+)=(.*)$", line.strip())
        if m:
            vals[m.group(1)] = m.group(2).strip().strip("'\"")
    return vals


def parse_size(size, default=(1024, 1024)):
    m = re.match(r"^(\d+)x(\d+)$", str(size or ""))
    return (int(m.group(1)), int(m.group(2))) if m else default


def local_size(w, h):
    s = min(1.0, LOCAL_MAX_SIDE / max(w, h))
    return max(256, int(w * s) // 64 * 64), max(256, int(h * s) // 64 * 64)


def free_gpu_from_router():
    """Unload chat models from llama-router so the image model fits. Embeddings run on CPU and stay."""
    try:
        with urllib.request.urlopen(ROUTER + "/v1/models", timeout=10) as r:
            models = json.load(r)["data"]
    except Exception:  # noqa: BLE001 - router down is fine, GPUs are free then
        return
    for m in models:
        if m["id"] not in ("embed", "lfm3-1.7b", "lfm3-utility") and m.get("status", {}).get("value") == "loaded":
            req = urllib.request.Request(ROUTER + "/models/unload", json.dumps({"model": m["id"]}).encode(),
                                         {"Content-Type": "application/json"})
            try:
                urllib.request.urlopen(req, timeout=30).read()
            except Exception:  # noqa: BLE001
                pass


def run_local(prompt, w, h, refs=()):
    w, h = local_size(w, h)
    with tempfile.TemporaryDirectory(prefix="local-img-") as tmp, open(GPU_LOCK, "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        free_gpu_from_router()
        out = os.path.join(tmp, "out.png")
        cmd = [SD_CLI, "--diffusion-model", f"{SD_DIR}/flux-2-klein-4b-Q4_0.gguf",
               "--vae", f"{SD_DIR}/full_encoder_small_decoder.safetensors",
               "--llm", f"{SD_DIR}/Qwen3-4B-Q4_K_M.gguf",
               "-p", prompt, "--cfg-scale", "1.0", "--sampling-method", "euler", "--steps", "4",
               "-W", str(w), "-H", str(h), "--seed", "-1",
               "--backend", "diffusion=vulkan1,te=vulkan0,vae=vulkan0",
               "--params-backend", "diffusion=vulkan1,te=vulkan0,vae=vulkan0",
               "--flash-attn", "off,diffusion=on", "-o", out]
        for i, data in enumerate(refs):
            p = os.path.join(tmp, f"ref{i}.png")
            open(p, "wb").write(data)
            cmd += ["-r", p]
        r = subprocess.run(cmd, cwd=SD_DIR, capture_output=True, text=True, timeout=LOCAL_TIMEOUT)
        if r.returncode != 0 or not os.path.exists(out):
            errs = [l for l in (r.stdout + r.stderr).splitlines() if "[E]" in l][-3:]
            raise RuntimeError("local generation failed: " + " | ".join(errs)[:300])
        return base64.b64encode(open(out, "rb").read()).decode()


def run_cloudflare(cf_model, style, prompt, width, height, steps):
    e = env()
    url = f"https://api.cloudflare.com/client/v4/accounts/{e['CLOUDFLARE_ACCOUNT_ID']}/ai/run/{cf_model}"
    fields = {"prompt": prompt}
    if "flux-1-schnell" not in cf_model:  # schnell is fixed-size and rejects width/height
        fields.update(width=str(width), height=str(height))
    if steps:
        fields["steps"] = str(steps)
    headers = {"Authorization": "Bearer " + e["CLOUDFLARE_API_TOKEN"]}
    if style == "multipart":
        b = uuid.uuid4().hex
        body = b"".join(
            f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode() for k, v in fields.items()
        ) + f"--{b}--\r\n".encode()
        headers["Content-Type"] = f"multipart/form-data; boundary={b}"
    else:
        body = json.dumps({k: (int(v) if v.isdigit() else v) for k, v in fields.items()}).encode()
        headers["Content-Type"] = "application/json"
    with urllib.request.urlopen(urllib.request.Request(url, body, headers), timeout=170) as r:
        data, ctype = r.read(), r.headers.get("Content-Type", "")
    if ctype.startswith("image/"):
        return base64.b64encode(data).decode()
    j = json.loads(data)
    img = (j.get("result") or {}).get("image") if isinstance(j.get("result"), dict) else None
    if not img:
        raise RuntimeError(f"no image in response: {str(j)[:300]}")
    return img


def parse_multipart(ctype, body):
    """Return (fields, files) from a multipart/form-data body."""
    msg = BytesParser(policy=HTTP).parsebytes(b"Content-Type: " + ctype.encode() + b"\r\n\r\n" + body)
    fields, files = {}, []
    for part in msg.iter_parts():
        name = part.get_param("name", header="content-disposition")
        data = part.get_payload(decode=True) or b""
        if part.get_filename() or (name or "").startswith("image"):
            if data:
                files.append(data)
        elif name:
            fields[name] = data.decode(errors="replace")
    return fields, files


class H(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if self.path.rstrip("/") in ("/v1/models", "/models"):
            data = [{"id": k, "object": "model", "owned_by": "thumbo-local"} for k in sorted(LOCAL)]
            data += [{"id": k, "object": "model", "owned_by": "cloudflare-workers-ai"} for k in MODELS]
            return self._send(200, {"object": "list", "data": data})
        if self.path.rstrip("/") in ("/health", "/healthz", ""):
            return self._send(200, {"status": "ok"})
        self._send(404, {"error": {"message": "not found"}})

    def do_POST(self):
        path = self.path.rstrip("/")
        try:
            body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            ctype = self.headers.get("Content-Type", "")
            if path in ("/v1/images/generations", "/images/generations"):
                req, refs = json.loads(body or b"{}"), []
            elif path in ("/v1/images/edits", "/images/edits"):
                if ctype.startswith("multipart/"):
                    req, refs = parse_multipart(ctype, body)
                else:
                    req = json.loads(body or b"{}")
                    refs = [base64.b64decode(i.split(",")[-1]) for i in req.get("images") or [req.get("image")] if i]
                if not refs:
                    return self._send(400, {"error": {"message": "edit needs at least one image"}})
            else:
                return self._send(404, {"error": {"message": "only /v1/images/generations and /v1/images/edits"}})

            name = (req.get("model") or DEFAULT).split("/")[-1]
            w, h = parse_size(req.get("size"))
            n = max(1, min(int(req.get("n") or 1), 4))
            prompt = req.get("prompt", "")
            if name in LOCAL:
                imgs = [run_local(prompt, w, h, refs) for _ in range(n)]
            elif name in MODELS:
                if refs:
                    return self._send(400, {"error": {"message": f"{name} cannot edit images; use local-flux-klein-4b"}})
                cf_model, style = MODELS[name]
                imgs = [run_cloudflare(cf_model, style, prompt, w, h, req.get("steps")) for _ in range(n)]
            else:
                return self._send(400, {"error": {"message": f"unknown model {name}; available: {sorted(LOCAL) + list(MODELS)}"}})
            self._send(200, {"created": 0, "data": [{"b64_json": i} for i in imgs]})
        except urllib.error.HTTPError as e:
            self._send(502, {"error": {"message": f"Cloudflare HTTP {e.code}: {e.read()[:300].decode(errors='replace')}"}})
        except subprocess.TimeoutExpired:
            self._send(504, {"error": {"message": "local generation timed out"}})
        except Exception as e:  # noqa: BLE001
            self._send(500, {"error": {"message": str(e)[:300]}})

    def log_message(self, fmt, *args):
        print("%s %s" % (self.address_string(), fmt % args), flush=True)


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", 4000), H).serve_forever()
