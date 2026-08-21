# Known Issues and Open Work

## Proven Boundary, Unresolved Root Cause

Guarded local-inference work established a defensible routing boundary on this
Mac Pro: bounded single-turn Vulkan execution can complete, but semantic
usefulness and interactive stability do not support automatic agent routing.
The evidence is sufficient for that architecture decision; it is not sufficient
to name one driver, firmware, runtime, or hardware root cause.

## Completed Engineering Outcomes

The public case study now includes:

- A reproducible [single-turn Vulkan smoke](../evidence/vulkan-single-turn-smoke-2026-08-14.md)
  on each D700, with exact host/runtime vector and explicit limitations
- Strict usefulness records for
  [TinyLlama](../evidence/vulkan-usefulness-suite-2026-08-14.md) and
  [`thumbo-safe`](../evidence/thumbo-safe-vulkan-usefulness-2026-08-14.md)
- Sanitized environment, selection, and D700 requalification evidence
- An installed-schema-valid multi-agent repair with a final deep audit of 0
  critical findings
- Deterministic Writer workspace enforcement and a working direct Coder tool
  path
- Corrected Career delegation, Researcher runtime isolation, Broadcaster
  zero-tool enforcement, and proper-modality Vision, speech, and transcription
  tests

Those are substantive infrastructure results: the project did not merely find
problems; it converted them into enforced operating boundaries and repeatable
verification.

### 2026-08-20 dated outcomes

- The official 64 GB kit removed the prior capacity block for a guarded
  Qwen2.5-Coder-32B Q4_K_M load; the model remained not useful at 0.3 generated
  token/s and did not complete its practical suite.
- Three smaller Qwen Q4_K_M artifacts completed exact sentinels and bounded 4K
  benchmarks; all failed their complete speed gates, so no conditional
  interactive-usefulness suite ran and no quality score is inferred for that
  comparison.
- Qwen3.5-4B later passed a separate frozen short-task suite 5/5. This supports
  only explicit, manual, bounded supplied-text tasks with human review. It did
  not pass the earlier interactive speed gate and is not live, deployed, or an
  OpenClaw route.
- Completed post-upgrade measurements were safety-clean in their recorded
  envelopes. That does not prove the historic Vulkan root cause or attribute
  any behavior change to RAM.

## Local Vulkan Status

| Test area | Result | Disposition |
|-----------|--------|-------------|
| Single-turn runtime smoke | Completed independently on each D700 | Runtime evidence only |
| TinyLlama strict usefulness gates | **0/4** | Smoke fixture, not an agent route |
| `thumbo-safe` strict usefulness gates | **1/4** | Explicit bounded zero-tool text only |
| Qwen3.5-4B frozen short-task suite | **5/5**, including safety | Manual short supplied-text candidate only; not routed or deployed |
| Interactive/conversation behavior | Historical fault and timeout boundary remains | Unqualified |
| Automatic local fallback | Deliberately excluded | Hosted failures remain visible |

## Multi-Agent Remaining Limits

- **Researcher inheritance:** nested `web_search` and `web_fetch` worked, but
  the installed bridge stripped configured `browser` and `read`.
- **Security warnings:** 4 warnings and 2 informational findings remain. They
  concern deferred or accepted boundaries rather than hidden critical findings.
- **Broadcaster bootstrap:** essential AGENTS instructions inject fully, while
  trailing nonessential IDENTITY and HEARTBEAT content remains truncated.
- **Provider state:** model availability, latency, quota, and quality are dated
  operational facts and require current qualification.
- **Public provenance:** private sessions, configuration, logs, credentials,
  and recovery-sensitive material are intentionally absent from this pack.

## Intentional Tradeoffs

| Tradeoff | Rationale |
|----------|-----------|
| **No automatic local fallback** | A hosted outage remains observable instead of crossing a hardware-risk boundary |
| **No static live-model catalog** | Provider assignments age quickly; role fit and qualification are the durable design |
| **No raw configuration or recovery runbook** | Public evidence should not expose private host state or unsafe copy-and-paste operations |
| **Partial results remain visible** | An honest partial pass is more useful than a polished but unsupported claim |

## Next Useful Improvements

1. Add CI that runs `make test` on every documentation change.
2. Publish a sanitized machine-readable multi-agent test artifact from a
   separately approved bounded run.
3. Resolve or document the installed cross-agent browser/read inheritance
   behavior.
4. Address the remaining security warnings only through separately reviewed,
   reversible changes.

### Local-subsystem next steps

1. Do not promote Qwen3.5-4B beyond its admitted manual short-task role without
   a new role-specific qualification. Its 5/5 short-task pass does not satisfy
   the failed interactive speed gate.
2. Preserve pinned artifact, runner, build, guard, transcript, and manifest
   identities for any rerun; treat changes as a new evidence envelope.
3. Investigate the historic interactive fault only through separately approved
   guarded work; do not infer causation from the memory upgrade.
4. Keep packaging, provider registration, aliases, routing, bindings, and an
   effective-route test pending until separately approved; do not describe the
   candidate as deployed.

### Multi-agent next steps

1. Requalify any changed route, tool grant, or delegation path against the
   effective child surface, not configuration text alone.
2. Publish only a sanitized machine-readable enforcement result after review.
3. Keep the Researcher browser/read inheritance disposition partial until the
   missing effective capabilities pass a new test.

## Non-Goals

- Claiming a universal fix or benchmark for legacy AMD hardware
- Publishing credentials, private configuration, raw sessions, or operational
  recovery instructions
- Recreating a high-risk workload solely to obtain a public failure artifact
- Claiming production certification, zero risk, or external validation

See [Evidence and Limits](evidence.md) for the full provenance boundary and
[Safety Controls](safety-controls.md) for the enforced stop conditions.
