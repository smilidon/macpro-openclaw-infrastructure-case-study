# Local Model Testing Record — September to November 2026

**Purpose:** publish every local-model measurement and finding from this host,
including models that were rejected or removed, so that anyone with the same
hardware can skip the dead ends. For the step-by-step setup that resulted, see
the [D700 local AI guide](../docs/d700-local-ai-guide.md).

**Host:** Mac Pro 6,1 (late 2013), Xeon E5-2697 v2 (12 cores / 24 threads,
Ivy Bridge: AVX and F16C, **no AVX2/FMA**), 64 GB RAM, 2× AMD FirePro D700
6 GB (Tahiti XT, GCN1), Linux 7.2 with Mesa 26.2 RADV (Vulkan 1.3). ROCm does
not support these cards; Vulkan is the only usable GPU path.

All numbers are single observations unless stated otherwise. Speeds are tokens
per second (tok/s); "gen" is generation (decode), "prompt" is prompt processing
(prefill).

## 1. Summary of what to use and what to skip

| Model | Verdict on this hardware | Why |
| --- | --- | --- |
| LFM3 1.7B Q4_K_M (CPU) | **Use** as last-resort / offline text and tools model | 25 gen / 74 prompt tok/s on CPU alone; correct tool calls; needs no GPU |
| Gemma 4 E4B Q4_K_M + projector (2 GPUs) | **Use** for local vision only | Only local model that reads images; ~5.9 gen tok/s; in four agent tests it skipped a required tool call and invented answers |
| Qwen3.5 9B Q4_K_M (2 GPUs) | Keep as second local text model | 4.2 gen tok/s, 64K context across both cards; called its tool but misreported file values in 2 of 2 exact lookups |
| EmbeddingGemma 300M Q8_0 (CPU) | **Use** for memory search | CPU-only; needs a batch size ≥ 512 |
| FLUX.2 Klein 4B Q4_0 (sd.cpp) | **Use** for local images and edits | 512×512 in ~105 s, **only with flash attention** |
| Wan 2.1 T2V 1.3B fp16 (sd.cpp) | Usable for short clips | ~14 min per 1 s of 416×240 video |
| Gemma 4 12B Q4_K_M | Skip | 2.4 gen tok/s across both cards; no gain worth the VRAM |
| Qwen3 8B Q4_K_M | Skip | 4.5–4.8 gen tok/s, no advantage over Qwen3.5 9B |
| Qwen3.5 4B Q4_K_M | Skip (superseded) | 6.4 gen tok/s on 2 GPUs; LFM3 on CPU is faster and better at tools |
| Qwen3.5 4B "offline-safe" (Ollama) | Removed | Ollama's bundled runtime had no Vulkan; CPU 8.1 tok/s; verbose thinking broke exact-answer tasks |
| `thumbo-safe` (custom Ollama model) | Removed | Passed 1/4 strict usefulness gates (see earlier evidence) |
| Wan 2.2 5B / 14B variants | Skip | Do not fit in 6 GB per card |
| whisper.cpp `small.en` (CPU) | **Use** for local transcription | 11 s of audio in 6.2 s, exact transcript |
| whisper.cpp `base.en` (CPU) | Optional faster choice | 11 s in 1.9 s, minor punctuation differences |
| whisper.cpp `large-v3-turbo` q5_0 (CPU) | Skip as default | 11 s in 30.7 s (no AVX2/FMA on this CPU); keep only for non-English |
| GTE reranker ModernBERT base Q8_0 (CPU) | **Use** as local decision model | Best MTEB AskUbuntu MAP of four rerankers tested; 10.7 pairs/s |
| BGE v2-m3 / Jina v2 / Qwen3-Reranker 0.6B | Skip | Slightly lower MAP; BGE 2× and Qwen3 12× slower |
| Piper `en_US-lessac-medium` (CPU) | **Use** for local speech output | 4.8 s of speech in 1.5 s; whisper read it back word for word |

## 2. Ollama baseline (2026-11-17)

Qwen3.5 4B Q4_K_M through Ollama 0.32.5 with its bundled llama.cpp runtime.

