# Decision Record: Local Inference Boundary and Multi-Agent Coordination

> **Status:** Accepted — these boundaries stand until new guarded qualification
> runs produce revised evidence.

## Context

- **Platform:** 2013 Mac Pro 6,1, dual AMD FirePro D700 GPUs (6 GiB VRAM
  each), one Intel Xeon E5-2697 v2, Nobara Linux. Historic usefulness evidence
  used approximately 32 GiB RAM; an official Apple 64 GB kit was installed on
  2026-08-19 and current Linux reporting is approximately 62.75 GiB usable.
- **Workload:** OpenClaw agent runtime — long contexts, structured output, tool
  use, delegation, and sustained inference
- **Historic local-inference problem:** guarded Vulkan-offload experiments triggered
  AMDGPU ring-timeout and device-loss failures under agent-style pressure.
  Failures occurred below thermal stop thresholds, so temperature alone was
  not an acceptance signal.
- **Coordination problem:** a general assistant needs specialist capability
  without granting every model the same context, tools, or external authority.
- **Claim boundary:** this record does not name a single hardware root cause,
  generalize to all AMD systems, or certify the deployment as risk-free.

## Decision 0: Preserve the Host/Orchestrator Role

The Mac Pro remains the durable home and coordinator for Thumbo. Thumbo's
primary purpose is human-supervised career support: preparing and organizing
materials, research, and interview-related work for review. Inference may use
a qualified hosted route; local execution is not a condition of successful
reuse.

**Rationale:** the host has a useful, durable role even when one accelerator
subsystem has a narrow admission boundary. Separating host value from inference
placement makes the design portable, reviewable, and honest about capability.

## Qualification Method

No route is promoted from a promising demonstration alone. It is assessed for
the capabilities and safety boundaries of its intended job.

| Gate | What it checks | Pass requirement |
|------|----------------|------------------|
| **1. Structured output** | Exact syntax and repair behavior | Valid output with no invented repair |
| **2. Context retrieval** | Recovery of a planted supplied fact | Exact target recovered |
| **3. Reasoning and refusal** | Correct bounded reasoning plus an explicit refusal constraint | Both requirements satisfied |
| **4. Tool use** | Native schema-conformant invocation where tools are permitted | Correct method, arguments, and effective tool boundary |
| **5. Operational behavior** | Resource limits, logs, isolation, delegation, and fallback behavior | No stop condition, unauthorized surface, or host instability |

**Promotion rule:** failure at any gate stops promotion. The route may be
narrowed, retested after a specific corrective change, or excluded from
automatic use. Hardware or safety-control failure ends the run immediately; it
is not normalized as a benchmark result.

## Decision 1: Local Inference Boundary

| Route | Decision |
|-------|----------|
| **Hosted specialist routes** | Use for normal agent workloads |
| **Local generation** | Retain only for explicit, bounded, zero-tool supplied-text work |
| **Automatic local fallback** | **Excluded** — never for hosted-route failure, recovery, commands, or operational decisions |

### Rationale

The project favors a clearly understood boundary over fake resilience. A model
that is fast in a narrow demonstration but unreliable in its intended role does
not belong in automatic routing. The local lane remains deliberately narrow so
a hardware-risk domain cannot become a hidden recovery fallback.

### Revisit Criteria

Revisit only with a guarded run that records sanitized runtime, build, model,
and configuration versions; test inputs and structured results; relevant
kernel-log, thermal, and process observations; and an observer note explaining
the disposition.

### Post-upgrade disposition — 2026-08-20

The 64 GB upgrade enabled bounded tests that the earlier capacity envelope
could not admit. Qwen2.5-Coder-32B Q4_K_M technically loaded but generated at
0.3 token/s and did not complete its practical suite. Three smaller Qwen
artifacts completed exact sentinels and guarded 4K benchmarks, but each failed
its full speed-admission gate and did not advance to the conditional
interactive-usefulness suite. These results add evidence; they do not prove a
Vulkan fix or authorize
automatic, interactive, tool, recovery, or long-context use. The full sanitized
record is [Post-upgrade Local Qualification](../evidence/post-upgrade-local-qualification-2026-08-20.md).

A later, separately scoped Qwen3.5-4B suite passed 5/5 short-task cases,
including the mandatory authorization stop. The accepted decision is manual
short supplied-text use with human review under the exact 4K hybrid envelope.
The earlier interactive speed failure remains controlling, and no provider,
alias, route, binding, packaging, or deployment decision was made. See
[Qwen3.5-4B Short-Task Qualification](../evidence/qwen35-4b-short-task-qualification-2026-08-20.md).

## Decision 2: Multi-Agent Coordination (2026-08-14)

| Aspect | Decision |
|--------|----------|
| **Main** | General coordinator with an explicit allowlist: Career, Researcher, Writer, Coder, Vision, and Broadcaster |
| **Career** | Persistent and fact-locked; delegates only to Researcher and Writer |
| **Writer** | Workspace-only file tools; no runtime, web, messaging, or publishing |
| **Researcher** | No runtime or write tools; nested search/fetch worked, but configured browser/read was lost, so capability remains partial |
| **Broadcaster** | Zero tools; draft preparation only |
| **Coder** | Direct from Main on the Sol/high route with narrow workspace-only coding tools |
| **Vision, TTS, Transcriber** | Modality-only use through their proper input surfaces |
| **Delegation default** | Isolated context and concise task briefs |
| **External actions** | Sending, publishing, submissions, outreach, spending, and commitments require explicit human approval |
| **Gateway/security** | Installed-schema validation; loopback-only Gateway; final audit 0 critical, 4 warnings, 2 informational findings — not zero risk |

### Rationale

Explicit allowlists and isolated delegation limit capability drift and
unnecessary context sharing. Fact-locking Career, confining Writer to its
workspace, removing runtime from Researcher, and making Broadcaster zero-tool
reduce the blast radius of mistakes. The partial Researcher result is recorded
instead of presumed complete. The local GPU boundary remains unchanged.

### Revisit Criteria

Revisit coordination only with a new guarded qualification for any changed
delegation path or tool grant, evidence that effective runtime policy still
matches configuration, and an observer note explaining residual risk. Any
expansion of external authority requires separate human approval.

## Related Documents

- [Architecture](architecture.md) — routing model and failure behavior
- [Qualification Protocol](qualification-protocol.md) — gate definitions and dispositions
- [Local-model Qualification](local-model-qualification.md) — exact test vectors and recorded results
- [Evidence and Limits](evidence.md) — what supports claims and what is excluded
- [Safety Controls](safety-controls.md) — stop conditions and containment rules
- [Multi-Agent Topology](multi-agent-topology.md) — route-admission and verification detail
- [Hardware Upgrade and Current State](hardware-upgrade-and-current-state.md) — exact platform chronology
