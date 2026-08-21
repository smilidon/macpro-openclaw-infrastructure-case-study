# Post-Upgrade Local Qualification — 2026-08-20

## Verdict and Scope

Guarded qualification **was performed after the official 64 GB upgrade**. The
results expand the evidence boundary from the historic approximately 32 GiB
environment, but they do not admit a local route for automatic, interactive,
tool, recovery, or autonomous work.

- Qwen2.5-Coder-32B-Instruct Q4_K_M technically loaded but was impractically
  slow and did not complete its usefulness suite: **not useful / not
  qualified**.
- Qwen3.5-9B, official Qwen3-8B, and Qwen3.5-4B Q4_K_M artifacts loaded,
  returned exact sentinels, and completed bounded 4K benchmarks. Each missed
  its complete speed-admission gate: **benchmark evidence only / not admitted
  for interactive use**.
- No candidate reached the conditional interactive-usefulness suite in the
  original speed-gated comparison. No absent quality score is converted into
  a semantic failure.

Later the same day, Qwen3.5-4B passed a **separate** frozen five-case short-task
suite 5/5. That later record creates only a manual short-task admission; it
does not change this comparison's failed interactive speed gate. See
[Qwen3.5-4B Short-Task Qualification](qwen35-4b-short-task-qualification-2026-08-20.md).

These are dated results on one Mac Pro 6,1 with one Intel Xeon E5-2697 v2,
two FirePro D700 GPUs with 6 GiB VRAM each, and 65,801,300 kB total physical
memory (approximately 62.75 GiB).

## Historic and Current Boundaries

The original retained usefulness maximum remains **1/4 strict gates** on the
pre-upgrade, approximately 32 GiB host. A historic interactive Vulkan fault and
later timeouts also remain part of the architecture decision. The later
safety-clean bounded runs do not erase those results and do not prove that RAM
caused or fixed Vulkan behavior.

## Qwen2.5-Coder-32B Guarded Result

| Item | Exact recorded value |
|---|---|
| Artifact | Official `Qwen/Qwen2.5-Coder-32B-Instruct-GGUF`, revision `9d3053fce650fe1cdbdb75998c2a87add9d178ef` |
| File / quantization | `qwen2.5-coder-32b-instruct-q4_k_m.gguf`, Q4_K_M |
| Size / SHA-256 | 19,851,335,872 bytes / `4d64b316b5e6319d9613e0d97935d9ebd631fc7e334da400d00085eca749d085` |
| Runner | llama.cpp Debug/O0 commit `8e7f22b67ef4667b4ddd50230771287f328cfb3f`; binary SHA-256 `8efa16ddeace39a618140a16d9a1a7bb419ccb4c5d78430f480b30b67b5978f3` |
| Stage 1 | Exact `QWEN32B_SENTINEL_OK`; 373.235225 s; prompt 0.2 token/s; generation 0.3 token/s |
| Practical suite | First case externally stopped after 128.045427 s before any response token; remaining 24 not run |
| Exact scoring boundary | 0/1 attempted with a runtime failure; **not** a semantic 0/25 |
| Disposition | Technically loadable, not useful, not qualified |

Two earlier Stage 1 attempts ended at explicit swap-policy guards before model
load completed. The first was CPU-only and stopped when swap became nonzero;
the second used 20 GPU layers across both D700s and stopped when swap exceeded
its immutable admission baseline. These were guard-policy stops, not semantic
model failures. A later explicitly authorized run monitored swap without using
growth as a stop; all other hardware, thermal, service, kernel, process, and
memory-floor guards remained active.

The final practical case stop was an external cancellation, not a hardware
guard trip. No later case ran, and cleanup found no remaining inference or
scoring process.

## Completed Dual-D700 4K Comparison

Throughput values are medians over three repetitions. The admission floors
were pp512 >=60 token/s and tg128 >=8 token/s; both parts had to pass before a
conditional four-case usefulness suite.