| Profile | Gen tok/s | Prompt tok/s | Avg latency | Strict tasks passed |
| --- | ---: | ---: | ---: | ---: |
| CPU only, 8 threads | 8.13 | 11.92 | 19.3 s | 1/4 |
| 8 layers on the display GPU | 5.53 | 16.55 | 26.0 s | 1/4 |

Findings:

- The bundled runtime enumerated no Vulkan devices; only one GPU was usable
  and partial offload was **slower** than CPU for generation.
- Ollama model files do not accept a tensor split, so both cards cannot be
  used together through Ollama on this setup.
- The model's default template forced a visible "thinking" trace, which failed
  exact-match tasks (JSON extraction, arithmetic, redaction). Only the
  free-form question passed.
- **Lesson:** build llama.cpp yourself with Vulkan; do not rely on Ollama's
  bundled runtime for these cards.

## 3. Ollama short-context test (2026-09-11)

Same Qwen3.5 4B model, 4K context, 8 of 33 layers on GPU, deterministic
sampling, thinking disabled.

| Test | Input tokens | Wall time | Exact answer |
| --- | ---: | ---: | --- |
| Cold lookup | 955 | 29.2 s | correct |
| Warm arithmetic | 1,242 | 31.8 s | correct |
| Warm reference lookup | 2,457 | 60.8 s | correct |
| Cold paragraph copy | 1,273 | 42.8 s | correct (35 tokens) |

Prompt processing was ~41 tok/s and generation 5.5–7.8 tok/s. Planning rule
from this run: about `6 s + input_tokens / 40 + output_tokens / 5.4`.
A follow-up long-context run (~17.5K-token inputs at a 32K window) was
cancelled after one case; its short control returned a correctly located value
with an extra prefix, which counts as a format failure. No long-context result
is claimed.

## 4. llama.cpp Vulkan benchmarks (2026-11-20)

Self-built llama.cpp (native CPU flags plus Vulkan), both D700s visible.
Short prompt (11–12 tokens), up to 128 generated tokens. "Dual" means layers
split across both cards; "single" means the non-display card only. No GPU ring
timeouts or resets occurred in any run. GPU edge temperatures stayed at
49–57 °C and CPU package at 52–58 °C.

| Run | Model | Placement | Context | VRAM card A / B (MiB) | Prompt tok/s | Gen tok/s |
| --- | --- | --- | ---: | --- | ---: | ---: |
| A | Qwen3.5 9B | dual | 64K | 4002 / 3007 | 12.4 | 4.2 |
| B | Qwen3.5 9B | single | 16K | 5273 / — | 9.9 | 3.1 |
| C | Qwen3.5 9B, micro-batch 512 | dual | 64K | 4198 / 3239 | 11.9 | 4.2 |
| D | Gemma 4 12B | dual | 64K | 4875 / 3697 | 6.0 | 2.4 |
| E | Qwen3 8B | dual | 32K | 4383 / 3383 | 8.1 | 4.5 |
| F | Qwen3 8B | single | 16K | 5766 / — | 7.2 | 3.4 |
| G | Qwen3 8B, flash attention off | dual | 16K | 4783 / 3784 | 8.4 | 4.8 |
| H | Qwen3.5 9B, flash attention off | dual | 32K | 4446 / 3438 | 12.3 | 4.3 |
| I | Qwen3.5 9B, KV cache in system RAM | dual | 64K | 3142 / 2364 | 9.7 | 2.8 |
| J | Qwen3.5 9B abliterated | dual | 64K | 5060 / 2949 | 12.1 | 4.2 |
| K | Qwen3.5 4B | single | 32K | 3275 / — | 13.5 | 4.9 |
| L | Qwen3.5 4B | dual | 64K | 2574 / 2071 | 16.9 | 6.4 |
| M | Qwen3.5 4B, GPU performance mode | dual | 64K | 2574 / 2076 | 17.0 | 6.4 |
| N | Qwen3.5 9B, GPU performance mode | dual | 64K | 4002 / 2975 | 12.2 | 4.2 |
| O | Gemma 4 E4B abliterated | dual | 64K | 3146 / 2246 | 9.1 | 4.5 |
| P | Gemma 4 E4B abliterated | single | 32K | 3235 / — | 16.3 | 3.5 |
| Q | Gemma 4 E4B, flash attention off | dual | 32K | 3395 / 2492 | 21.0 | 5.5 |
| R | Gemma 4 E4B, flash attention off, even 1:1 split | dual | 32K | 3022 / 2709 | 22.8 | 5.9 |

