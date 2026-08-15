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

## Reproduction boundary

The installed local model may be exercised only through the explicit,
zero-tool Offline lane. Rejected Vulkan candidates are not restarted merely to
recreate a failure. A future reproduction requires a separately approved,
guarded plan with one resident model, active thermal and kernel monitoring, and
an immediate-stop policy for GPU reset or device-loss signals.
