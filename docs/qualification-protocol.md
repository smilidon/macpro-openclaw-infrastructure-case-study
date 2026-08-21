# Qualification Protocol

## Promotion Is Role-Specific

A model is not "good" in the abstract. This project admits a route only to a
defined role, tool boundary, and workload after it passes the relevant gates.
That discipline turns model selection from guesswork into an auditable
engineering decision. A short successful response does not authorize general
agent use.

## Qualification Conditions

| Condition | Requirement |
|-----------|-------------|
| **Route integrity** | Pin the exact requested provider and model; disable silent fallback during qualification |
| **Session hygiene** | Use a fresh isolated session, fictional or non-sensitive inputs, and a short initial request |
| **Scope control** | Increase context, tools, continuation, and delegation only after the smaller gate passes |
| **Evidence boundary** | Record private operational evidence safely; publish only a sanitized, honest summary |

## Gate Sequence

| Gate | What it checks | Required outcome |
|------|----------------|------------------|
| **1. Structure** | Exact structured output and repair behavior | Valid output with no invented repair |
| **2. Retrieval** | Recovery of a planted supplied fact | Exact target recovered without substitution |
| **3. Reasoning and refusal** | Correct bounded reasoning plus an explicit refusal constraint | Both requirements satisfied |
| **4. Tool schema** | Native schema-conformant calls where tools are allowed | Correct method and required arguments |
| **5. Effective enforcement** | Actual compiled child surface and host authorization, not configuration text alone | Required tools remain; denied tools are absent or blocked |
| **6. Continuation and delegation** | Multi-turn compatibility, target workspace bootstrap, depth, and supervision | Correct handoff with no unauthorized delegation or context exposure |
| **7. Operational behavior** | Resource signals, fallback behavior, factual controls, and negative external-action tests | No stop condition, fabricated fact, unauthorized action, or host instability |

Failure halts the ladder for that route and role. Context and complexity are not
increased to manufacture a pass.

## Enforcement Tests

- A workspace-only policy must prove an allowed operation inside the workspace
  and denial outside it before any outside content is disclosed.
- A child-agent test must inspect the tools actually exposed to the child.
  Configured policy alone is insufficient when inheritance can strip or add a
  surface.
- Career tests use fictional facts and reject unsupported biographical details,
  dates, skills, metrics, credentials, and achievements.
- Broadcaster and other draft-only roles must prove they cannot send or publish.
- Vision, speech generation, and transcription are tested only through their
  proper image, speech, and audio surfaces.
- Local hardware tests retain thermal, kernel-log, device-selection, process,
  timeout, and cleanup checks in addition to semantic gates.

## Dispositions

Deterministic failures are recorded once rather than retried repeatedly.

| Disposition | Meaning |
|-------------|---------|
| **Admit** | Allow only the tested role and boundary |
| **Partial** | A useful subset passed; record the missing capability explicitly |
| **Narrow** | Retain a smaller explicit use case with no implied fallback |
| **Quarantine** | Block automatic routing pending separately approved requalification |
| **Exclude** | The route cannot meet a useful, safe role |

## Recording Requirements

Each result records:

1. Requested and actual provider/model, reasoning setting, and fallback behavior
2. Sanitized runtime, build, and model version information
3. Test-input description and role being qualified
4. Pass, partial, or failure outcome for each gate
5. Effective tools and any actual tool calls
6. Usage, latency, stop reason, and error class where exposed
7. Relevant hardware or service observation window
8. Explicit disposition and remaining uncertainty

This is what makes the case study valuable: capabilities are demonstrated,
limitations remain visible, and architectural promotion follows evidence rather
than enthusiasm.

## Related Documents

- [Decision Record](decision-record.md) — infrastructure decisions and rationale
- [Safety Controls](safety-controls.md) — stop conditions and containment
- [Local-model Qualification](local-model-qualification.md) — exact D700 test vectors and scores
- [Evidence and Limits](evidence.md) — bounded results and provenance
- [Multi-Agent Topology](multi-agent-topology.md) — effective route and delegation gates