Findings:

- **Splitting layers across both cards beats one card** for every model
  (for example Qwen3.5 9B 4.2 vs 3.1 tok/s), even though the cards are linked
  over PCIe rather than a fast interconnect.
- For **text chat, flash attention off** was equal or faster (runs G, H, Q, R).
  This is the opposite of the image-model finding below; set it per workload.
- An even 1:1 layer split was the fastest Gemma E4B configuration.
- Keeping the KV cache in system RAM (run I) cost a third of the speed.
- Forcing the GPU performance power profile made no difference (M vs L, N vs A).
- Longer prompts: Qwen3.5 9B processed a 5K-token prompt at ~44 tok/s; Gemma
  E4B processed a 236-token image-plus-text prompt at ~53 tok/s.
- Gemma 4 12B weights alone exceed one card and ran at 2.4 tok/s: not worth it.

## 5. CPU-only small model (2026-11-21)

LFM3 1.7B Q4_K_M with no GPU layers, 12 threads: **74 tok/s prompt,
25 tok/s generation** (512-token prompt, 64 generated, 2 repetitions). It emits
a reasoning trace before its answer (about 70 tokens for a trivial reply), so
give it an output budget of at least a few hundred tokens. It produced a
correctly formed function call on a tool-calling check.

On this CPU a 1.7B model is faster than any GPU model above, and it frees the
GPUs for media work. Developer-published benchmarks (not reproduced here)
list LFM3 1.7B at BFCL v4 71.4 vs Qwen3.5 4B 55.1 and Gemma 4 E4B 48.3, but
behind Qwen on knowledge (GPQA Diamond 63.4 vs 75.8) and long-context recall
(RULER 128K 65.6 vs 84.6). Its licence (LFM Open License v1.0) has a revenue
threshold for commercial use.

## 6. Real agent tests through OpenClaw (2026-11-21)

All on the dedicated offline agent, which has a file-read tool.

| Task | Model | Time | Result |
| --- | --- | ---: | --- |
| Read a config file, list CPU-only sections | LFM3 1.7B | 126 s | Correct; tool used; cost 0 |
| Read the same file, answer 4 questions (photo model, fastest model, largest context and value, count of auto-loaded models) | LFM3 1.7B | 225 s | Read the file; 2/4 correct (exact value and count right; two judgment answers wrong) |
| Same 4 questions | Gemma 4 E4B | 70 s, then 64 s | Fail twice: skipped the read tool and invented all four answers both times |
| Same 4 questions | Qwen3.5 9B | 7 s | Blocked: its model entry declared no tool support (configuration error) |
| Same 4 questions, after fixing the entry | Qwen3.5 9B | 213 s | Read the file; 2/4 correct (fastest model and exact context value right; photo model and count wrong) |
| Read the file, report one exact value, while an image job held the GPUs | LFM3 1.7B then Qwen3.5 9B | 243 s | GPU gate rerouted the first step to LFM3 (tool call); Qwen answered the second step: **wrong** (1000000000 vs 32768) |
| Same exact-value lookup, GPUs idle | Qwen3.5 9B | 51 s | **Wrong** (16384); its read pulled in about half as much file content as LFM3's, so it likely read part of the file and guessed |
| Same exact-value lookup, GPUs idle | LFM3 1.7B | 117 s | Correct (32768), quoted the section |
| Local image via OpenClaw's default image route | FLUX.2 Klein 4B | 170 s | Pass: 640×640, correct subject |
| Local video via the wrapper script | Wan 2.1 1.3B + TAEHV | 735 s | Pass: 17 frames, coherent, little motion; no GPU resets |

