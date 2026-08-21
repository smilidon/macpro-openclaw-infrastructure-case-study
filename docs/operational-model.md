# Operational Model

Thumbo is a career-support OpenClaw agent hosted and orchestrated on the reused
Mac Pro. It assists with preparation, research, organization, and drafting
under human review. Hosted routes are intentional qualified components, while
the local Vulkan lane remains a separate bounded subsystem.

## Main: Direct Work and Explicit Delegation

Main answers simple general requests directly and coordinates substantial work.
Its delegation allowlist is limited to Career, Researcher, Writer, Coder,
Vision, and Broadcaster. Isolated child context is the default; concise briefs
carry the goal, constraints, verified facts, relevant excerpts or paths, and
acceptance checks without copying long conversations.

Main owns the final user-visible response. Specialist output is treated as a
draft or evidence: material claims, file changes, test results, and the actual
route are checked before completion is reported.

## Specialist Routes

| Role | Operating boundary | Observed behavior |
|------|--------------------|-------------------|
| **Career** | Persistent, fact-locked career context; delegates only to Researcher and Writer | Reviews delegated work against verified facts; submissions, outreach, publishing, and commitments require approval |
| **Researcher** | No runtime or write tools | Nested search and fetch succeeded; the installed bridge did not preserve configured browser or local-read access |
| **Writer** | Workspace-only `read`, `write`, `edit`, and `apply_patch` | An inside read was permitted and an outside read was denied before disclosure; no shell, web, messaging, or publishing surface |
| **Coder** | Direct from Main on the Sol/high route; workspace-only coding and bounded runtime tools | Create, read, edit, hash, delete, and absence verification passed without fallback |
| **Broadcaster** | Zero tools; outbound-copy preparation only | Preserved supplied facts and could not send or publish |
| **Vision** | Actual image input only | Harmless image description passed through the installed image surface |
| **TTS** | Speech-generation surface only | Generated a local test audio file without external delivery |
| **Transcriber** | Audio-transcription surface only | Correctly transcribed the bounded local test audio |

Search remains outside automatic delegation until its workspace and behavior
are separately qualified. Cheap, Utility, Gemma Utility, and Offline remain
bounded lanes rather than general specialists.

## Local Offline Lane

The local lane accepts only explicit supplied-text tasks such as summarizing,
rewriting, extraction, classification, and formatting.

- **Zero tools:** no commands, file writes, web access, messaging, or child
  agents.
- **No operational authority:** output is reviewed rather than acted upon.
- **Never automatic:** hosted-route failure cannot silently cross into local
  generation.

Qwen3.5-4B has separately qualified for five manual short-task types under one
exact 4K hybrid envelope: bounded arithmetic, exact retrieval, sentiment,
grounded one-sentence summary, and an authorization stop. That candidate is
not installed as the lane's OpenClaw model: current offline configuration
still uses `ollama/thumbo-safe:latest`, and Qwen packaging, provider/alias,
route/binding changes, and effective-route testing remain pending. Its 5/5
result therefore documents a candidate capability, not live routing.

## Failure and Fallback Boundaries

- A hosted failure is surfaced or routed to a qualified hosted alternative
  within the same role.
- Known quota, compatibility, request-size, and availability failures are not
  retried indefinitely.
- A specialist that loses required tools is reported as partially capable, not
  treated as a full pass.
- No draft, lookup, or model result grants authority to send, publish, apply,
  contact, spend, or commit externally.
- The operator chooses whether to retry, defer, or select another qualified
  route.

That restraint is the reliability feature: the system gives up capability
openly instead of quietly exchanging a known boundary for an unknown one.

## Model Identity and Deployment Scope

Static model names and provider availability are dated. The stable design
principle is **role fit plus live qualification**, backed by cross-provider
fallbacks where a role requires them.

The tested Gateway was loopback-only. Installed-schema validation passed, and
the final deep audit reported 0 critical findings, 4 warnings, and 2
informational findings. This is a bounded, operator-supervised deployment—not
production certification or a zero-risk claim.

## Related Documents

- [Architecture](architecture.md) — routing model and failure behavior
- [Decision Record](decision-record.md) — infrastructure decisions and rationale
- [Safety Controls](safety-controls.md) — stop conditions and fault containment
- [Evidence and Limits](evidence.md) — bounded results and provenance limits
- [Multi-Agent Topology](multi-agent-topology.md) — route gates, data boundaries, and enforcement tests
- [Qwen3.5-4B Short-Task Qualification](../evidence/qwen35-4b-short-task-qualification-2026-08-20.md) — manual candidate boundary and non-deployment state
