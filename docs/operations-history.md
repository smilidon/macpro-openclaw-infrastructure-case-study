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
| 2026-09-12 | OpenClaw 2026.9.4 update-rollback recovery | Restored unambiguous package-manager ownership, corrected a schema-identifier-quoting artifact, and brought the runtime forward to match already-migrated state rather than forcing state backward. Gateway returned to a verified healthy state. |
| 2026-09-12 | Stale legacy install shim after ownership repair | A leftover global-install shim from before package-manager ownership was corrected kept resolving to the superseded build. CLI commands intermittently ran the wrong version until the shim was repointed at the current, correctly-owned install. |
| 2026-09-24 | Backup consolidation and external verification | Consolidated ~81 GB of local backup artifacts to a single verified 4.2 GB tar.zst + sha256 on external flash drive; removed all but two local sqlite snapshots. Freed ~74 GB on root filesystem. |

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

## 6. OpenClaw 2026.9.4 update-rollback and forward-migration recovery — 2026-09-12

### What happened

An update attempt from `2026.9.2` toward the current release stalled in two stages. A pre-update ownership check first refused to touch the install at all, because it could not confirm which package manager owned it: an earlier environment change had left the install running from a location its active package manager no longer recognized as its own. Once ownership was restored and the update was retried, it progressed further before a post-update state-schema check failed, and the updater rolled the package back to `2026.9.2` to avoid running an unverified build. That rollback left the shared state database already advanced past what the rolled-back code understood, so the gateway could not start cleanly under either version.

### Corrective actions

The operator re-established unambiguous package-manager ownership for the install rather than leaving two competing install locations in place, confirmed by read-only inspection that every affected schema object held zero rows before any diagnostic step touched it, and — cross-checked against an independent public report of the identical failure mode (see [openclaw/openclaw#142770](https://github.com/openclaw/openclaw/issues/142770)) — determined the correct recovery direction was forward, not backward: bring the runtime up to the release the database had already migrated toward, rather than force the database back to match the older, rolled-back code. A minor identifier-quoting side effect introduced by an earlier diagnostic table rename was also found and corrected before the schema was accepted as canonical. The gateway was confirmed healthy, with every agent's session store intact, once the matching release was in place.

### Lasting lesson

A failed update's rollback can restore code that is now older than the state it must read. Diagnose which side — the runtime or the persisted state — has actually fallen behind before choosing a recovery direction. Forcing state backward to match stale code can undo real, already-applied progress even when, as here, no user data is actually lost.

## 7. Stale legacy install shim resolved to the superseded build — 2026-09-12

### What happened

Restoring unambiguous package-manager ownership (entry 6, above) moved the active install to the package manager's own managed location. A second, older global-install location from before that arrangement was established still held a command shim from an earlier install, and that shim was never updated by the ownership repair, since it belonged to a different, no-longer-active install path. Because both locations were present on the command search path, and their relative order was not always consistent between shells, commands could intermittently run through the stale shim instead of the current install.

This stayed invisible for ordinary commands, which do not depend on the exact build. It surfaced once the shared state schema advanced (entry 6) past what the stale build understood: the stale build's own safety check correctly refused to proceed rather than risk the newer state, but the resulting message pointed only at the version mismatch, not at the underlying duplicate-install cause.

### Corrective actions

The operator repointed the stale shim directly at the current, correctly-owned install, rather than continuing to depend on consistent command-search-path ordering between the two locations. Confirmed the fix in a fresh shell: the affected commands now resolve to the current build and complete normally regardless of ordering.

### Lasting lesson

A package-manager ownership repair fixes the *active* install location; it does not retire a shim left behind by a prior, now-superseded install at a different location. When more than one install location can appear on the command search path, treat resolving them to the same target as part of the repair, not a follow-up -- the safety check that later refuses to run is a symptom, not the fault.

## 8. Backup consolidation and external verification — 2026-09-24

### What happened

Local backup directory had accumulated ~81 GB of artifacts across multiple recovery and diagnostic operations, leaving the root filesystem with 1.8 GB free. A fresh authoritative backup was created directly to an external flash drive (SanDisk 233 GB exFAT, labeled `EMERGENCY`) using tar.zst with sha256 sidecar — the same method as the prior verified backup. The backup was fully verified by complete decompression (275,476 entries) and spot-checked for key state files.

### Corrective actions

- Created `openclaw-full-2026-09-24.tar.zst` (4.2 GB) and `openclaw-full-2026-09-24.tar.zst.sha256` on the external drive.
- Verified integrity via full decompression and content spot-check (openclaw.json, state/openclaw.sqlite, all agents, 11,686 workspace entries).
- Removed all local backup artifacts except the two most recent sqlite snapshots (2026-09-02).
- Freed ~74 GB on /home (1.8 GB → 82 GB free).

### Verification boundary

The external backup is the single authoritative recovery artifact. Local sqlite snapshots are retained for quick rollback of agent state only. No credentials, private paths, or raw session data were exposed in this record.

## Current public operating state — 2026-09-24

- OpenClaw gateway: version `2026.9.4`, active and reachable on its loopback service endpoint. Update to `2026.9.5` available.
- Main route: `openai/gpt-5.6-terra`; other specialist routes remain governed by their explicit tool and approval boundaries.
- Agent fleet: 21 configured agents.
- Main and specialist heartbeats: disabled, avoiding background lane contention.
- Telemetry: disabled.
- Codex native session catalog: disabled; the normal Codex harness remains available.
- Local/offline lane: still bounded, opt-in, and excluded from automatic fallback.
- Backups: authoritative full backup on external flash drive (2026-09-24), local sqlite snapshots (2).

This is an operational snapshot, not a security certification, availability guarantee, or performance promise. For the durable architecture and safety boundaries, see [Architecture](architecture.md), [Safety Controls](safety-controls.md), and [Known Issues](known-issues.md).

## What is next

1. Apply the available `2026.9.5` update and re-test the latency mitigation; remove the local patch if an upstream release supplies an equivalent verified fix.
2. Measure cold-start versus warm-turn behavior separately, including browser rendering and remote-client metrics where appropriate.
3. Keep public claims evidence-backed, dated, and explicit about what remains unresolved.
