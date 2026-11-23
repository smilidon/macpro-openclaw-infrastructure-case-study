# Local Last-Resort Fallback and Local Media — 2026-11-21

**Status:** operator-requested change, measured on the host. Partial: the
results below are what was observed on this date, not a qualification suite.

## Why the routing boundary changed

Until this date the public posture was that local generation is never an
automatic fallback (see [Known Issues](../docs/known-issues.md)). The operator
asked for the opposite guarantee: the agents must keep working, slowly if
necessary, when free and paid hosted quotas are exhausted or the host loses
internet entirely. The boundary was moved only after three hardware-risk
mitigations were in place and observed working (below).

## Incident that preceded the change

A local image-generation test at 512×512 on one D700 exceeded the GPU driver's
default 10-second graphics-ring timeout. The driver reset the card twice; the
second reset left the device wedged, and because the local chat runtime also
held both cards, the host locked up and needed a forced reboot.

## Mitigations

| Mitigation | Effect | Observation |
| --- | --- | --- |
| Driver lockup timeout raised from 10 s to 60 s (kernel parameter, reboot) | Long single GPU jobs are no longer treated as hangs | 512×512 and video jobs of 94–850 s completed with zero ring timeouts or resets |
| One shared GPU lock for every GPU workload | Image jobs, video jobs and GPU chat models never hold the cards at the same time | A chat request sent while the lock was held was served by the CPU model instead of loading a GPU model |
| CPU-only last-resort text model | Fallback needs no GPU at all | Answers while media jobs hold both cards |

The lock is a single file lock: media jobs take it exclusively for the whole
job; GPU chat requests hold it shared while their response streams. A small
local gate in front of the model router applies it, because the router cannot.
Text-only GPU chat requests that arrive during a media job are rerouted to the
CPU model; requests that carry an image wait, because only the GPU vision model
can read images. Embeddings run on the CPU and are never gated.

## Local models after cleanup

| Role | Model | Placement | Measured speed |
| --- | --- | --- | --- |
| Last-resort text, tools | LFM3 1.7B Q4_K_M | CPU only, always loaded | ~25 tok/s generation, ~74 tok/s prompt |
| Vision, general | Gemma 4 E4B Q4_K_M + projector | Both D700s | ~5.9 tok/s generation |
| Larger text | Qwen3.5 9B Q4_K_M | Both D700s, on demand | ~4.2 tok/s generation |
| Memory embeddings | EmbeddingGemma 300M Q8_0 | CPU only | — |

Nine unused local models (including the earlier safety-tuned 4B offline model
and `thumbo-safe`) and four unused benchmark model files were removed, freeing
about 40 GB.

Every text agent's fallback chain now ends with the CPU model and then the
larger GPU text model (the GPU vision model failed tool use, so it is kept only
for image input); the vision agent ends with the GPU vision model; the offline
agent uses the CPU model first (it outperformed the larger GPU text model on
exact file lookups, below). Speech got its own local fallbacks (next section).

## Local speech fallback

Both run on the CPU, so they never contend for the GPU lock.

- Transcription order: hosted Groq Whisper → hosted Mistral Voxtral (free tier)
  → local whisper.cpp `small.en` through a CLI wrapper. Through OpenClaw with
  the hosted entries removed, the local entry returned an exact transcript of a
  5-second Ogg/Opus clip (44 s wall time, mostly CLI start-up).
- Speech output: the hosted Google TTS stays first; a local Piper voice was
  added through OpenClaw's local-CLI speech provider. Through OpenClaw it
  synthesized a sentence in 1.4 s, and the local transcriber read it back word
  for word.
- CPU timings for an 11-second sample: `base.en` 1.9 s, `small.en` 6.2 s,
  `large-v3-turbo` (q5_0) 30.7 s.

## Memory search

Memory search was configured for an embedding model that was not installed, so
semantic recall could not work. It was repointed at the local CPU embedding
model and all 25 agent indexes were rebuilt (1,215 files, about 28 minutes on
CPU). The first rebuild failed because the embedding server's batch limit
(256 tokens) was smaller than OpenClaw's memory chunks (up to ~480 tokens); the
batch limit was raised for the CPU embedding model only. A post-rebuild search
returned relevant ranked results.

## Local image generation

FLUX.2 Klein 4B (Q4_0) via stable-diffusion.cpp on Vulkan, diffusion on one
card, text encoder and decoder on the other, 4 steps.

| Size | Default attention | Flash attention (diffusion only) |
| --- | --- | --- |
| 256×256 | correct image, 42–44 s | — |
| 384×384 | uniform grey noise (pixel std-dev ≈ 11) | correct image, 71 s |
| 512×512 | uniform grey noise (std-dev ≈ 6), with or without VAE tiling, on either card | correct image, 103 s |
| 640×448 via the image API | — | correct image, 113 s |

Root finding: on these GCN1 cards the default attention path silently produces
noise above 256×256; no error is reported. Flash attention for the diffusion
model is therefore mandatory on this host.

Local generation is now the default image route, exposed through the existing
OpenAI-compatible local image endpoint; hosted image models are fallbacks, and
agents are expected to use hosted vision and image models to check and refine
rather than to generate first. Local reference-image editing uses the same
model.

## Local video generation

Wan 2.1 text-to-video 1.3B (fp16) with a Q4_K_M UMT5-XXL encoder. 416×240,
17 frames (~1 s), 20 steps, flash attention: completed in ~14 minutes with a
coherent clip; the full VAE decoder ran out of VRAM once and recovered by
temporal tiling, so the lightweight TAEHV decoder is used afterwards. The 5B and
14B variants do not fit in 6 GB per card. OpenClaw has no local video provider
for this stack, so video is a local command that shares the GPU lock.

## Real OpenClaw tests on local models

| Test | Model | Result |
| --- | --- | --- |
| Offline agent reads a file with its read tool and answers | LFM3 1.7B | Pass: correct, 126 s, cost 0 |
| Same agent, 4-part question about the same file | LFM3 1.7B | Read the file; 2/4 correct (exact value and count right, two judgment answers wrong); 225 s |
| Same 4-part question | Gemma 4 E4B | Fail twice: did not call the read tool and invented all four answers; 70 s and 64 s |
| Same 4-part question | Qwen3.5 9B | First blocked by a wrong "no tool support" model entry; after the fix, read the file and got 2/4 correct; 213 s |
| Tool-call format check | LFM3 1.7B | Pass: well-formed function call |
| Exact value lookup in a file, GPUs idle | LFM3 1.7B / Qwen3.5 9B | LFM3 correct; Qwen wrong (2 of 2 runs) |
| Text request during an image job | gate | Rerouted to LFM3; no GPU reset |
| `openclaw infer image generate` | FLUX.2 Klein 4B local | 640×640 in 170 s |
| Local video command | Wan 2.1 1.3B | 1-second clip in ~12 min |
| Local speech output, then local transcription of it | Piper / whisper small.en | Pass, word-for-word |
| Retest: one-number lookup that requires the read tool | Gemma 4 E4B | Fail twice: answered "2" (correct: 417) with 2 output tokens and no tool call; 32 s and 7 s |

## Limits

- Small local models are slow and noticeably less reliable than hosted models;
  the fallback is availability insurance, not a quality claim.
- The CPU model has a 32K context and no vision.
- A long media job delays vision requests that need the GPU model.
- These are single observations on one host, not a repeated qualification.
