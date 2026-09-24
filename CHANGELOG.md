# Change Log

## 2026-09-24 — Backup consolidation, external verification, and pending 2026.9.5 update

### Added

- Recorded a dated [operations-history entry](docs/operations-history.md#8-backup-consolidation-and-external-verification--2026-09-24) for the consolidation of ~81 GB of local backup artifacts to a single verified 4.2 GB tar.zst + sha256 on external flash drive, freeing ~74 GB on the root filesystem.
- Updated [current operating state](docs/current-operating-state.md) to reflect authoritative backup on external media, freed disk space, and available update to `2026.9.5`.
- Bumped recorded gateway version to `2026.9.4` (pending `2026.9.5`).

### Verified boundaries

- External backup fully verified by complete decompression (275,476 entries) and spot-check of key state files.
- No credentials, private configuration, host/network identifiers, raw sessions, or private paths exposed.
- Local sqlite snapshots retained (2 most recent) for quick agent-state rollback only.

## 2026-09-12 — Stale legacy install shim resolved to the superseded build

### Added

- Recorded a dated [operations-history entry](docs/operations-history.md#7-stale-legacy-install-shim-resolved-to-the-superseded-build--2026-09-12) for a follow-on incident to the 2026.9.4 recovery above: a leftover shim from a superseded global-install location kept resolving to the older build after ownership was corrected, until repointed directly at the current install.

### Verified boundaries

- No state, config, or history was affected; this was a command-resolution issue only.
- Framed the lesson generally (any setup with more than one possible global-install location on the command search path), not as an nvm- or npm-specific detail, consistent with this repository's existing abstraction level.

## 2026-09-12 — OpenClaw 2026.9.4 update-rollback recovery

### Added

- Recorded a dated [operations-history entry](docs/operations-history.md#6-openclaw-20269-4-update-rollback-and-forward-migration-recovery--2026-09-12) for the `2026.9.2` → `2026.9.4` update failure and recovery.
- Added an [Update reliability](docs/current-operating-state.md#update-reliability) note and bumped the recorded gateway version to `2026.9.4`.

### Verified boundaries

- Confirmed no user data was at risk before any schema-affecting diagnostic step; the only schema objects touched held zero rows.
- Preserved the distinction between the fix and the root-cause finding: the recovery *direction* (forward, not backward) was itself the material result, not just the version bump.
- Excluded exact file paths, commands, and table/column-level detail from the public record, consistent with this repository's existing exposure boundary.

## 2026-09-08 — Public operations history and current-state record

### Added

- Established this repository as the source of truth for publicly shareable Thumbo project claims.
- Added a dated, sanitized [operations history](docs/operations-history.md) covering the session-guard incident, remote-access repair, hardware qualification, 2026.8.2 upgrade recovery, and latency investigation.
- Added a [current operating state](docs/current-operating-state.md) page with explicit performance and privacy boundaries.

### Verified boundaries

- Preserved the distinction between confirmed mitigations and unresolved limits.
- Excluded credentials, private configuration, host/network identifiers, raw sessions, private paths, backups, and recovery-control details.
- Documented the local latency mitigation as version-specific and reversible rather than as an upstream or permanent fix.

## 2026-08-20 — Final documentation voice and verification pass

### Refined

- Completed a prose-only voice pass on the README while preserving all
  technical facts, numeric values, links, code, tables, and qualification and
  deployment boundaries.
- Kept successful reuse of the 2013 Mac Pro as the central framing for the
  sanitized multi-agent topology, exact hardware chronology, and post-upgrade
  evidence.

### Verified

- Applied the preservation-first policy: every preexisting public path remains,
  and the retained raw JSON, runners, scripts, tests, and profile asset were
  left unchanged.
- Passed documentation-link, public-artifact, exposure, privacy,
  prohibited-claim, layout, diff, and path-preservation checks.

## 2026-08-20 — Qwen3.5-4B bounded short-task admission

### Added

- Added a sanitized Qwen3.5-4B Q4_K_M qualification record with pinned model
  and runtime hashes, the frozen five-case suite, exact hybrid envelope,
  timing aggregates, safety extrema, chronology, source-map labels, and latest
  evidence-manifest hash.
- Recorded the 5/5 short-task result, including the mandatory authorization
  stop, as a manual supplied-text admission with human review.

### Boundary retained

- Preserved the failed interactive speed gate at 24.6539 pp512 and 4.92894
  tg128 token/s against 60/8 floors; the short-task result is a separate
  admission and does not qualify interactive performance.
- Recorded that Qwen3.5-4B is not live or deployed: OpenClaw still uses
  `ollama/thumbo-safe:latest` for its offline configuration, and Qwen packaging,
  provider/alias/route/binding work and effective-route testing remain pending.
- No raw run directory, transcript, telemetry, manifest, private path, service
  state, configuration, or recovery-sensitive command was added.

## 2026-08-20 — Preservation-first reuse and post-upgrade evidence

### Added

- Reframed the case study around successful reuse of the 2013 Mac Pro as the
  durable host and orchestrator for Thumbo, while retaining the existing
  multi-agent, least-privilege, route-admission, safety, and local-boundary
  detail.
- Added the exact hardware chronology and current official 64 GB kit state.
- Added a sanitized post-upgrade qualification record covering the guarded
  Qwen2.5-Coder-32B result and the completed Qwen3.5-9B, official Qwen3-8B, and
  Qwen3.5-4B dual-D700 4K benchmark dispositions.
- Added a consolidated multi-agent topology with specialist route boundaries,
  effective enforcement tests, partial dispositions, data-source safety, and
  failure behavior.

### Preserved and corrected

- Preserved every existing public path and kept raw JSON, runners, scripts,
  tests, and non-wrapper dated evidence content unchanged.
- Retained the historic 0/4 and 1/4 usefulness scores as pre-upgrade results;
  later tests are separately dated and do not claim that RAM fixed Vulkan.
- Replaced the broken private continuation link with an explicit public
  exclusion note and removed current-status language from the public narrative.

## 2026-08-14 — Local-model qualification guide

### Added

- Published a fact-locked [Mac Pro 6,1/D700 local-model qualification and
  reproduction guide](docs/local-model-qualification.md) covering exact
  model/quantization roles, host and runtime settings, four strict semantic
  gates, safety stop conditions, and the staged promotion rule.
- Recorded the controlling results together: TinyLlama 1.1B Chat Q2_K at 0/4
  (runtime smoke fixture only) and `thumbo-safe` Llama 3.2 1B Instruct Q8_0 at
  1/4 (bounded, zero-tool, human-reviewed text only).
- Made evidence limits explicit and excluded embedding and cloud models from
  the local D700/Vulkan scores and claims.

## 2026-08-14 — Reproducible D700 Vulkan smoke record

### Verified

- Re-ran a final, guarded 16-token `llama-cli --single-turn` smoke on each
  D700 independently with the Debug/O0 Vulkan build and TinyLlama 1.1B Q2_K.
- Both devices exited successfully within the 75-second limit: `Vulkan0` at
  177.1 prompt tok/s / 55.4 generation tok/s, and `Vulkan1` at 180.7 / 57.7.
- No fresh AMDGPU reset, ring timeout, watchdog, or `llama-cli` kernel trap was
  found in the corresponding kernel-log window.
- Published a sanitized reproduction vector with PCI IDs, OS/kernel, RADV,
  compiler/build, model hash, command, timeout, thermals, results, and explicit
  limitations: [Vulkan smoke record](evidence/vulkan-single-turn-smoke-2026-08-14.md).

### Not promoted

- This does not supersede the documented interactive `libggml-vulkan` fault or
  timeouts. Vulkan local generation remains excluded from automatic routing,
  Ollama integration, interactive use, larger-context/model tests, and dual-GPU
  generation.

## 2026-08-14 — TinyLlama usefulness qualification

### Verified

- Ran four bounded single-turn usefulness gates on `Vulkan0`: fact-locked JSON,
  supplied-context retrieval, bounded arithmetic, and a no-edit safety case.
- The runtime completed every test without a new host fault, but TinyLlama 1.1B
  Chat Q2_K failed all four semantic gates. The performance result (about 56
  generation tok/s) is explicitly separated from usefulness.
- Published the runner, exact prompts, outputs, acceptance criteria, and 0/4
  disposition in [the usefulness record](evidence/vulkan-usefulness-suite-2026-08-14.md).

### Excluded

- TinyLlama 1.1B Chat Q2_K is not a useful local-agent candidate on this stack;
  it is retained only as a Vulkan runtime smoke-test fixture.

## 2026-08-13 — Vulkan inference test harness prepared

### Added

- Installed the Vulkan development packages required to configure upstream
  `llama.cpp` with the GGML Vulkan backend on Nobara:
  `vulkan-headers`, `vulkan-loader-devel`, `libshaderc-devel`, `glslang`, and
  `glslang-devel`.
- Created a temporary upstream `llama.cpp` Vulkan test build under
  `tmp/llama-vulkan-test`.
- Verified the build cache records `GGML_VULKAN=ON` and resolves Vulkan through
  `/usr/include` and `/usr/lib64/libvulkan.so`.

### Not promoted

- This is a harness-preparation milestone only. It does not qualify local LLM
  inference, Ollama multi-GPU behavior, or automatic Main-session fallback.
- Local generation remains bounded to explicit zero-tool use until a guarded
  inference run passes with device mapping, kernel-log, thermal, model, and
  routing evidence.

## 2026-08-12 — Dual-D700 graphics and streaming requalification

### Verified

- Both FirePro D700 devices enumerate through AMDGPU/DRM and RADV Vulkan, with
  6 GiB of VRAM each.
- Short off-screen rendering passed independently on each GPU without an
  observed AMDGPU reset or fault.
- The physical Plasma Wayland desktop and Sunshine capture are GPU-backed.
- The D700 VA-API H.264 encoder works for 1920x1080 streaming. HEVC and AV1 do
  not have usable encoding profiles on this stack.

### Constraints discovered

- XRDP remains a software-rendered virtual session and is retained only as a
  recovery connection.
- H.264 hardware encode is limited to 2048x1152, so 2560x1440 Moonlight
  requests fail during encoder creation. Use 1920x1080 or lower.
- These observations requalify graphics, display, and H.264 encoding only.
  They do not establish local LLM inference stability or multi-GPU inference.

### In progress

- A separately controlled upstream `llama.cpp` Vulkan smoke test now has its
  build prerequisites and a Vulkan-enabled build cache in place. The inference
  run itself remains pending: one non-display GPU first, a small GGUF model, and
  active thermal/kernel monitoring. A two-GPU tensor split is out of scope until
  that first gate passes.

See [the dated evidence record](evidence/dual-d700-requalification-2026-08-12.md)
for scope and limits.