| Artifact and placement | pp512 token/s | tg128 token/s | Exact sentinel | Gate and disposition |
|---|---:|---:|---|---|
| Qwen3.5-9B Q4_K_M, full dual-GPU offload, 30/70 display/non-display split | 35.2522 (34.6523–35.8917) | 5.75994 (5.72211–5.84995) | `QWEN35-PINNED-OK`, 7.748 s | Both speed floors missed; benchmark evidence only |
| Official Qwen3-8B Q4_K_M, full layer/output offload, 30/70 split | 12.9765 (12.7291–13.1188) | 9.0655 (8.90158–9.19801) | `QWEN3-8B-OFFICIAL-OK`, 6.622 s command window | Generated-token floor passed, prompt floor missed; benchmark evidence only |
| Qwen3.5-4B Q4_K_M, full GPU, 1/1 split | 40.3410 (38.6862–40.3895) | 3.61279 (3.53886–3.88348) | Exact pass | Complete speed gate failed; matrix candidate only |
| Qwen3.5-4B Q4_K_M, hybrid 16/32 layers, 8/8 allocation | 24.6539 (24.4549–24.8199) | 4.92894 (4.91464–5.04356) | `QWEN35-4B-B-OK`, 8.597 s | Matrix winner by lower estimated 512+128 time; speed gate failed; benchmark evidence only |

The Qwen3.5-4B hybrid winner's estimated 512+128 compute time was 46.737 s,
versus 48.121 s for full GPU. “Winner” applies only to that two-row matrix
rule; it is not route admission.

## Artifact and Runner Identity

| Artifact | Lineage and immutable revision | Size / SHA-256 |
|---|---|---|
| Qwen3.5-9B Q4_K_M | Official `Qwen/Qwen3.5-9B` lineage `c202236235762e1c871ad0ccb60c8ee5ba337b9a`; third-party `unsloth/Qwen3.5-9B-GGUF` conversion `3885219b6810b007914f3a7950a8d1b469d598a5` | 5,680,522,464 bytes / `03b74727a860a56338e042c4420bb3f04b2fec5734175f4cb9fa853daf52b7e8` |
| Qwen3-8B Q4_K_M | Official `Qwen/Qwen3-8B-GGUF` revision `7c41481f57cb95916b40956ab2f0b139b296d974` | 5,027,783,488 bytes / `d98cdcbd03e17ce47681435b5150e34c1417f50b5c0019dd560e4882c5745785` |
| Qwen3.5-4B Q4_K_M | Official `Qwen/Qwen3.5-4B` lineage `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`; third-party `unsloth/Qwen3.5-4B-GGUF` conversion `720bb031aae5488eae5d6a78768e6d826662b2ae` | 2,740,937,888 bytes / `00fe7986ff5f6b463e62455821146049db6f9313603938a70800d1fb69ef11a4` |

The three completed comparison records used llama.cpp `0.1.2-dev`, build
10546, commit `0e1d9185c5fe82e905d1f5ae6b2e5dcd607a8dfd`, built with GNU 16.1.1
as RelWithDebInfo with explicit `-O2 -g -DNDEBUG` and Vulkan enabled.
Selected build hashes were:

| Build artifact | SHA-256 |
|---|---|
| `llama-cli` | `d2e47ba868c81e30db30ac10dfde8ab18e8e2fe1fbdd928790bff065d8d9ef56` |
| `llama-bench` | `d4869cfde38b90c92c047bae7bc5a2ec26f2cf0c29e260f9c5e5c0fd39bef635` |
| Vulkan backend library | `08aded21f9af9ad9f94a2f3ba14ee625425585d71e1f97452f12f42a52c3d3a1` |
| CPU backend library | `b49592e5df903fea45896296115941150c290d0a6760430580d68343d9a141da` |

The Qwen3-8B and Qwen3.5-4B records revalidated the retained runner/hash set
instead of silently rebuilding it.

## Fixed Envelope and Route Scope

The completed comparison was 4,096-token context, text-only, zero-tool,
single-turn, deterministic, and network-isolated. It used CPU KV, flash
attention off, layer splitting across both Vulkan devices, three pp512/tg128
repetitions, and 12 CPU threads. The guard sampled at 250 ms and covered memory,
swap, EDAC/HardwareCorrupted, thermals, VRAM margin, service stability,
timeouts, process cleanup, and live/postflight kernel faults.

This envelope does not qualify multimodal work, embeddings, tools, commands,
agent delegation, recovery, serving, automatic fallback, multi-turn use,
contexts above 4K, or quality/usefulness where the conditional suite did not
run. Hosted models are a separate route category and are not counted as local
D700 qualification.

