#!/usr/bin/env python3
"""GPU gate in front of the llama.cpp router.

Listens on 127.0.0.1:8081 (what OpenClaw uses) and forwards to the router on 127.0.0.1:8082.

The two FirePro D700s are shared by GPU chat models (gemma-e4b, qwen35-9b-abliterated) and by
local image/video jobs (cf-image-shim local-flux-klein-4b, ~/.local/bin/local-video). They cannot
share VRAM, so everything coordinates through one flock on ~/models/.gpu-media.lock:
  * media jobs take it exclusively (LOCK_EX) for the whole job;
  * GPU chat requests hold it shared (LOCK_SH) while the response streams;
  * if a media job holds the GPUs, text-only GPU chat requests are rerouted to the CPU model
    (lfm3-1.7b) instead of waiting; requests with images wait, since only gemma has vision;
  * CPU models (embed, lfm3-1.7b) and everything else pass straight through.
Set up 2026-11-21. Service: llama-gpu-gate.service (systemd --user).
"""
import fcntl, http.client, json, os, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

UPSTREAM = ("127.0.0.1", 8082)
LOCK = os.path.expanduser("~/models/.gpu-media.lock")
GPU_MODELS = {"gemma-e4b", "qwen35-9b-abliterated"}
CPU_FALLBACK = "lfm3-1.7b"
WAIT_FOR_VISION = 1800  # seconds a vision request may wait for a media job
HOP = {"connection", "keep-alive", "transfer-encoding", "te", "trailer", "upgrade", "proxy-connection", "host", "content-length"}


def has_image(req):
    for m in req.get("messages") or []:
        c = m.get("content")
        if isinstance(c, list) and any(isinstance(p, dict) and p.get("type") in ("image_url", "input_image", "image") for p in c):
            return True
    return False


def acquire_shared(lock_file, block_seconds):
    deadline = time.monotonic() + block_seconds
    while True:
        try:
            fcntl.flock(lock_file, fcntl.LOCK_SH | fcntl.LOCK_NB)
            return True
        except BlockingIOError:
            if time.monotonic() >= deadline:
                return False
            time.sleep(1)


class Gate(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _forward(self, body):
        conn = http.client.HTTPConnection(*UPSTREAM, timeout=3600)
        headers = {k: v for k, v in self.headers.items() if k.lower() not in HOP}
        if body is not None:
            headers["Content-Length"] = str(len(body))
        conn.request(self.command, self.path, body=body, headers=headers)
        r = conn.getresponse()
        self.send_response(r.status, r.reason)
        for k, v in r.getheaders():
            if k.lower() not in HOP:
                self.send_header(k, v)
        self.send_header("Transfer-Encoding", "chunked")
        self.send_header("Connection", "close")
        self.end_headers()
        while True:
            chunk = r.read1(65536)
            if not chunk:
                break
            self.wfile.write(b"%x\r\n%s\r\n" % (len(chunk), chunk))
            self.wfile.flush()
        self.wfile.write(b"0\r\n\r\n")
        self.wfile.flush()
        conn.close()
        self.close_connection = True

    def _handle(self):
        n = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(n) if n else None
        req = None
        if body and "json" in (self.headers.get("Content-Type") or ""):
            try:
                req = json.loads(body)
            except ValueError:
                req = None
        model = (req or {}).get("model") if isinstance(req, dict) else None
        if model not in GPU_MODELS:
            return self._forward(body)
        with open(LOCK, "a") as lock_file:
            vision = has_image(req)
            if acquire_shared(lock_file, WAIT_FOR_VISION if vision else 0):
                return self._forward(body)
            if vision:
                self.send_error(503, "GPUs busy with a long media job; try again later")
                return
            req["model"] = CPU_FALLBACK
            print(f"GPUs busy: rerouting {model} -> {CPU_FALLBACK}", flush=True)
            return self._forward(json.dumps(req).encode())

    def do_GET(self):
        self._forward(None)

    def do_POST(self):
        try:
            self._handle()
        except (BrokenPipeError, ConnectionResetError):
            pass
        except Exception as e:  # noqa: BLE001
            try:
                self.send_error(502, f"gate error: {e}"[:200])
            except Exception:  # noqa: BLE001
                pass

    do_DELETE = do_PUT = do_POST

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", 8081), Gate).serve_forever()
