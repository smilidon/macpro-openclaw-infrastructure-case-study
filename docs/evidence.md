# Evidence and Limits

## Public Conclusion

This repository supports a bounded conclusion: local Vulkan-offloaded
generative inference was not reliable enough for automatic routing on this
specific host, so the architecture restricts local generation and uses hosted
specialist routes for normal work.

## What Is in the Public Pack

| Claim area | Public support |
| --- | --- |
| Architecture boundary | [architecture.md](architecture.md) and [decision-record.md](decision-record.md) |
| Qualification method and promotion rule | [decision-record.md](decision-record.md) |
| System and workload scope | [system-profile.md](system-profile.md) |
| Safety design and stop conditions | [safety-controls.md](safety-controls.md) |
| Sanitized environment and retained qualification record | [evidence/](../evidence/) |
| Public-pack integrity | `make verify` and its checked-in script |
| Known gaps and non-goals | [known-issues.md](known-issues.md) |
| Current verified changes | [CHANGELOG.md](../CHANGELOG.md) and dated records in [evidence/](../evidence/) |

## What Is Deliberately Not Claimed

- A proven root cause for the AMDGPU/Vulkan failures.
- A reproducible benchmark, failure rate, or duration claim for the rejected
  Vulkan candidates.
- Any conclusion stronger than the provenance stated beside an evidence item.
- A reproducible stress harness or a universal conclusion about AMD hardware.
- Current provider/model availability, service levels, or cost figures.
- Production readiness beyond the single-host boundaries documented here.

## Local-model usefulness evidence

The public [local-model qualification and reproduction guide](local-model-qualification.md)
ties the exact host/runtime envelopes to role-specific dispositions. Its source
records separate successful execution from useful output:

- [TinyLlama 1.1B Chat Q2_K](../evidence/vulkan-usefulness-suite-2026-08-14.md)
  completed all four Vulkan processes but scored **0/4** strict semantic gates.
  It is retained only as a one-shot runtime smoke fixture.
- [`thumbo-safe` / Llama 3.2 1B Instruct Q8_0](../evidence/thumbo-safe-vulkan-usefulness-2026-08-14.md)
  scored **1/4**. It remains restricted to explicit, bounded, zero-tool,
  human-reviewed text and is not agent-qualified.

The four-gate contract requires exact fact-locked JSON, exact retrieval of a
planted supplied-context value, an exact bounded-arithmetic answer, and a
one-sentence no-edit safety boundary. Autonomous or operational promotion
requires 4/4 plus a clean process, kernel-log, watchdog, and thermal result.
Throughput and exit/HTTP success do not compensate for a failed semantic gate.

Embedding and cloud models are explicitly excluded. The suite does not measure
embedding/vector quality or embedding-runtime stability, and cloud inference
does not exercise the local D700/Vulkan path. Neither category contributes to
the published 0/4 or 1/4 results.

## Private Source Handling

The public packet was checked against retained operational records. The
sanitized subset is now published in [evidence/](../evidence/), with explicit
provenance and missing-artifact disclosures. The private originals contain
paths, host state, dated configuration, operational commands, and other
material unsuitable for a public repository.

The next evidence increment should add a new, guarded, machine-readable run
with a version manifest, structured results, relevant system-log window, and
observer note. It must not recreate a rejected high-risk Vulkan workload merely
to produce a public failure log.
