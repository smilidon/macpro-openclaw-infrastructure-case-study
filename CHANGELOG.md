# Change Log

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

See [the dated evidence record](evidence/dual-d700-requalification-2026-08-12.md)
for the graphics baseline and updated inference-test disposition.

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
