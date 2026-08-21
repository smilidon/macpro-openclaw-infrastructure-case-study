# Evidence Pack

This directory separates evidence by provenance so that a reader can tell what
was directly captured, what is a retained engineering record, and what was not
preserved for public release.

## Contents

- `environment-2026-08-10.md` records the current, non-sensitive test
  environment.
- `historical-qualification-matrix.md` is a sanitized transcription of the
  retained Codex handoff. It is historical operational evidence, not a new
  reproduction.
- `current-smoke-observation-2026-08-10.md` records a bounded local-lane
  observation and its limitations.
- `vulkan-single-turn-smoke-2026-08-14.md` records a reproducible dual-D700,
  one-card-at-a-time Vulkan smoke test, including the full hardware/software
  test vector and its narrower-than-production disposition.
- `vulkan-usefulness-suite-2026-08-14.md` publishes the fixed useful-work
  gates, exact prompts and outputs, and the exclusion decision for TinyLlama
  1.1B Chat Q2_K on the Vulkan test stack.
- `post-upgrade-local-qualification-2026-08-20.md` records the sanitized
  post-64GB Qwen2.5-Coder-32B guard sequence and the completed dual-D700 4K
  Qwen3.5-9B, Qwen3-8B, and Qwen3.5-4B benchmark dispositions, including
  artifact/build hashes, safety extrema, rerun correction, and source map.
- `qwen35-4b-short-task-qualification-2026-08-20.md` records the separate
  frozen 5/5 short-task usefulness result, exact hybrid execution envelope,
  timing and safety bounds, retained chronology and source-map labels, and the
  explicit fact that the candidate is not an OpenClaw route or deployment.
- `TEST_METHOD.md` defines the fixed, bounded evaluation method used for the
  current local lane.
- `results/README.md` indexes the captured evaluation runs and their
  disposition.

## Evidence rules

- A historical record supports an engineering decision, but does not turn a
  past test into a reproducible public benchmark.
- No raw crash journal, prompt corpus, model blob, private configuration, host
  identifier, or credential is included here.
- No claim about a local model is stronger than the evidence beside it.
- The absence of an artifact is stated plainly rather than filled with a
  reconstructed or simulated substitute.
- A guard stop, speed-gate stop, or human stop is not converted into an absent
  semantic or quality score.
- A later role-specific short-task admission does not overwrite an earlier
  interactive speed-gate failure; the two dispositions answer different
  questions and remain visible together.

## Reproduction boundary

The installed local model may be exercised only through the explicit,
zero-tool Offline lane. The newly qualified Qwen3.5-4B artifact is not installed
or routed through OpenClaw; its evidence supports manual invocation only.
Rejected Vulkan candidates are not restarted merely to recreate a failure. A
future reproduction requires a separately approved, guarded plan with one
resident model, active thermal and kernel monitoring, and an immediate-stop
policy for GPU reset or device-loss signals.
