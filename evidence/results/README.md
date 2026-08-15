# Captured Evaluation Results

## Method

These files are outputs from `../run-safe-evals.sh`, using the bounded method
in `../TEST_METHOD.md`: `thumbo-safe:latest`, zero tools, 4K context, four
GPU layers, deterministic sampling, short output caps, and an immediate stop
condition for GPU/kernel faults. They are observations of one host and one
installed manifest, not a general model benchmark.

## Runs

| Run | Scope | Result | Disposition |
| --- | --- | --- | --- |
| `thumbo-safe-20260810T014609-0400.json` | Four fixed cases | Two requests timed out; exact retrieval did not pass; strict classification did not pass. The JSON-shaped response was semantically correct, but the first-run evaluator had an escaping defect, so it is not counted as a pass. | No functional qualification. |
| `thumbo-safe-20260810T015043-0400.json` | Isolated incident-note summary, a real supplied-text use case | HTTP 200 after 59.1 seconds; response was `ubes???????????????`. No kernel fault was captured. | Functional failure; do not use free-form local summaries. |
| `thumbo-safe-20260810T212928-0400.json` | Repaired evaluator; isolated exact retrieval | HTTP 200 after 60.8 seconds; response was repeated gibberish instead of `HARBOR-7429`. No kernel fault was captured. | Functional failure confirmed; do not use the model for supplied-text tasks. |
| `thumbo-safe-20260810T215759-0400.json` | CPU-only exact-retrieval control after correcting Vulkan device selection | HTTP 200 in 5.46 seconds; exact response `HARBOR-7429`. No kernel fault was captured. | Control passed. |
| `thumbo-safe-20260810T215835-0400.json` | Exact retrieval with four layers on the verified non-display D700 | HTTP 200 in 5.87 seconds; exact response `HARBOR-7429`. Runtime log identified Vulkan0 as AMD Radeon R9 200 / HD 7900 Series at PCI `0000:06:00.0`. No kernel fault was captured. | Guarded D700 check passed; proceed only through the remaining bounded suite. |

## Conclusion

The test distinguishes host stability from task quality. The approved local
lane completed requests without an observed AMDGPU/Vulkan fault, but it did
not produce reliable output for a basic, source-grounded summary. It therefore
has **no current functional qualification** for summary, extraction,
classification, or formatting work. No routing change is made by this evidence
record; any future use requires a corrected harness and a passing, reviewable
evaluation run.
