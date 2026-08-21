# Dual FirePro D700 Requalification — 2026-08-12

A related continuation record remains private and is intentionally excluded
from this public repository. This replaces a broken link to the private target
without importing its path or contents.

## Scope

This record captures a bounded graphics, display, and video-encoding
requalification after both FirePro D700 devices were enabled with the `amdgpu`
driver. It does **not** establish that local LLM inference is reliable.

The enabling repair disabled the stale Apple GMUX blacklist file
(`/etc/modprobe.d/blacklist-apple-gmux.conf`), rebuilt the
`7.1.4-200.nobara.fc44.x86_64` initramfs, and retained the existing
`amdgpu.runpm=0` and `amdgpu.ppfeaturemask=0xffffffff` kernel arguments. The
retained repair log is
`gpu-repair/enable-both-d700-20260812-155630.log`; it also records the rollback
procedure.

## Verified observations

- Both AMD Tahiti devices enumerate through DRM and Vulkan (RADV), each with
  6 GiB of VRAM.
- A three-second, off-screen `glmark2-es2-gbm` test passed independently on
  `/dev/dri/renderD128` and `/dev/dri/renderD129`. The recorded scores were
  5853 and 5973 respectively; no AMDGPU reset or fault was observed.
- The physical display is attached to the second device (`card1`, connector
  `DP-4`) at 1920x1080.
- The local Plasma Wayland session is GPU-backed. XRDP is deliberately not
  treated as a GPU-rendered session: its virtual Xorg backend falls back to
  software rendering.
- Sunshine was configured to use VA-API. It captures the physical display with
  KMS and successfully discovers the D700 H.264 encoder (`h264_vaapi`).

## Limits and current disposition

- The D700 VA-API encoder supports H.264 only on this stack; HEVC and AV1
  encoder probes fail because no supported profile is exposed.
- Hardware H.264 has a maximum supported encode size of 2048x1152. Moonlight
  must use 1920x1080 or lower; a 2560x1440 client request fails at encoder
  creation and is not a firewall failure.
- The GPUs are independent devices. Current display capture and H.264 encoding
  use the GPU attached to the physical display. This evidence does not show
  multi-GPU rendering or multi-GPU inference.
- Local LLM inference remains unqualified. Earlier Vulkan/Ollama experiments
  were unstable, so any new inference attempt must use a single non-display
  GPU, a small model, active thermal and kernel monitoring, and immediate stop
  conditions. A successful graphics or video test is not sufficient evidence
  to promote local generation into automatic routing.

## Next controlled experiment

The first part of this experiment is complete: the Vulkan build dependencies
were installed and upstream `llama.cpp` was configured in a temporary test tree
with `GGML_VULKAN=ON`.

Recorded build-preparation facts:

- DNF transaction time: `2026-08-13 00:55:35`.
- Installed packages: `vulkan-headers`, `vulkan-loader-devel`,
  `libshaderc-devel`, `glslang`, and `glslang-devel`.
- Temporary build path: workspace-local `tmp/llama-vulkan-test` (the private
  absolute home path is intentionally omitted).
- Upstream `llama.cpp` revision:
  `8e7f22b67ef4667b4ddd50230771287f328cfb3f`.
- Toolchain observed during follow-up documentation: `cmake version 4.3.0` and
  `gcc (GCC) 16.1.1 20260515 (Red Hat 16.1.1-2)`.
- CMake cache: `GGML_VULKAN:BOOL=ON`,
  `Vulkan_INCLUDE_DIR:PATH=/usr/include`, and
  `Vulkan_LIBRARY:FILEPATH=/usr/lib64/libvulkan.so`.
- Follow-up build attempt on 2026-08-13 found that `glslc` and
  `spirv-headers-devel` were also needed. Because the active shell had no sudo
  password path, those two RPMs were downloaded and extracted locally under
  `tmp/local-tools` for the test build rather than installed into the OS.
