# Operations History and Reliability Record

This is the public, sanitized operational record for the Thumbo OpenClaw case study. It records material upgrades, incidents, mitigations, verification boundaries, and open limits without publishing credentials, private hostnames, account data, raw sessions, private paths, or deployment-control details.

## Public source-of-truth policy

This repository is the sole source of truth for **publicly shareable** project history and current-state claims. Changes to public claims must be made here, reviewed in Git history, and reflected in the changelog.

Private configuration, credentials, backups, customer/work-product data, raw session records, and security-sensitive recovery runbooks remain private by design. They are not superseded by this repository and must never be copied here.

## Timeline

| Date | Milestone | Public outcome |
| --- | --- | --- |
| 2026-08-01 | Session and safety-guard incident | Separated stale runtime binding and failed input scanning from OAuth diagnosis; disabled the failing closed guard; validated a fresh hosted smoke session. |
| 2026-08-07 | Remote-access reliability repair | Retired an unsafe Wi-Fi recovery loop and prevented unattended host sleep. Network recovery was left to the platform connection manager. |
| 2026-08-11 to 2026-08-20 | Hardware recovery and qualification | Restored dual-GPU enumeration, upgraded system memory to 64 GB, and ran bounded local-model qualification. Local generation remained excluded from automatic routing. |
| 2026-09-02 | OpenClaw 2026.8.2 update recovery | Reconciled configuration-schema changes, stale model entries, plugin consent, legacy session migration, and a stale HTTPS route. The gateway returned to a verified healthy state. |
| 2026-09-06 | Latency investigation and mitigation | Identified dashboard Codex catalog scans, then isolated model-catalog event-loop starvation during prompt preparation. A reversible local hotfix reduced the observed cold preparation delay; residual cold-start cost remains. |
| 2026-09-08 | Public operating record refresh | Updated the public case study to make this repository the canonical public record of progress, limits, and operating claims. |

## 1. Session and input-scanning incident — 2026-08-01

### What happened

A stale session binding was presented as an OAuth problem. In the same period, a custom prompt-injection guard failed closed when its classifier was unavailable, uncertain, or asked to scan oversized input. Ordinary owner-authored messages could therefore be treated as attacks.

### Corrective actions

- Disabled the failing guard rather than continuing to misclassify infrastructure faults as user behavior.
- Validated the configuration and restarted the gateway.
- Confirmed a fresh hosted-model smoke test and Codex harness path worked.
- Preserved existing conversations; affected users were directed to begin a fresh session rather than reuse the retired binding.

### Lasting lesson

Security controls must distinguish an actual detection from a scan failure, uncertainty, authentication issue, or input-size limit. A stale runtime binding is not an OAuth failure.

## 2. Remote-access reliability repair — 2026-08-07

### What happened

An aggressive user-level Wi-Fi watchdog tried to reset the only active network interface after external probe failures. That behavior could interrupt the remote connection used to administer the host. Separately, unattended sleep made the host unreachable.

### Corrective actions

- Disabled the active watchdog while retaining it on disk for reversible review.
- Prevented unattended sleep through a persistent inhibitor and the system sleep controls.
- Left normal reconnection to the operating system's network manager.

### Verification boundary

The repair verified the sleep controls and the then-active connection. It did not claim to make the underlying Wi-Fi hardware or driver universally reliable; wired networking remains the preferred physical reliability improvement.

## 3. Hardware recovery and bounded local inference — August 2026

The host's second D700 GPU had stopped binding after a kernel-argument change. The prior safe power-management argument was restored across boot entries and the system was requalified conservatively. The later 64 GB memory upgrade improved what could be loaded, but it did not erase historical Vulkan stability limits.

The standing boundary remains unchanged:

- keep one local model resident and one inference request active at a time;
- use local models only for explicit, bounded, zero-tool text work;
- require qualification evidence before any route change;
- do not use a local model as an automatic fallback for consequential, external, credential, or command-authorizing work.

