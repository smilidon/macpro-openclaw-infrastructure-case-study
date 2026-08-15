# Safety Controls and Fault Containment

This project treats containment as an architecture feature, not an emergency
afterthought. Hardware tests, model qualification, delegation, filesystem
access, and external actions each have an explicit stop boundary.

## Local Hardware Controls

Guarded local tests use a conservative operating envelope:

- **One loaded model** and **one concurrent request**
- **Non-display-GPU targeting** where applicable
- **Active thermal monitoring** with 76 C GPU and 82 C CPU watchdog stops
- **Kernel-log observation** before and after each bounded run
- Explicit timeout, device selection, process cleanup, and model-residency
  checks

Dynamic fan control and the hardware watchdog are safety controls, not
performance tuning. The objective is simple: make an unsafe run stop visibly
before it becomes a routine routing decision.

## Hardware and Qualification Stop Conditions

Any of the following ends a run and blocks promotion:

- GPU device loss, ring timeout, reset, lost VRAM, or parser failure
- Thermal watchdog intervention or fan-control failure
- Unexpected host instability, swap pressure, timeout, or process termination
- Invalid structure, missed retrieval target, unsupported fact, unsafe refusal,
  or non-conformant tool call
- A requested route resolving to the wrong model or silently using a fallback
- A deterministic compatibility, authorization, quota, or request-size failure

**Temperature is only one signal.** A cool run that resets a GPU is still a
failed run. A successful process that fails its semantic gate is runtime
evidence, not agent qualification.

## Multi-Agent Containment

| Boundary | Control |
|----------|---------|
| **Delegation** | Main and Career use explicit allowlists, bounded depth, isolated context by default, and concise task briefs |
| **Career truth** | Verified facts outrank drafts and research; applications, employer contact, publishing, and commitments require human approval |
| **Writer** | Workspace-only file access was tested deterministically: inside allowed, outside denied before disclosure |
| **Researcher** | Runtime and write tools are denied; qualification inspects the actual child surface rather than trusting configuration text |
| **Coder** | Workspace-only coding/runtime tools, no elevation, web, messaging, Gateway administration, scheduling, nodes, or media tools |
| **Broadcaster** | Zero tools; prepares drafts and cannot send or publish |
| **Vision, TTS, Transcriber** | Tested only through the appropriate image, speech-generation, or transcription surface |
| **Local offline lane** | Explicit, zero-tool, operator-reviewed, and never an automatic fallback |

These controls demonstrate practical least-privilege engineering: capability is
split by role, and passing one lane never grants authority in another.

## Change Safety and Recovery

Configuration repair followed a reversible sequence:

1. Record preimage hashes and create timestamped backups.
2. Validate agent identities and exact target paths.
3. Run the installed-schema dry run.
4. Apply only the approved operations.
5. Validate before any restart.
6. Confirm hot reload, Gateway health, and effective runtime policy.
7. Run the deep security audit and bounded independent smoke tests.
8. Preserve rollback artifacts and stop rather than beginning an unapproved
   second repair cycle.

The tested Gateway remained loopback-only. The final audit reported 0 critical
findings, 4 warnings, and 2 informational findings. That is a meaningful
security result, not a claim of zero risk. A validation failure, critical audit
finding, ineffective policy, unhealthy Gateway, unexpected external action, or
required unapproved restart is a hard stop.

## Public Evidence Boundary

Public documentation keeps the engineering decisions, sanitized test vectors,
results, and limitations while excluding credentials, private configuration,
session transcripts, host paths, and recovery-sensitive details. Evidence is
useful only when publishing it does not weaken the system it describes.

A Vulkan-enabled build or visible access to both GPUs is not qualification by
itself. Promotion still requires the runner, model identity, device selection,
thermal and kernel observation, cleanup, semantic scores, and explicit
disposition documented by the [Qualification Protocol](qualification-protocol.md).

## Related Documents

- [Qualification Protocol](qualification-protocol.md) — gate sequence and promotion criteria
- [Decision Record](decision-record.md) — infrastructure decisions and rationale
- [Known Issues](known-issues.md) — open evidence gaps and non-goals
- [System Profile](system-profile.md) — hardware and workload constraints
- [Evidence and Limits](evidence.md) — bounded public support
