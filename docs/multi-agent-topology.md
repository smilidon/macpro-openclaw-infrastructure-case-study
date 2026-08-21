# Multi-Agent Topology and Enforcement

## Purpose and Trust Model

Thumbo is hosted on the reused Mac Pro and supports human-approved career work.
Main coordinates specialists, verifies their results, and owns the final
user-visible response. Specialist output is evidence or a draft—not authority
to publish, send, submit, spend, commit, or act externally.

The documented topology is intentionally least-privileged. Role membership,
tool access, delegation depth, data source, route identity, and external action
are separate gates.

## Specialist Route Table

| Route | Intended capability | Effective boundary | Delegation boundary | Verified or partial disposition |
|---|---|---|---|---|
| Main | Coordination, direct simple work, final verification | Reviews route, claims, file changes, and tests | Career, Researcher, Writer, Coder, Vision, Broadcaster only | Verified coordinator boundary |
| Career | Durable, fact-locked career context | Supplied verified facts outrank drafts and references; no autonomous external action | Researcher and Writer only | Fictional fact-lock and nested delegation passed |
| Researcher | Sourced retrieval | No runtime or write tools | No broader delegation documented | **Partial:** nested search/fetch worked; configured browser/read did not survive the installed bridge |
| Writer | Prose, structure, and editing | Workspace-only read/write/edit/apply-patch; no runtime, web, messaging, or publishing | None documented | Inside-workspace allow and outside-workspace deny passed |
| Coder | Software and infrastructure work | Workspace-only coding and bounded runtime tools; no elevation, messaging, Gateway administration, scheduling, nodes, or media | Direct from Main | Intended Sol/high route and file-operation probe passed without fallback |
| Broadcaster | Outbound-copy preparation | Zero tools; drafts only | None | Fact preservation passed; no send/publish surface |
| Vision | Image interpretation | Proper image-input surface only | None | Harmless image check passed |
| TTS | Local speech generation | Speech-generation surface only | None | Bounded local generation passed without delivery |
| Transcriber | Audio transcription | Audio-input surface only | None | Bounded local transcription passed |
| Local offline lane | Explicit supplied-text experiment | Zero tools; no commands, decisions, child agents, or automatic fallback | None | Current OpenClaw lane still uses `ollama/thumbo-safe:latest`; Qwen3.5-4B has a separate manual 5/5 short-task qualification but is not routed or deployed |

## Capability-Boundary Table

| Capability | Main | Career | Researcher | Writer | Coder | Broadcaster | Local lane |
|---|---:|---:|---:|---:|---:|---:|---:|
| Final response ownership | Yes | No | No | No | No | No | No |
| Fact-locked career context | Review | Yes | Supplied subset | Supplied subset | No | Supplied subset | Supplied text only |
| Web/reference retrieval | Route-specific | Via Researcher | Search/fetch verified; browser partial | No | No public grant | No | No |
| Workspace mutation | Review/coordinate | No public grant | No | Writer workspace only | Coder workspace only | No | No |
| Runtime execution | Route-specific | No public grant | No | No | Bounded workspace runtime | No | No |
| External action | Human approval required | No autonomous action | No | No | No | No | No |
| Automatic fallback to local | No | No | No | No | No | No | Not applicable |

## Route-Admission Gates

A role is admitted only when all required gates pass for that exact route:

1. **Identity:** requested and actual route/model match; qualification disables
   silent fallback.
2. **Role fit:** the task belongs to the specialist's documented purpose.
3. **Effective tools:** the child receives required tools and denied tools are
   absent or blocked in practice.
4. **Data boundary:** only the minimum supplied facts or approved references
   enter the child context.
5. **Delegation:** the target is allowlisted and within depth; isolated context
   and a concise task brief are the default.
6. **Semantic result:** literal criteria pass without fabricated facts,
   unsupported repair, or a missed refusal boundary.
7. **Operational result:** no fallback drift, authorization failure, host stop,
   or unapproved external action occurs.

Failure produces a visible disposition—partial, narrow, quarantine, or
exclude—rather than a hidden capability substitution.

## Enforcement Tests

- Main-to-Coder completed on the intended route with workspace-only file
  create/read/edit/hash/delete/absence checks and no fallback.
- Writer's deterministic host-policy probe allowed an in-workspace read and
  denied an outside read before content disclosure.
- Researcher's effective nested child surface exposed search/fetch but not the
  configured browser/read tools. This remains partial rather than being called
  a full pass.
- Career fictional ranking and nested delegation preserved supplied facts and
  did not authorize external action.
- Broadcaster preserved supplied facts with no tool surface.
- Vision, speech generation, and transcription were tested only through their
  proper modality surfaces.

These are bounded operator-verified tests. The public pack does not contain raw
sessions, live configuration, credentials, private paths, or recovery actions.

## First-Party Data and External-Reference Safety

First-party supplied facts are authoritative for personal claims. External
references may add sourced context, but they cannot overwrite a supplied fact,
invent a biographical claim, or grant permission to act. Research returns its
sources and uncertainty; Main or Career reconciles them against the fact lock
before Writer or Broadcaster receives a brief.

Only the minimum necessary excerpt crosses a delegation boundary. Private
career materials and operational context remain outside public evidence and
outside unrelated specialists. A public reference is not treated as permission
to contact, submit, publish, or disclose.

## Failure and Fallback Boundaries

- Hosted route failure is surfaced or sent to a separately qualified hosted
  alternative in the same role. It never triggers automatic local inference.
- Loss of a required child tool is a partial capability, not a successful pass.
- Local failure stops the task; it cannot generate commands, recovery steps, or
  operational decisions.
- Deterministic compatibility, authorization, quota, request-size, and route
  identity failures are not retried indefinitely.
- Human approval remains required for every consequential external action.

## Gateway Scope and Remaining Limits

The tested OpenClaw/Gateway version was `2026.7.1-2`. Installed-schema
validation passed, the Gateway remained loopback-only, and the final deep audit
reported 0 critical findings, 4 warnings, and 2 informational findings. This is
a dated single-host observation, not zero-risk status or external validation.

Remaining limits include Researcher browser/read inheritance, the retained
warnings, partial trailing Broadcaster bootstrap truncation, dated hosted-route
availability, and the lack of a sanitized machine-readable multi-agent raw
artifact. Any changed route, tool grant, or delegation path requires a new
effective-surface qualification.

## Related Documents

- [Architecture](architecture.md)
- [Operational Model](operational-model.md)
- [Qualification Protocol](qualification-protocol.md)
- [Safety Controls](safety-controls.md)
- [Evidence and Limits](evidence.md)