See [Local-model Qualification](local-model-qualification.md) and the dated records under [evidence](../evidence/README.md).

## 4. OpenClaw 2026.8.2 update recovery — 2026-09-02

### What happened

The package update completed, but post-update validation and gateway startup failed. The recovery exposed a layered migration problem rather than a failed package replacement:

- retired configuration fields and model aliases;
- required explicit multi-agent ownership;
- a large shared SQLite state store with stale planner statistics;
- new plugin capability-consent requirements;
- a legacy session-store migration; and
- a stale HTTPS handler whose ownership had to be verified before removal.

### Corrective actions

The operator took backups before state work, verified database integrity, rebuilt SQLite planner statistics, handled session migration through the supported repair path, reviewed and accepted only the already-configured plugin capabilities, removed only the verified stale route, and confirmed gateway health afterward.

### Lasting lesson

Treat update failure as a sequence of independently verifiable gates. Confirm the installed version separately from the updater result, preserve state before maintenance, and do not remove routes or accept plugin capabilities without proving their ownership and scope.

## 5. Extreme latency investigation and mitigation — 2026-09-06

### Confirmed symptoms

The browser UI and ordinary requests could pause for tens of seconds. Paired local and remote checks showed periods in which the gateway itself stalled, independent of the remote streaming connection. The host was not under sustained CPU, memory, swap, or disk pressure during the relevant samples.

### First confirmed contributor: native Codex session catalog

Dashboard catalog refreshes were enumerating many local Codex threads sequentially. Disabling native Codex session discovery stopped that recurring catalog workload while preserving normal hosted-model and Codex harness use. This was a targeted improvement, not a complete latency fix.

### Root cause isolated for the remaining major stall

A main-thread CPU capture attributed the dominant slow-turn work to model-catalog evaluation: provider-runtime comparison, configuration hashing, and runtime-policy evaluation over a large configured model list. The earlier stage timing had reported this as bootstrap delay because the event loop was monopolized before the next stage could proceed.

### Reversible local hotfix

A small, locally installed patch was validated against real selections and synthetic precedence cases before rollout. It:

- skips model entries that have no runtime policy before expensive matching;
- takes a safe positive shortcut for identical or structurally equal provider configuration objects; and
- yields between bounded batches of synchronous model-entry evaluation.

The patch preserves model choices, aliases, credential semantics, and runtime-policy behavior. It is version-specific and may be overwritten by a future OpenClaw update; the original files and a guarded rollback remain private.

### Observed result and limits

In matched fresh-session tests, cold prompt preparation fell from about 36 seconds to about 20 seconds, while bootstrap timing fell from about 33 seconds to about 17 seconds. Subsequent warm tests no longer reproduced the prior roughly 30-second preparation stall. These are host-specific observations, not a claim that all latency was eliminated or that upstream OpenClaw contains the same fix.

Cold-start overhead remains material, intermittent client-side rendering concerns were not fully localized, and future updates require regression verification.

## Current public operating state — 2026-09-08

- OpenClaw gateway: version `2026.9.2`, active and reachable on its loopback service endpoint.
- Main route: `openai/gpt-5.6-terra`; other specialist routes remain governed by their explicit tool and approval boundaries.
- Agent fleet: 18 configured agents.
- Main and specialist heartbeats: disabled, avoiding background lane contention.
- Telemetry: disabled.
- Codex native session catalog: disabled; the normal Codex harness remains available.
- Local/offline lane: still bounded, opt-in, and excluded from automatic fallback.

This is an operational snapshot, not a security certification, availability guarantee, or performance promise. For the durable architecture and safety boundaries, see [Architecture](architecture.md), [Safety Controls](safety-controls.md), and [Known Issues](known-issues.md).

## What is next

1. Re-test the latency mitigation after every OpenClaw update and remove the local patch if an upstream release supplies an equivalent verified fix.
2. Measure cold-start versus warm-turn behavior separately, including browser rendering and remote-client metrics where appropriate.
3. Keep public claims evidence-backed, dated, and explicit about what remains unresolved.
