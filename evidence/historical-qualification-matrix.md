# Historical Qualification Matrix

> **Evidence-status note — 2026-08-20:** This matrix preserves historical
> observations from the pre-upgrade, approximately 32 GiB host. The reported
> 18,263-token retrieval lacks the original public run artifacts and does not
> establish a stable context boundary above 8K. Later reproducible strict
> usefulness testing passed 1/4 gates and did not meet admission threshold.
> An official 64 GB kit was installed on 2026-08-19; current Linux reporting is
> approximately 62.75 GiB usable, but no result below was run in that state.

Source: retained Codex local-model handoff dated 2026-07-30. The records below
are treated as historical engineering evidence. Raw run directories and the
original crash-journal windows were not retained in the public workspace.

| Model | Historical result | Disposition |
| --- | --- | --- |
| `thumbo-safe:latest` (Llama 3.2 1B) | Correct short facts, arithmetic, refusal behavior, tool arguments, and exact retrieval from an 18,263-token prompt at a 32K allocation; four-layer hybrid run reported no new AMD/Vulkan fault. | Admitted only for explicit, bounded, zero-tool Offline work. |
| `qwen3:8b` | Passed four short cases at about 17.7 output tokens/second, then repeatedly hit Vulkan device loss and AMD GPU resets under real 15.6K–15.8K full-agent prompts. | Quarantined; removed; never automatic or emergency fallback. |
| `granite4.1:3b` | Passed a 4K guarded bakeoff, then an 8K allocation with a 4,098-token prompt caused ring timeout, GPU reset, lost VRAM, device loss, and parser failure at about 49°C. CPU-only 4K retrieval was safe but took 176.5 seconds and returned the wrong answer. | Disqualified for routing; removed. |
| `nemotron-3-nano:4b` | Correct short tool-routing cases and about 25.4 output tokens/second; failed exact retrieval from 16,386 tokens. | Historical comparison only. |
| `qwen2.5vl:3b` | Correct visual facts and OCR under a 4K runtime context, but malformed requested JSON. | Historical comparison only; structured output required validation. |

## Historical decision

The retained record supports a narrow conclusion: sustained, large-context
Vulkan generation was not reliable enough for automatic routing on this host,
and moderate temperature alone was not an acceptance signal. It does not prove
a universal AMD, Vulkan, driver, or model-family defect.

## Missing historical artifacts

- Exact kernel and driver manifests for each run.
- Original per-stage JSON outputs and prompt hashes.
- Raw thermal time series and crash-journal windows.
- A reproducible public version of the full-agent prompt.

These are intentionally listed as absent. Future work should add new, sanitized
captures rather than reconstructing them from memory.
