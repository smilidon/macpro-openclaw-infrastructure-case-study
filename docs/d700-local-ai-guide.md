# Local AI on a 2013 Mac Pro (FirePro D700 / Tahiti GCN1) — Practical Guide

**Last verified:** 2026-11-21 on Linux 7.2, Mesa 26.2 (RADV, Vulkan 1.3),
llama.cpp build `401563f10` (2026-11-18), stable-diffusion.cpp `532d2c1`
(2026-11-15).

This is what actually works on this hardware, in the order to do it, and the
traps that cost the most time. Measurements behind each step are in the
[local model testing record](../evidence/local-model-testing-record-2026-09-to-11.md)
and the [2026-11-21 evidence record](../evidence/local-fallback-and-media-2026-11-21.md).
Sanitized copies of the helper scripts and the model preset are in
[`reference/`](../reference/README.md).

Applies to: Mac Pro 6,1 with dual FirePro D300/D500/D700 (Tahiti/Pitcairn,
GCN1). Numbers below are for D700 6 GB cards and a 12-core Xeon E5-2697 v2.

## 0. The short version

1. Use Vulkan (RADV). ROCm does not support GCN1, and Ollama's bundled runtime
   did not see the GPUs at all.
2. **Before any long GPU job, raise the GPU driver lockup timeout** or a long
   job can hang the whole machine.
3. Build llama.cpp and stable-diffusion.cpp yourself with Vulkan and native
   CPU flags.
4. Text: split models across both cards; flash attention **off** for chat.
5. Images and video: flash attention **on** for the diffusion model, or you
   get grey noise above 256×256.
6. A 1.7B model on the CPU (LFM3) is faster than any GPU model here; use it as
   the always-available fallback.
7. Put one shared lock around all GPU work; the cards cannot hold a chat model
   and an image model at the same time.

## 1. Kernel: GPU lockup timeout (do this first)

The amdgpu default treats any GPU job running longer than 10 seconds as a hang.
Image diffusion steps on these cards take longer, the driver resets the card,
and a second reset can leave it wedged and freeze the host.

```sh
sudo grubby --update-kernel=ALL --args="amdgpu.lockup_timeout=60000"
# reboot, then confirm:
cat /sys/module/amdgpu/parameters/lockup_timeout   # 60000
```

The cost is that a genuinely stuck GPU takes up to 60 s to recover. Undo with
`--remove-args="amdgpu.lockup_timeout"`. On distributions without `grubby`, add
the parameter to the kernel command line in your bootloader configuration.

## 2. Build the runtimes

The Xeon E5 v2 has AVX and F16C but **no AVX2 or FMA**; `GGML_NATIVE=ON` picks
the right flags. You need `glslc` (shaderc) for the Vulkan shaders.

```sh
# llama.cpp
cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DGGML_NATIVE=ON -DGGML_VULKAN=ON
cmake --build build -j 20

# stable-diffusion.cpp
cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DSD_VULKAN=ON -DGGML_NATIVE=ON
cmake --build build -j 20
```

Check that both cards appear: `llama-server --list-devices` should show
`Vulkan0` and `Vulkan1` (and `vulkaninfo --summary` should list two RADV TAHITI
devices). One of them drives the display and has slightly less free VRAM.

## 3. Text models (llama.cpp router)

Run `llama-server` in router mode with a model preset file so several models
can be loaded and swapped on demand. The preset used here is in
[`reference/models-preset.ini`](../reference/models-preset.ini). Key settings:

| Setting | Value | Why |
| --- | --- | --- |
| Devices | both cards, layer split, even 1:1 | faster than one card for every model tested |
| GPU layers | all | partial CPU offload was much slower |
| Flash attention (chat) | off | equal or faster on GCN1 for text |
| Batch / micro-batch (GPU models) | 512 / 256 | larger chunks caused GPU timeouts before the lockup fix |
| Batch / micro-batch (CPU embedding) | 2048 / 2048 | memory-search chunks are up to ~480 tokens |
| Threads | 24 for CPU-only models | hyper-threads gave +54% prompt and +21% generation speed over 12 |

Recommended models (measured generation speed):

| Model | Where | Speed | Use |
| --- | --- | ---: | --- |
| LFM3 1.7B Q4_K_M | CPU only | 25 tok/s | fallback, tools, offline |
| Gemma 4 E4B Q4_K_M + F16 projector | both GPUs | 5.9 tok/s | images in, vision |
| Qwen3.5 9B Q4_K_M | both GPUs, 64K context | 4.2 tok/s | larger text tasks |
| EmbeddingGemma 300M Q8_0 | CPU only | — | memory search |

