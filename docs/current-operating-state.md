# Current Operating State

**Last reviewed:** 2026-09-08  
**Public record status:** current, sanitized operational snapshot

## Purpose

This page is the current public reference for the case-study deployment. Historical claims belong in [Operations History](operations-history.md); releases and public-document changes belong in the [Change Log](../CHANGELOG.md).

## Active boundaries

| Area | Current public state |
| --- | --- |
| Gateway | OpenClaw `2026.9.2`; active loopback service; telemetry disabled. |
| Main orchestration | Hosted main route with explicit specialist delegation and human approval for consequential or external action. |
| Agent fleet | 18 configured agents with separate role and tool boundaries. |
| Background activity | Main and specialist heartbeats are disabled. |
| Codex integration | Normal harness available; native session catalog disabled to avoid dashboard-driven catalog enumeration overhead. |
| Local inference | Opt-in only, one model and one request at a time, zero-tool bounded text work only; never an automatic fallback. |
| Public documentation | This repository is the source of truth for public claims, decisions, evidence boundaries, and current-state summaries. |

## Performance posture

A September 2026 investigation confirmed gateway-wide event-loop stalls during prompt preparation. The two verified mitigations were disabling native Codex session discovery and applying a reversible, version-specific local model-catalog hotfix. Matched cold-session tests improved substantially, but significant cold-start cost remains and the work must be rechecked after upgrades.

See [Operations History](operations-history.md#5-extreme-latency-investigation-and-mitigation--2026-09-06) for scope, measurements, and limitations.

## Public-data boundary

The repository deliberately excludes secrets, private configuration, host and network identifiers, raw session data, private operational paths, backups, and recovery-control details. Public documentation must describe outcomes and verification boundaries without making those materials discoverable.
