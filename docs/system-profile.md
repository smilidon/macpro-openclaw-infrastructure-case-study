# System Profile and Workload

## Platform in Scope

This case study concerns one 2013 Mac Pro 6,1 running a Fedora-family Linux distribution (Nobara). The machine currently features:

- **Processor:** Intel Xeon E5-2697 v2
- **Memory:** official Apple 64 GB DDR3 ECC kit (4 × 16 GB); current Linux reporting is approximately 62.75 GiB usable
- **Graphics:** Dual AMD FirePro D700 GPUs (`1002:6798`, Apple subsystem IDs `106b:0128` and `106b:0127`), 6 GiB VRAM each (GCN 1.0 architecture)

The original strict usefulness and historic fault evidence used the earlier,
approximately 32 GiB configuration. The 64 GB kit was installed on 2026-08-19.
Post-upgrade qualification was performed on 2026-08-20 and is documented
separately; capacity improvement is not evidence that RAM caused or fixed the
historic Vulkan behavior.

It is an intentionally constrained, legacy workstation—**not** a proxy for current accelerator hardware or AMD GPUs generally.

---

## Workload Being Qualified

The question was not whether a model could produce an attractive short answer. The target workload was an **agent runtime** that must sustain:

- Long supplied context with structured output and syntax adherence
- Multi-step reasoning and safe refusal under schema pressure
- Bounded tool use with strict schema conformance
- Repeated conversational turns and sustained inference pressure
- Nested delegation across specialized agent roles
- Least-privilege tool boundaries enforced by the gateway
- Modality surfaces with explicit fallback behavior
- Configuration, security, and recovery validation in the same loop

That distinction matters: a route that appears usable in an isolated chat can still be unsafe or ineffective in an operational agent role.

---

## Design Constraints

- Existing legacy hardware and a near-zero capital budget
- **No automatic use** of a route that has not passed its intended workload gate
- Hardware safety takes precedence over local throughput
- Private configuration, account information, host paths, and raw logs cannot be published as portfolio material
- Single-host scope: no cluster, no failover, no distributed inference

---

## Resulting Architecture

The resulting system is **routed-first for normal agent work**, with qualified hosted inference used intentionally and a small local lane that is deliberately constrained.

- **Hosted specialist routes** handle normal operational tasks within role-specific tool boundaries.
- **Local offline lane** is restricted to explicit, zero-tool, bounded text tasks—no automatic routing, tool use, or delegation.
- **Gateway policy** enforces least-privilege tools and schema-validated configuration.
- **Multi-agent roles** separate coordination, career context, research, writing, coding, media, and outbound-copy preparation.
- **Configuration, security, and recovery checks** are part of the operating method rather than afterthoughts.

See [Architecture](architecture.md) for the route boundary.

---

## 2026-08-14 Validation Outcomes

The documented maintenance cycle produced these verified outcomes on this host:

- **Schema-valid repair** applied against the installed OpenClaw version
- **Loopback-only Gateway** remained healthy after validation and hot reload
- **Deep security audit** completed with 0 critical, 4 warning, and 2 informational findings
- **Writer boundary** deterministically permitted an in-workspace read and denied an outside read before disclosure
- **Coder tools** created, read, edited, hashed, and removed a temporary file inside the intended workspace on the Sol/high route
- **Career, Researcher, and Broadcaster boundaries** were narrowed and inspected through isolated tests
- **Modality specialists** were exercised only through their proper image, speech-generation, and transcription surfaces

Local semantic evaluation remained below the promotion gate:

- **0/4** on one interactive/conversational usefulness suite
- **1/4** on the other tested local route
- **Bounded Vulkan smoke** completed a single turn within the recorded thermal and timeout limits

**No automatic local route is enabled.** The local lane remains opt-in for explicitly bounded, zero-tool work.

## 2026-08-20 Post-Upgrade Outcomes

- Qwen2.5-Coder-32B-Instruct Q4_K_M became technically loadable but generated
  its sentinel at 0.3 token/s and did not complete the practical suite.
- Qwen3.5-9B, official Qwen3-8B, and Qwen3.5-4B Q4_K_M artifacts completed
  bounded 4K exact-sentinel and benchmark stages but failed their full speed
  admission gates.
- Completed guarded measurements were safety-clean within their recorded
  envelopes; no conditional interactive-usefulness suite ran for the three
  speed-gated benchmark candidates.

The resulting disposition is bounded benchmark evidence only—not interactive,
automatic, tool, recovery, or long-context qualification. See
[Post-upgrade Local Qualification](../evidence/post-upgrade-local-qualification-2026-08-20.md).

Qwen3.5-4B subsequently passed a **separate** frozen five-case short-task suite
5/5 under the matrix-selected hybrid placement. Mean/median wall time was
6.998/7.180 seconds; median prompt/generation throughput was 17.1/5.5 token/s.
This adds a manual short supplied-text qualification with human review, not an
interactive-performance admission. The candidate is not configured, routed,
or deployed in OpenClaw. See [Qwen3.5-4B Short-Task Qualification](../evidence/qwen35-4b-short-task-qualification-2026-08-20.md).

---

## Reproduction Vector

The public [Vulkan single-turn smoke record](../evidence/vulkan-single-turn-smoke-2026-08-14.md) names the exact D700 PCI IDs, kernel, RADV version, `llama.cpp` revision, model hash, build mode, CLI flags, timeout, thermal observation, and result. It is the technical reference for comparable Mac Pro 6,1 hardware; it is deliberately **not** a claim of interactive or production inference support.

---

## Evidence Boundary

- **Public:** architecture, sanitized evidence summaries, safety controls, qualification vectors, and reproduction records
- **Private:** gateway configuration, credentials, host paths, raw sessions, account details, and recovery material

This boundary keeps the portfolio useful without turning operational internals into public artifacts.

---

## Related Documents

- [Architecture](architecture.md) — system architecture and routing
- [Evidence and Limits](evidence.md) — what supports claims and what is excluded
- [Safety Controls](safety-controls.md) — stop conditions and thermal bounds
- [Local-model Qualification](local-model-qualification.md) — exact test vectors and scores
- [Hardware Upgrade and Current State](hardware-upgrade-and-current-state.md) — exact chronology and current capacity
- [Qwen3.5-4B Short-Task Qualification](../evidence/qwen35-4b-short-task-qualification-2026-08-20.md) — exact short-task envelope and admission boundary
