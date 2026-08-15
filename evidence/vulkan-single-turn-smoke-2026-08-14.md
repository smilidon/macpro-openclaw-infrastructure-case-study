# Dual FirePro D700 Vulkan single-turn smoke — 2026-08-14

## Verdict: PARTIAL

**Question.** Can each FirePro D700 complete a tightly bounded, one-shot `llama.cpp` Vulkan generation on the repaired host without a fresh kernel fault?

**Answer.** Yes, for this exact smoke-test envelope. This is not an admission test for interactive chat, a larger model, dual-GPU generation, Ollama, or agent routing.

## Reproduction-grade environment

| Component | Captured value |
| --- | --- |
| Host class | Apple Mac Pro 6,1 (2013) |
| CPU / memory | Xeon E5-2697 v2, 12 cores / 24 threads; 32 GiB RAM |
| OS | Nobara Linux 44 (KDE) |
| Kernel | `7.1.4-200.nobara.fc44.x86_64` |
| GPUs | Two Apple FirePro D700 devices: PCI IDs `1002:6798`, subsystem IDs `106b:0128` and `106b:0127` |
| Kernel driver | `amdgpu` on both adapters |
| Vulkan implementation | Mesa RADV 26.2.0; Vulkan API 1.3.354 on both Tahiti devices |
| Vulkan memory reported by `llama-cli` | 6144 MiB per adapter; 5353 MiB free on `Vulkan0`, 6132 MiB free on `Vulkan1` immediately before the run |
| `llama.cpp` source | upstream commit `8e7f22b67ef4667b4ddd50230771287f328cfb3f` |
| Build | Debug / `-O0`, `GGML_VULKAN=ON`; CMake 4.3.0; GCC 16.1.1 |
| Model | TinyLlama 1.1B Chat v1.0, GGUF `Q2_K`; 483,116,416 bytes; SHA-256 `030a469a63576d59f601ef5608846b7718eaa884dd820e9aa7493efec1788afa` |

The host retained the AMDGPU stability parameters `amdgpu.runpm=0 amdgpu.ppfeaturemask=0xffffffff`. They are part of this host's operating state, not a claim that they cure the Vulkan issue.

## Method

Each GPU was run separately. The executable was the Debug/O0 `llama-cli`; the model was loaded with no mmap and no warmup. Output was redirected, and the process had a 75-second timeout (with a 10-second kill grace period). No Ollama model was loaded or started. The command, substituting the local binary and model paths, was:

```sh
timeout --kill-after=10s 75s llama-cli \
  -m tinyllama-1.1b-chat-v1.0.Q2_K.gguf \
  --device Vulkan0 \
  --gpu-layers 99 --split-mode none \
  --flash-attn off --load-mode none \
  --single-turn --simple-io --no-warmup \
  --ctx-size 512 --n-predict 16 \
  -p 'Reply with exactly: local Vulkan smoke test.'
```

The `Vulkan1` run differed only in `--device Vulkan1`. Kernel logs and temperatures were captured before and after the pair. A fresh-log check found no event during the run window matching AMDGPU reset, ring timeout, watchdog, general-protection fault, or `llama-cli` trap. The journal does contain the separate 2026-08-13 `libggml-vulkan` fault documented below; it is not presented as a result of this smoke test.

Both successful runs also wrote the same startup diagnostic to stderr: `failed to find ggml_backend_init` while scanning `libggml-vulkan.so` and `libggml-cpu.so`. The device list was nevertheless available and the requested `Vulkan0`/`Vulkan1` run completed. This observation is retained as a build/runtime caveat, not silently treated as normal or as proof of the root cause.

## Results

| Device | Exit | Wall time | Prompt throughput | Generation throughput | Result |
| --- | ---: | ---: | ---: | ---: | --- |
| `Vulkan0` | 0 | 2.48 s | 177.1 tok/s | 55.4 tok/s | completed and exited |
| `Vulkan1` | 0 | 2.65 s | 180.7 tok/s | 57.7 tok/s | completed and exited |

GPU thermal sensors were approximately 44.0 C (`TG0D`) and 49.5 C (`TG1D`) before the pair, and 45.2 C and 50.5 C afterward. The main fan remained at 1350 RPM. These are short-run observations, not sustained-load thermals.

## What this does and does not establish

Both cards can perform a short, full-offload, single-turn TinyLlama generation under the stated stack. The prompt demanded an exact phrase, and neither model response matched it. That makes this a runtime/throughput smoke test, not a quality, instruction-following, or structured-output pass.

On 2026-08-13, a release-build interactive run produced a kernel general-protection fault in `libggml-vulkan.so.0.19.0`; Debug/O0 interactive stdin probes on both individual GPUs then timed out rather than exiting cleanly. See [the requalification record](dual-d700-requalification-2026-08-12.md). That failure remains the controlling disposition: do not route local Vulkan generation automatically, run it conversationally, increase context/model size, or test dual-GPU generation on the strength of this result.

## Replication notes for comparable hardware

Treat the PCI subsystem IDs, kernel, Mesa/RADV version, `llama.cpp` commit, model hash, and CLI flags above as a complete test vector. Verify your own device list with `llama-cli --list-devices`, run one adapter at a time, redirect stdout/stderr, use a short timeout, and inspect only the kernel-log interval covering the test. Stop rather than retry if an AMDGPU reset, ring timeout, watchdog/device-loss signal, or kernel trap appears.

This record deliberately omits host name, serial identifiers, raw journal, paths, and model distribution URL. Those do not improve reproducibility and would expand the public attack surface.