Skip Gemma 4 12B (2.4 tok/s), Qwen3 8B (no gain over Qwen3.5 9B), and
Qwen3.5 4B on GPU (slower than LFM3 on CPU).

LFM3 emits a reasoning trace before answering; give it a few hundred output
tokens, or short replies come back empty.

## 4. Images (stable-diffusion.cpp)

Model files: FLUX.2 Klein 4B `Q4_0` GGUF, Qwen3 4B `Q4_K_M` text encoder, and
the FLUX.2 small decoder VAE. Diffusion on one card, text encoder and VAE on the
other:

```sh
sd-cli --diffusion-model flux-2-klein-4b-Q4_0.gguf \
  --vae full_encoder_small_decoder.safetensors --llm Qwen3-4B-Q4_K_M.gguf \
  -p "your prompt" --cfg-scale 1.0 --steps 4 -W 512 -H 512 \
  --backend diffusion=vulkan1,te=vulkan0,vae=vulkan0 \
  --params-backend diffusion=vulkan1,te=vulkan0,vae=vulkan0 \
  --flash-attn off,diffusion=on -o out.png
```

- **`--flash-attn ...diffusion=on` is mandatory above 256×256.** Without it the
  output is uniform grey noise with no error message.
- Times: 256×256 ~43 s, 384×384 71 s, 512×512 ~105 s, 640×448 113 s.
- Editing: add `-r input.png` (reference image) with an edit instruction.
- Unload any GPU chat model first; both do not fit in VRAM together.

## 5. Video (Wan 2.1 1.3B)

Only the 1.3B text-to-video model fits in 6 GB per card. Files: Wan 2.1 T2V
1.3B fp16, `umt5-xxl` encoder `Q4_K_M`, Wan 2.1 VAE, and the TAEHV tiny decoder
(`taew2_1`).

```sh
sd-cli -M vid_gen --diffusion-model wan2.1_t2v_1.3B_fp16.safetensors \
  --vae wan_2.1_vae.safetensors --tae taew2_1.safetensors \
  --t5xxl umt5-xxl-encoder-Q4_K_M.gguf -p "your prompt" \
  --cfg-scale 6.0 --sampling-method euler --flow-shift 3.0 --steps 20 \
  -W 416 -H 240 --video-frames 17 --fps 16 \
  --backend diffusion=vulkan1,te=vulkan0,vae=vulkan0 \
  --params-backend diffusion=vulkan1,te=vulkan0,vae=vulkan0 \
  --flash-attn on -o out.webm
```

Expect ~14 minutes for 17 frames (~1 s). Without the tiny decoder, the full VAE
ran out of VRAM and fell back to slower tiling.

## 6. Sharing the GPUs safely

The cards can hold either a chat model or an image/video model, not both. Use
one file lock for all GPU work:

- image and video jobs take it exclusively for the whole job and unload GPU
  chat models first;
- a small gate in front of the model router holds it shared while a GPU chat
  response streams; if a media job holds it, text-only requests are rerouted to
  the CPU model instead of waiting.

[`reference/llama-gpu-gate.py`](../reference/llama-gpu-gate.py) and
[`reference/local-video.sh`](../reference/local-video.sh) implement this.

## 7. Speech (CPU only)

Speech does not need the GPUs, so it never waits for an image or video job.

| Task | Tool | Model | Measured |
| --- | --- | --- | --- |
| Speech to text | whisper.cpp (CPU build) | `ggml-small.en` | 11 s of audio in 6 s, exact transcript |
| Speech to text (multilingual) | whisper.cpp | `ggml-large-v3-turbo-q5_0` | 11 s of audio in 31 s; too slow as a default |
| Speech to text (fastest) | whisper.cpp | `ggml-base.en` | 11 s in 1.9 s, minor punctuation differences |
| Text to speech | Piper (`pip install piper-tts`) | `en_US-lessac-medium` | 4.8 s of speech in 1.5 s |

Convert input with ffmpeg first (voice notes are usually Ogg/Opus, which
whisper-cli cannot read). Wrappers: [`reference/local-stt.sh`](../reference/local-stt.sh)
and [`reference/local-tts.sh`](../reference/local-tts.sh).

OpenClaw wiring (shape only):

