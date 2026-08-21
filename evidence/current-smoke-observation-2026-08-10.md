# Current Bounded Local-Lane Observation — 2026-08-10

> **Chronology note — 2026-08-20:** “Current” in this title refers to the
> 2026-08-10 observation on the pre-upgrade, approximately 32 GiB host. An
> official Apple 64 GB kit was installed on 2026-08-19; current Linux reporting
> is approximately 62.75 GiB usable. Post-upgrade qualification is documented
> separately and does not alter this dated result.

## Purpose

Confirm that the approved local manifest can be loaded under the current safety
configuration without treating a smoke test as broad qualification.

## Observation

- `thumbo-safe:latest` loaded with a 32K context and four-layer GPU offload.
- Ollama reported a 75% CPU / 25% GPU processor split.
- GPU edge temperature was 46°C before the test and observed at 47–50°C during
  the bounded retrieval attempts.
- CPU package temperature was 50°C before the test and observed at 51–56°C
  during the attempts.
- No new AMDGPU ring-timeout, reset, Vulkan device-loss, or related kernel
  event was observed while the model was resident.

## Small-Context API Check

A 4K-context, zero-tool API request completed with HTTP 200. The runtime
reported 51 prompt tokens in 25.11 seconds (2.03 prompt tokens/second), eight
generated tokens in 1.39 seconds (5.74 tokens/second), and 30.98 seconds total.
This establishes that the current service can complete a small request under
the observed safety conditions.

## Limitation and disposition

The direct 32K retrieval harness did not yield a clean machine-readable
response through the capture path used for this observation. The 4K API
response body was likewise not retained by that capture path. Exact-answer
correctness is therefore **not claimed** here. This is a hardware-safety and
small-request service observation only, not a repetition of the historical 18K
retrieval result.

No rejected model was downloaded, restarted, or stress-tested.

## Follow-up evaluation

A fixed 4K, zero-tool evaluation suite was subsequently run using the method
in `TEST_METHOD.md`. It confirmed a clean hardware observation but did **not**
qualify the model for the intended supplied-text tasks: the isolated incident
summary case returned gibberish despite HTTP 200. See `results/README.md` for
the captured records and precise disposition.

The later four-gate strict usefulness record passed 1/4 gates and did not meet
the admission threshold. This smoke observation does not supersede that result.