Lessons: small local models need tasks grounded in tool output; a model entry
that wrongly declares "no tools" fails before any inference; and Gemma 4 E4B
should not be used for tool-driven agent work here. Resulting routing: the
offline agent uses LFM3, then Qwen3.5 9B, then Gemma (vision), because LFM3 was
the more reliable tool user despite being smaller; every other text
agent falls back to LFM3, then Qwen3.5 9B; Gemma is kept only for image input.

## 7. Image and video models

Details and timings are in the
[2026-11-21 evidence record](local-fallback-and-media-2026-11-21.md). Key
findings for this hardware:

- stable-diffusion.cpp on Vulkan works. FLUX.2 Klein 4B Q4_0 with the
  Qwen3 4B text encoder: 256×256 in ~43 s.
- **Above 256×256 the default attention path silently outputs uniform grey
  noise** on these GCN1 cards, on either card, with or without VAE tiling.
  Enabling flash attention for the diffusion model fixes it (384×384 in 71 s,
  512×512 in 103 s).
- Long single GPU jobs exceed the driver's default 10 s lockup timeout. The
  result was two GPU resets and a full host lock-up. Raise it (60 s worked).
- Wan 2.1 1.3B text-to-video: 416×240, 17 frames, 20 steps took ~14 min; the
  full VAE decoder ran out of VRAM once and recovered by tiling. Use the TAEHV
  tiny decoder.

## 6a. Small CPU model as a dispatcher (2026-11-21)

Can LFM3 1.7B decide on its own to hand work to the larger GPU models through
OpenClaw sub-agents? Mostly no.

| Test | Result |
| --- | --- |
| Small file lookup | Did it itself, correct, 110 s |
| Image question, no image tool visible | Fail: opened the PNG as text, overflowed its 32K context, then looped on invented file paths |
| Image question with OpenClaw's `view_image` tool directly visible | Pass: hosted vision 156 s; local Gemma E4B only, 50 s |
| Told the exact `sessions_spawn` call for Gemma | Spawn and wait worked; the Gemma sub-agent took 9 min and gave a vague, partly wrong description |
| Long writing task that its instructions say to hand to Qwen 9B | Did not delegate |
| "Have your Qwen helper write..." | Did not delegate; wrote it itself |

What works: give the small model a dedicated tool that performs the hand-off
(`view_image`), and keep that tool out of any tool-search indirection; small
models do not use a search step to find tools. Also raise the image-description
timeout (default 60 s) for local vision models.

## 6b. CPU threads (2026-11-21)

LFM3 1.7B Q4_K_M, llama-bench, CPU only, 12-core / 24-thread Xeon E5-2697 v2:

| Threads | Prompt tok/s | Generation tok/s |
| ---: | ---: | ---: |
| 6 | 36.6 | 19.8 |
| 12 | 78.1 | 22.9 |
| 18 | 77.9 | 29.5 |
| 24 | 120.3 | 27.8 |

Hyper-threads help on this CPU, unlike the usual "physical cores only" advice.
Do not run two 24-thread processes at the same time.

## 6c. Local reranker as OpenClaw decision model (2026-11-21)

Standard test: MTEB **AskUbuntuDupQuestions** reranking test split (375
queries, 7,500 candidate pairs; queries without negatives skipped as MTEB
does), scored with MAP and MRR@10.

| Model (Q8_0 GGUF, llama.cpp `--rerank`, CPU, 12 threads) | Queries | MAP | MRR@10 | Pairs/s |
| --- | ---: | ---: | ---: | ---: |
| GTE reranker ModernBERT base (149M) | 361 | **61.78** | **75.37** | 10.7 |
| BGE reranker v2-m3 (568M) | 361 | 60.92 | 74.88 | 5.4 |
| Jina reranker v2 base multilingual (278M) | 361 | 60.74 | 74.58 | 16.4 |
| Qwen3-Reranker 0.6B | first 100 | 60.79 | 73.90 | 1.4 |
| GTE ModernBERT on the same first 100 | 100 | 60.57 | 75.42 | 17.4 |

GTE ModernBERT gave the best ranking quality, is twice as fast as BGE and
about 12 times faster than Qwen3-Reranker on this CPU, and is the model
OpenClaw's own rerank documentation recommends.

