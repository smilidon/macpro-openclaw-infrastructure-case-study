# Reference files

Sanitized copies of the working configuration from the
[D700 local AI guide](../docs/d700-local-ai-guide.md). Adjust paths, ports and
model file names for your own host before use. Ports used here: model router
8082 behind the GPU gate on 8081; local image endpoint 4000 (all loopback only).

| File | What it is |
| --- | --- |
| `models-preset.ini` | llama.cpp router preset: LFM3 1.7B (CPU), Gemma 4 E4B + projector and Qwen3.5 9B (both GPUs), EmbeddingGemma (CPU) |
| `llama-gpu-gate.py` | Small proxy in front of the router that shares one GPU lock with image/video jobs and reroutes text to the CPU model while the GPUs are busy |
| `local-image-endpoint.py` | OpenAI-compatible `/v1/images/generations` and `/v1/images/edits` endpoint running FLUX.2 Klein 4B locally (flash attention on), with optional hosted Cloudflare Workers AI models; credentials are read from a local environment file, never stored here |
| `local-video.sh` | Wan 2.1 1.3B text-to-video wrapper that takes the same GPU lock |
| `local-stt.sh` | CPU whisper.cpp transcription wrapper (ffmpeg converts voice notes first); used as an OpenClaw CLI audio model |
| `rerank-proxy.py` | Fixed-sigmoid `/rerank` proxy so a llama.cpp reranker can be OpenClaw's decision model |
| `searxng.container` | Rootless Podman quadlet running SearXNG on 127.0.0.1:8888 only, image pinned by digest, all capabilities dropped |
| `searxng-settings.example.yml` | SearXNG settings: JSON output on (OpenClaw's `searxng` provider needs it), limiter off for loopback-only use, short engine timeouts, engines enabled explicitly |
| `local-tts.sh` | CPU Piper speech wrapper; used as OpenClaw's `tts-local-cli` provider command |

To enable every engine an image ships (minus inactive ones and ones that need
API keys), list the names from the image's own defaults:

```bash
podman exec searxng /usr/local/searxng/.venv/bin/python -c "import yaml; [print(e['name']) for e in yaml.safe_load(open('/usr/local/searxng/searx/settings.yml'))['engines'] if not e.get('inactive')]"
```

These are provided as-is from one host; they are not a supported product.
