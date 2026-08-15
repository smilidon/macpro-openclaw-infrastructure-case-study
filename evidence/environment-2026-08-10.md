# Sanitized Test Environment — 2026-08-10

## Host scope

- Hardware: 2013 Mac Pro 6,1 with dual AMD FirePro D700 GPUs.
- Operating system: Nobara Linux.
- Kernel: `7.1.4-200.nobara.fc44.x86_64`.
- Local inference service: Ollama, with one-model residency and one-request
  parallelism enforced.

## Local model under observation

- Manifest: `thumbo-safe:latest`.
- Foundation: Llama 3.2 1B, as recorded in the retained qualification handoff.
- Allocation: 32K context, deterministic decoding, and four GPU layers on the
  non-display D700.
- Allowed use: explicit, bounded, zero-tool summarization, rewriting,
  extraction, classification, and formatting.

## Active guardrails

| Guardrail | Value |
| --- | --- |
| GPU edge stop threshold | 76°C |
| CPU package stop threshold | 82°C |
| SMC-derived stop threshold | 78°C |
| Resident local generators | One maximum |
| Local generation parallelism | One maximum |
| Automatic fallback into local generation | Prohibited |

This file deliberately omits hardware serials, network data, private paths,
account data, and service secrets.
