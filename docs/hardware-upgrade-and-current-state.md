# Hardware Upgrade and Current State

## Current Platform

| Component | Verified current state |
|---|---|
| Host | 2013 Mac Pro 6,1 running Nobara Linux |
| Processor | One Intel Xeon E5-2697 v2, 12 cores / 24 threads |
| Memory | Official Apple 64 GB DDR3 ECC kit, 4 × 16 GB; Linux reports 65,801,300 kB total, approximately 62.75 GiB |
| Graphics | Two AMD FirePro D700 / Tahiti GPUs, 6 GiB VRAM each |
| Durable role | OpenClaw host and orchestrator for Thumbo |
| Inference placement | Qualified hosted routes by default; local Vulkan only inside an explicit bounded test or admitted lane |

This is one processor, not a dual-processor system. The two D700 VRAM pools are
independent and are not represented as one 12 GiB transparent pool.

## Chronology

| Date | State or outcome | Claim boundary |
|---|---|---|
| 2026-08-10 to 2026-08-14 | Historic local evidence recorded on the approximately 32 GiB host; strict maximum was 1/4 usefulness gates, and interactive Vulkan fault/timeout evidence remained | Establishes the original narrow local boundary only |
| 2026-08-14 | Multi-agent repair and verification documented role allowlists, least privilege, loopback Gateway scope, partial Researcher inheritance, and explicit external-action approval | Bounded operator-verified deployment, not certification |
| 2026-08-19 | Official Apple 64 GB DDR3 ECC kit installed | Capacity change only; no inference result follows from installation alone |
| 2026-08-20 | Guarded post-upgrade local-model qualification performed | Bounded 4K load, sentinel, benchmark, short-task usefulness, safety, and disposition evidence |

## What the Upgrade Changed

The memory upgrade removed the prior capacity-admission block for a guarded
Qwen2.5-Coder-32B-Instruct Q4_K_M attempt. The artifact technically loaded and
generated the exact sentinel, but at 0.3 token/s; its practical suite was
stopped during the first case before a response token. The upgrade therefore
changed the capacity boundary from “cannot enter this guarded test” to “can be
tested and rejected as impractical in this envelope.”

The same current host also produced bounded, safety-clean 4K benchmark evidence
for Qwen3.5-9B, official Qwen3-8B, and Qwen3.5-4B Q4_K_M artifacts. All three
returned exact sentinels, but each failed its complete speed-admission gate and
did not advance to its conditional interactive-usefulness suite.

Qwen3.5-4B then passed a separate frozen five-case short-task suite 5/5 under
the matrix-selected hybrid placement. That adds a bounded manual supplied-text
role; it does not change the interactive speed failure. No Qwen3.5-4B package,
OpenClaw provider, alias, route, or binding was created, and the effective-route
test remains pending.

## What the Upgrade Did Not Establish

- It did not prove that memory capacity caused or fixed the historic Vulkan
  ring-timeout, device-loss, kernel-trap, or interactive-timeout behavior.
- It did not replace the original strict 1/4 usefulness result.
- It did not qualify automatic routing, interactive serving, tools, commands,
  recovery work, multi-turn use, or long context.
- It did not deploy or route Qwen3.5-4B; the documented 5/5 result is a manual
  candidate admission only.
- It did not establish uptime, throughput outside the stated tests, a cost
  result, or general behavior for other Mac Pro or AMD systems.

## Portability and Revertibility

The durable architecture is portable at the route boundary: Thumbo's host,
role, evidence, and human-approval model do not depend on one provider or on
local Vulkan being admitted. A hosted route can be requalified or replaced
within the same specialist role without pretending that the local lane passed.

Local qualification is revertible by disposition rather than by destructive
change. A candidate that misses a gate remains excluded, its artifacts and
records are retained, and automatic routing remains disabled. Hardware and
runtime changes require a new dated evidence envelope; they never rewrite an
older result.

## Related Records

- [System Profile](system-profile.md)
- [Decision Record](decision-record.md)
- [Local-model Qualification](local-model-qualification.md)
- [Post-upgrade Local Qualification](../evidence/post-upgrade-local-qualification-2026-08-20.md)
- [Qwen3.5-4B Short-Task Qualification](../evidence/qwen35-4b-short-task-qualification-2026-08-20.md)
- [Known Issues](known-issues.md)