```json5
{
  tools: { media: {
    models: [
      { provider: "groq", model: "whisper-large-v3-turbo", capabilities: ["audio"] },
      { type: "cli", command: "/path/to/local-stt", args: ["{{AttachmentPath}}"],
        timeoutSeconds: 900, capabilities: ["audio"] },
    ],
    audio: { enabled: true },
  } },
  tts: {
    providers: {
      "tts-local-cli": { command: "/path/to/local-tts",
        args: ["{{Text}}", "{{OutputPath}}"], outputFormat: "wav", timeoutMs: 300000 },
    },
    // if a persona uses fallbackPolicy "fail", give it a binding for
    // tts-local-cli too, or the local provider is skipped
  },
}
```

## 8. OpenClaw-specific notes

- Put local models at the **end** of every text agent's fallback chain (CPU
  model first, then a 9B GPU text model) so agents keep working when hosted
  quotas run out or the internet is down.
- Make sure local model entries declare tool support correctly; a wrong
  "no tools" flag blocks every tool-using agent on that model.
- After onboarding with an existing local server, check that your main agent's
  primary model was not switched to the local model.
- Background maintenance can be local: point `utilityModel` at a second,
  thinking-off copy of the CPU model, and memory dreaming at the GPU text model
  (it runs at night). Keep compaction on a large-context model; its setting
  has no fallback chain.
- Decision model: a local cross-encoder reranker works through OpenClaw's
  bundled `rerank` provider. GTE reranker ModernBERT base scored best of four
  on MTEB AskUbuntuDupQuestions here. Put a fixed sigmoid in front of
  llama.cpp's raw scores, and tune any probability threshold for the model.
- Recall-gate threshold: the llama.cpp GTE GGUF scores match the official
  model within 0.015, so OpenClaw's default `highThreshold` 0.75 applies; on
  BEIR SciFact the balanced (best-F1) point was 0.87. Shadow-test before `live`.
- Web search: a self-hosted SearXNG found the SimpleQA answer in its top 10
  for 77% of 150 questions vs 67% for OpenClaw's DuckDuckGo provider, with no
  errors. Enable many engines: the image's two defaults (DuckDuckGo, Google
  CSE) throttle a home IP within about 100 queries.
- Bigger local brain: mixture-of-experts models run on the CPU alone. Qwen3.6
  35B-A3B scored 72.9% on MMLU-Pro (lm-eval, 140 questions) vs 37% for LFM3
  1.7B, at about 9 tok/s and 22 GB RAM. Use 10–16 threads (24 collapses
  generation), and expect slow first turns (20–26 tok/s prompt). Simple BFCL
  tool calls do not need it: LFM3 scores as well there. LFM2.5 24B-A2B is
  faster (15.6 tok/s) but scored 55%; it needs `--reasoning-budget 0`, since
  `--reasoning off` leaves it thinking.
- Small local models do not find tools through Tool Search. Keep the tools
  they need (for example `view_image`) directly visible with
  `tools.toolSearch.exclude`, and raise `tools.media.image.timeoutSeconds` for
  local vision models.
- For memory search, point the embedding provider at the local CPU embedding
  model, then rebuild the index (about 28 minutes for ~1,200 files here).
- The local image endpoint can be OpenAI-compatible (`/v1/images/generations`
  and `/v1/images/edits`) so OpenClaw's LiteLLM image provider can use it; see
  [`reference/local-image-endpoint.py`](../reference/local-image-endpoint.py).

## 9. What did not work

| Attempt | Result |
| --- | --- |
| Ollama's bundled runtime on these GPUs | No Vulkan devices; partial offload slower than CPU |
| Single-card text models | Slower than splitting across both cards |
| KV cache in system RAM | One third slower |
| GPU performance power profile | No change |
| Default attention for image diffusion | Grey noise above 256×256 |
| VAE tiling as a fix for the grey noise | No effect |
| Default 10 s GPU lockup timeout with long jobs | Card resets and a full host freeze |
| Wan 2.2 5B / 14B | Do not fit in 6 GB per card |
| Gemma 4 E4B for tool-driven agent tasks | Skipped the tool and invented answers in four of four tests (two 4-part questions, two one-number lookups); keep it for image input only |
| LFM3 1.7B deciding by itself to delegate to larger local models | Never delegated in four tries; works only through a dedicated tool such as `view_image` |
| Qwen3.5 9B as first local agent model | Bigger, but misreported file values in two of two exact lookups that LFM3 1.7B got right |