- Build state after follow-up: `llama-bench` and `llama-cli` compiled
  successfully in `tmp/llama-vulkan-test/build/bin`.

## llama.cpp Vulkan inference probe — 2026-08-13

Test model:
`tmp/llama-vulkan-test/tinyllama-1.1b-chat-v1.0.Q2_K.gguf`, downloaded from the
public TinyLlama GGUF repository because the existing Ollama `thumbo-safe` blob
is under `/usr/share/ollama` and was not readable by the active user.

Device enumeration passed:

```text
Vulkan0: AMD Radeon R9 200 / HD 7900 Series (RADV TAHITI) (6144 MiB)
Vulkan1: AMD Radeon R9 200 / HD 7900 Series (RADV TAHITI) (6144 MiB)
```

Bounded benchmark results:

```text
Vulkan1, ngl=4, pp32: 15.48 t/s, tg8: 18.21 t/s
Vulkan0, ngl=4, pp32: 109.16 t/s, tg8: 26.43 t/s
Vulkan0/Vulkan1, ngl=8, pp32: 116.96 t/s, tg8: 30.97 t/s
Vulkan0/Vulkan1, ngl=99, pp128: 219.17 t/s, tg32: 29.35 t/s
```

Thermals stayed normal during the bounded runs: GPU edge temperatures remained
around 43-46 C and CPU package temperature remained around 45-47 C. No
`amdgpu` ring timeout, GPU reset, thermal fault, OOM, or watchdog event was
logged during the benchmark windows. `ollama ps` remained empty, so no Ollama
model was resident.

Critical failure:

```text
Aug 13 10:51:01 Thumbo kernel: traps: llama-cli[...] general protection fault
in libggml-vulkan.so.0.19.0
```

The crash happened after a short interactive `llama-cli` generation returned:

```text
The Vulkan test is running in local mode.
Prompt: 156.7 t/s | Generation: 31.3 t/s
```

Disposition: local `llama.cpp` Vulkan is promising for tiny benchmark runs, but
it is **not qualified** for Main/Ollama routing. The interactive runner crash is
a hard stop. Next work should investigate `llama-cli` non-interactive flags or
upstream build/runtime differences before any longer context, larger model, or
OpenClaw integration test.

## llama.cpp one-card fault matrix — 2026-08-13

Follow-up testing rebuilt `llama.cpp` with Debug/O0 symbols:

```text
tmp/llama-vulkan-test/build-debug-o0/bin/llama-cli
version: 0.1.0-dev (commit 8e7f22b), built with GNU 16.1.1
```

The bounded single-turn matrix tested each D700 independently with:

```text
--split-mode none
--flash-attn off
--load-mode none
--single-turn
--simple-io
--no-warmup
```

Results:

- `Vulkan0` passed `--gpu-layers 1`, `4`, `8`, `16`, `32`, and `99`.
- `Vulkan1` passed `--gpu-layers 1`, `4`, `8`, `16`, `32`, and `99`.
- Both cards passed `--load-mode mmap` at `--gpu-layers 8`.
- Both cards passed `--no-kv-offload`, `--no-op-offload`, and combined
  `--no-kv-offload --no-op-offload` at `--gpu-layers 8`.
- No AMDGPU reset, ring timeout, watchdog event, thermal fault, or repeat
  `llama-cli` kernel trap was logged during the single-turn matrix. The one
  kernel line matched by the filter was an unrelated USB enumeration message.

Interactive/conversation mode remains the failing boundary. Bounded stdin tests
against each individual D700 timed out instead of exiting cleanly and produced
large output streams. Combined with the earlier release-build kernel trap, this
points at the `llama-cli` interactive/runtime path or RADV/Tahiti Vulkan backend
rather than a single bad D700.

Retained logs:

```text
tmp/llama-vulkan-test/fault-matrix-singleturn-20260813-113325
tmp/llama-vulkan-test/fault-matrix-interactive-20260813-113752
```