## Safety Extrema

| Completed measurement | Minimum `MemAvailable` | Maximum sampled swap | Peak VRAM used, non-display / display | Peak GPU / CPU temperature |
|---|---:|---:|---:|---:|
| Qwen3.5-9B benchmark | 55,128,121,344 bytes | 1,529,212,928 bytes | 4,291,084,288 / 2,118,512,640 bytes | 61 / 66 C |
| Qwen3-8B benchmark | 56,367,243,264 bytes | 1,485,561,856 bytes | 3,622,494,208 / 2,234,314,752 bytes | 60 / 62 C |
| Qwen3.5-4B complete matrix | 53,066,231,808 bytes | 1,375,739,904 bytes | 2,091,470,848 / 2,002,993,152 bytes | 64 / 68 C |

Across these completed measurements, HardwareCorrupted and EDAC CE/UE counters
remained zero. No qualifying kernel/Vulkan fault, thermal or memory-floor
breach, service restart, or residual inference process was recorded. The
safety verdict is bounded to these intervals; it is not an uptime or sustained
stability claim.

## Semantic and Operational Stop Conditions

Promotion stops when any required literal semantic output, route identity,
speed floor, tool boundary, hardware guard, or cleanup check fails. A guard
stop is not scored as model semantics. A failed speed gate prevents the
conditional quality suite; an unrun suite has no score. A human stop ends the
run and does not become evidence about the response that was never generated.

## Rerun and Correction Notes

The first Qwen3.5-4B load began while its downloaded file was still growing and
failed a file-bounds check. The retained retry required no downloader process,
exact byte count and SHA-256, six-second size stability, a parse ending at the
exact final byte, and a standalone zero-token load before inference. All hard
gates passed, so the complete-file retry—not the race—is the authoritative
matrix result. The initial failure remains preserved as chronology and is not
misreported as model incompatibility.

Any rerun must pin artifact and runner revisions, rehash model and build,
preserve completed-file gates, keep the same route placement and guard policy,
record literal scorer output, and validate a fresh manifest. A changed runtime,
quantization, context, device placement, guard, or acceptance floor is a new
evidence envelope.

## Sanitized Source Map and Manifest Provenance

| Public claim | Retained source record label | Public treatment |
|---|---|---|
| 32B load, exact sentinel, guard stops, and external stop | `QWEN32B-Q4-GUARDED-PILOT-20260820T141003-0400`, `QWEN32B-Q4-PARTIAL-GPU-STAGE1-20260820T143449-0400`, `QWEN32B-Q4-FULL-25-20260820T151211-0400` | Exact sanitized summary; private roots and raw operations excluded |
| Qwen3.5-9B benchmark | `QWEN35-9B-Q4-PINNED-DUAL-D700-20260820T161317-0400` | Exact identity, medians, bounds, safety, and disposition |
| Official Qwen3-8B benchmark | `QWEN3-8B-Q4-OFFICIAL-DUAL-D700-20260820T165500-0400` | Exact identity, medians, bounds, safety, and disposition |
| Qwen3.5-4B corrected matrix | `QWEN35-4B-Q4-GPU-CPU-MATRIX-RETRY-COMPLETE-FILE-20260820T182325-0400` | Exact complete-file correction, matrix, safety, and disposition |

Manifest validation recorded all 60 CPU-pilot entries, all 46 partial-GPU
entries, all 104 full-32B entries, all 6,583 Qwen3.5-9B entries, all 78
Qwen3-8B entries, and all 79 corrected Qwen3.5-4B entries as valid/OK in their
respective retained records. The public repository does not import private
paths, raw sessions, service state, or recovery-sensitive operations.

## Future Evidence Requirements

Admission would require a newly approved run that preserves the identities and
guards above, passes the route's complete speed gate, completes a fixed
usefulness suite with literal scoring, and adds repeated-turn and intended-role
tests before any broader claim. Tool use, larger context, serving, and automatic
routing each require separate gates. No high-risk run should be recreated only
to make a public failure artifact.

For the separately admitted manual short-task role, the later 5/5 record is the
controlling evidence. Interactive, repeated-turn, serving, tool, and automatic-
routing promotion still require the broader gates described here.
