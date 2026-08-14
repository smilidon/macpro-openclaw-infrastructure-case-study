# Decision Record: Local Inference Boundary and Multi-Agent Coordination

> **Status:** Accepted — these boundaries stand until new guarded qualification
> runs produce revised evidence.

## Context

- **Platform:** 2013 Mac Pro 6,1, dual AMD FirePro D700 GPUs (6 GiB VRAM
  each), 32 GiB RAM, Nobara Linux
- **Workload:** OpenClaw agent runtime — long contexts, structured output, tool
  use, delegation, and sustained inference
- **Local-inference problem:** guarded Vulkan-offload experiments triggered
  AMDGPU ring-timeout and device-loss failures under agent-style pressure.
  Failures occurred below thermal stop thresholds, so temperature alone was
  not an acceptance signal.
- **Coordination problem:** a general assistant needs specialist capability
  without granting every model the same context, tools, or external authority.
- **Claim boundary:** this record does not name a single hardware root cause,
  generalize to all AMD systems, or certify the deployment as risk-free.

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
| **External actions** | Sending, publishing, applications, employer contact, spending, and commitments require explicit human approval |
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