End-to-end through OpenClaw's `decision_evaluate` tool, 30 AskUbuntu queries
from the same split, each asked as two boolean questions (one true duplicate,
one non-duplicate):

| Decision model | AUC | Picked the duplicate (of 30 pairs) | Correct at 0.5 | Median call |
| --- | ---: | ---: | ---: | ---: |
| OpenAI `gpt-6-luna` (was configured) | — | — | — | fails: needs an OpenAI Platform key with Decisions access; ChatGPT login is not enough |
| Google `gemini-decision-1` (free key) | 0.81 | 24 | 42/60 | 0.53 s |
| Local GTE ModernBERT reranker | 0.77 | 23 | 30/60 | 0.30 s |

The local reranker ranks almost as well as the hosted decision model, but its
scores are not calibrated: every answer scored 0.78 to 0.92, so a fixed 0.5
threshold is meaningless. Any consumer that thresholds the probability needs a
threshold tuned for this model (OpenClaw's rerank docs say the same).
llama.cpp returns raw logits for GTE, BGE and Jina; OpenClaw rejects scores
outside 0–1, so a small fixed-sigmoid proxy sits in front
([`reference/rerank-proxy.py`](../reference/rerank-proxy.py)).

### 6c-i. Tuning the reranker threshold (2026-11-22)

First check: do the llama.cpp GGUF scores match the official model? Six
query/passage pairs scored by the pinned Hugging Face release
(`f7481e6055501a30fb19d090657df9ec1f79ab2c`, transformers, sigmoid of the logit)
and by the local Q8_0 GGUF behind the sigmoid proxy differed by at most 0.015.
So OpenClaw's recall-gate default `highThreshold` 0.75, which its docs say
was measured with this exact model, carries over unchanged.

Second check, a standard set shaped like the Knowledge recall gate: BEIR
**SciFact** test split (300 queries, 5,183 abstracts). For each query, BM25
keyword top 10 (the gate's default shortlist), abstracts cut to 1,000
characters (the gate's excerpt size), scored by the local reranker; 3,000
pairs, 245 relevant. Threshold picked on a random half of the queries,
reported on the other half:

| `highThreshold` | Precision | Recall | F1 | Pages injected (held-out half) |
| ---: | ---: | ---: | ---: | ---: |
| 0.50 | 0.10 | 1.00 | 0.17 | 1,266 |
| 0.75 (OpenClaw default) | 0.23 | 0.95 | 0.38 | 492 |
| 0.80 | 0.35 | 0.88 | 0.50 | 302 |
| 0.85 | 0.56 | 0.78 | 0.65 | 167 |
| **0.87 (best F1 on the tuning half)** | **0.64** | **0.70** | **0.67** | 133 |
| 0.90 | 0.78 | 0.47 | 0.59 | 73 |

Reading: 0.75 favours recall (almost every relevant page gets through, with
many irrelevant ones); 0.87 is the balanced point on SciFact. SciFact is
scientific abstracts, not personal notes, so treat 0.87 as a data point: run
the gate in `shadow` mode and check its logged scores before going `live`.
The threshold only matters when the Knowledge plugin is the selected memory
provider (`plugins.slots.memory`); on this host `memory-core` holds that slot,
so the gate is off.

## 6d. Local search engine: SearXNG vs DuckDuckGo (2026-11-22)

Third-party search benchmarks do not settle a "best" engine: AIMultiple's
agentic search benchmark ranks Brave first, OpenBenchmarks puts Exa first on
single-query accuracy and Perplexity first on multi-hop research, and two other
public comparisons come from search-API vendors. None of them tested SearXNG.
The leaders are paid APIs, so the free, self-hosted SearXNG metasearch was
tested here against the current OpenClaw provider (DuckDuckGo).

Standard set: OpenAI **SimpleQA** test set (simple-evals), 150 questions drawn
with a fixed seed. Metric: the gold answer (normalised text match) appears in
the titles and snippets of the top 10 results. This measures retrieval only,
not a model's final answer. DuckDuckGo was called through OpenClaw's own
`web_search` tool; SearXNG through its JSON API, which is what OpenClaw's
`searxng` provider calls.

| Search | Answer in top 10 | Answer in top 3 | Errors | Median time |
| --- | ---: | ---: | ---: | ---: |
| DuckDuckGo via OpenClaw `web_search` | 101/150 (67%) | 82 | 9 provider errors | 1.0 s |
| SearXNG, image defaults, run at the same time | 51/150 | 41 | 74 empty result lists | 0.3 s |
| SearXNG, 5 engines (Brave, Bing, Startpage, Yahoo, Wikipedia + defaults), run alone | **116/150 (77%)** | 81 | 0 | 0.8 s |

What went wrong in the second row: this SearXNG image enables only DuckDuckGo
and Google CSE for general search. With both tools hitting DuckDuckGo from one
home IP, DuckDuckGo started returning CAPTCHAs and Google CSE answered
"unusual traffic" after about 100 queries, so SearXNG returned nothing.
Spreading queries across more engines fixed it.

Final setup: every engine the image ships enabled (263), except engines marked
inactive in that build and ten that need API keys. Engines that block
automated traffic are suspended by SearXNG and skipped. Not re-benchmarked;
spot checks took 2.8–6.0 s (the slowest engines run up to the 6 s
`max_request_timeout`) and returned 110–158 merged results from 13–19 engines.
Config: [`reference/searxng.container`](../reference/searxng.container) and
[`reference/searxng-settings.example.yml`](../reference/searxng-settings.example.yml).

OpenClaw switch (`tools.web.search.provider: "searxng"` plus
`plugins.entries.searxng.config.webSearch.baseUrl`) is left to the agent
itself on this host. An explicitly selected provider has no automatic
fallback, so keep DuckDuckGo as the manual fallback; it is also one of
SearXNG's engines.

## 6e. Larger mixture-of-experts models on CPU (2026-11-22)

Can a bigger local model run here as a "think harder" option? Mixture-of-experts
(MoE) models only use 2–4 B parameters per token, so they fit in the 62 GB of
RAM and run on the CPU alone. All tests used standard open-source tools, not
custom test sets:

- **Speed:** `llama-bench` (llama.cpp build 12499), prompt 512 / generate 64
  tokens, CPU only (`-ngl 0 -dev none`).
- **Tool calls:** the official `bfcl-eval` package (BFCL v4), categories
  `simple_python` and `multiple`, the same 50 + 50 question ids for every
  model (fixed seed), native function calling through llama-server's
  OpenAI-compatible API (`--jinja`), temperature 0, scored with
  `bfcl evaluate --partial-eval`.
- **Knowledge and reasoning:** EleutherAI `lm-evaluation-harness` 0.4.13,
  task `mmlu_pro` (5-shot chain of thought, the task default), 10 questions
  per subject (140), `local-chat-completions`, temperature 0, 1,024 new tokens.

Server settings: 12 threads, 16k context, thinking off (`--reasoning off`;
LFM2.5: `--reasoning-budget 0`; gpt-oss: `--reasoning-effort low`). Q4_K_M
files unless noted.

`--reasoning off` does not stop LFM2.5 24B-A2B from thinking. Its first
MMLU-Pro run spent the full 1,024-token budget on hidden reasoning and
returned an empty answer for 88 of 140 questions (scored 32%). With
`--reasoning-budget 0` it answers directly; the table shows that rerun.
Check for empty `content` before trusting a low score.

| Model | Active / total params | RAM | Generate tok/s (best threads) | Prompt tok/s | BFCL simple | BFCL multiple | MMLU-Pro strict | MMLU-Pro format-tolerant |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Qwen3.6 35B-A3B** (UD-Q4_K_M) | 3B / 35B | 22.2 GB | 9.1 (16) | 20–26 | 46/50 | 42/50 | **72.9%** | **72.9%** |
| LFM2.5 24B-A2B | 2B / 24B | 14.7 GB | **15.6** (10) | **34–39** | **49/50** | 46/50 | 55.0% | 56.4% |
| gpt-oss 20B (MXFP4) | 3.6B / 21B | 12.4 GB | 12.2 (12) | 22–36 | 45/50 | 42/50 | 50.7% | 61.4% |
| Gemma 4 26B-A4B (QAT Q4_0) | 4B / 26B | — | 9.4 (16) | 15–26 | — | — | — | — |
| LFM3 1.7B (current CPU fallback, dense) | 1.7B | 1.4 GB | 25 | 74 | 45/50 | **47/50** | 37.1% | 39.3% |

MMLU-Pro error margins are about ±4 points (lm-eval stderr 0.038–0.042).
"Strict" is lm-eval's own score. Its answer pattern only accepts
`The answer is (X)`. gpt-oss often wrote `**Answer: (D)**`, which strict
scoring counts as wrong (36 of its 140 answers were not parsed). The
format-tolerant column re-scores every model's saved answers with one pattern
that also accepts `Answer: (X)` and bold markers; remaining unparsed answers
were mostly cut off at the token limit.

Findings:

- **Simple tool calls do not separate these models.** The 1.7B LFM3 matches
  or beats models 10–20 times its size on BFCL simple/multiple, 2–3 times
  faster. Keep it as the fast fallback.
- **Knowledge and reasoning do.** Qwen3.6 35B-A3B scored 17 points above
  LFM2.5 24B-A2B, 11–22 above gpt-oss 20B and 34 above LFM3 on MMLU-Pro. It
  is the strongest model that runs on this host; one MMLU-Pro answer averaged
  about a minute.
- **LFM2.5 24B-A2B is the fast middle option:** best BFCL score here (95/100),
  about 1.7 times Qwen3.6's generation speed and 1.5 times its prompt speed,
  in 15 GB, but well behind it on MMLU-Pro.
- **Threads:** these models run best at 10–16 threads. At 24 threads
  generation collapsed to about 2 tok/s (Qwen3.6, Gemma 4), the opposite of
  the small dense model.
- **Whole model on the GPUs:** see section 6f.
- **Attention on the GPUs, experts in RAM** (`-ngl 99 -ncmoe 99 -fa on`)
  roughly doubled prompt speed (Qwen3.6 50 tok/s, gpt-oss 64) but cut
  generation by a third to a half, and it needs the GPU lock. Not used.
- **Prompt speed is the weak point:** 20–40 tok/s, about half of the GPU
  Qwen3.5 9B. A long OpenClaw system prompt takes minutes on the first turn.
- NVIDIA Nemotron 3.5 Lightning 30B-A3B (Q4_0, 18.9 GB, 18.8 GB RAM): speed
  only so far. Prompt 17–21 tok/s, generation 8.6 / 9.3 / 11.0 tok/s at 10 /
  12 / 16 threads, so it is as fast as Qwen3.6 or faster. `--reasoning-budget 0`
  turns its thinking off. BFCL and MMLU-Pro are not yet run.
- LFM2.5 speed was measured at 10, 12 and 16 threads only; its 24-thread and
  GPU-hybrid speeds were not measured.

Script: [`reference/bench-local-model.sh`](../reference/bench-local-model.sh).

## 6f. Mixture-of-experts models on the GPUs (2026-11-22)

Can a MoE model run on the two FirePro D700s (12 GB total, Vulkan)? Only
2-bit files fit with room for the KV cache. `llama-bench`, both GPUs
(`-ngl 99 -dev Vulkan0/Vulkan1 -ts 1,1 -sm layer -b 512 -ub 256`), prompt 512 /
generate 64, holding the GPU media lock, `amdgpu.lockup_timeout=60000`:

| Model | Where | Prompt tok/s | Generate tok/s |
| --- | --- | ---: | ---: |
| LFM2.5 24B-A2B QAD-Q2_K_L (8.9 GiB) | both GPUs, flash attention off | 45 | 10.1 |
| LFM2.5 24B-A2B Q4_K_M | CPU, 10 threads | 34 | **15.6** |
| Gemma 4 26B-A4B UD-IQ2_M (9.3 GiB) | both GPUs, flash attention off | 35 | 6.1 |
| Gemma 4 26B-A4B QAT Q4_0 | CPU, 16 threads | 19 | **9.4** |
| Qwen3.5 9B dense Q4_K_M (current GPU model) | both GPUs | ~44 | 4.2 |

Flash attention on was slightly slower for generation (9.1–9.6 and 5.1–5.2).
No driver resets. On these cards a MoE generates more slowly than the same
model on the CPU, and has to be cut to 2 bits to fit. It does beat the dense
9B now on the GPUs by 1.5–2.4 times on generation speed, but its 2-bit quality
was not measured. Keep large models on the CPU and the GPUs for image/video
and a small vision model.

Open-weight models found on 2026-11-22 that fit this hardware and were not yet
tested (vendor numbers only): Inkling 2 Mini (26.4B looped MoE, image input),
GLM-4.7-Flash 30B-A3B, Nemotron 3 Nano Omni 30B-A3B (text/image/audio/video),
Gemma 4 12B Unified (fits the GPUs at Q4_0), LFM2.5-8B-A1B, LFM3-VL-2B,
PaddleOCR-VL-1.6 and GLM-OCR (0.9B document OCR), EmbeddingGemma 2 (740M),
Parakeet-TDT-0.6B-v2 and Nemotron 3.5 ASR (speech-to-text), Kokoro-82M and
Kyutai Pocket TTS (text-to-speech), Z-Image Turbo (image generation).

## 7a. Speech (2026-11-21)

whisper.cpp was a CPU-only build (AVX, no AVX2/FMA), 12 threads, on the
standard 11-second JFK sample; Piper ran through its Python package on ONNX
Runtime, CPU only. Both were then tested through OpenClaw (see the
[2026-11-21 evidence record](local-fallback-and-media-2026-11-21.md)).

| Model | Wall time for 11 s of audio | Transcript |
| --- | ---: | --- |
| `ggml-base.en` | 1.9 s | correct words, comma instead of full stop |
| `ggml-small.en` | 6.2 s | exact |
| `ggml-large-v3-turbo-q5_0` | 30.7 s | exact |

## 8. Other pitfalls found

- **Embedding batch size:** an embedding server with a 256-token physical
  batch rejects longer chunks ("input too large"). OpenClaw memory chunks reach
  ~480 tokens. Use a batch and micro-batch of at least 512 (2048 used here).
- **Setup wizards can change your main model.** Connecting an existing local
  server during onboarding silently set the main agent's primary model to the
  local model. Check agent model settings after onboarding.
- **Model-entry flags matter:** a "supports tools: false" flag on a local model
  makes OpenClaw refuse every agent that requires tools.
- **btrfs free space** can take a moment to reflect deleted model files.

## 9. Models considered but not tested

From a 2026-11-17 survey of small open models (file sizes are Q4_K_M unless
noted). These were not run on this host; they are listed so others can judge
what is still unexplored.

| Model | Size | Notes |
| --- | ---: | --- |
| Qwen3.5 0.8B / 2B | 0.53 / 1.28 GB | vision-capable; emergency classifier / low-footprint baseline |
| LFM2.5 2.6B | 1.67 GB | older Liquid model; superseded by LFM3 |
| LFM3-VL 2B | 1.10 GB + projector | small vision candidate |
| Granite 4.2 3B / 8B | 2.24 / 5.35 GB | tools and reasoning challenger |
| MiniCPM5 2B | 1.56 GB | coding, maths and tools candidate |
| Gemma 4 E2B | 2.84 GB (Q4_0) | writing and vision |
| Ministral 3 3B | 2.15 GB | instruction and vision |
| Nemotron 3 Nano 4B | 2.84 GB | English reasoning; custom licence |
| Granite 4.0 H Tiny | 4.23 GB | hybrid MoE control |
| SmolLM3 3B, Phi-4-mini | — | older controls |
| Qwen3.8 27B (dense) | 16.6 GB | fits in RAM only; dense, so expected slower than the MoE models in section 6e |

## Evidence limits

- Single runs on one host; not a repeated qualification.
- Published benchmark scores are developer-reported and were not reproduced.
- Exact-match and agent tests are small; they show failure modes, not rates.
