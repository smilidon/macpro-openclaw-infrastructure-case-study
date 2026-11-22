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
| `local-tts.sh` | CPU Piper speech wrapper; used as OpenClaw's `tts-local-cli` provider command |

These are provided as-is from one host; they are not a supported product.
