# Vulkan Selection Preflight — 2026-08-10

## Scope

This record was made before an authorized one-time Ollama service restart and
the CPU-control/GPU evaluation pair.  The required Desktop setup references
were read first:

- `~/Desktop/Thumbo Project/TECHNICAL.md`
- `~/Desktop/Thumbo Project/LOCAL_MODEL_AND_SYSTEM_INVENTORY.md`

## Observed mapping

`vulkaninfo --summary`, run as the interactive account (which is a member of
the `ollama` group), reports:

| Vulkan enumeration index | Device | PCI / role |
| --- | --- | --- |
| `0` | AMD Radeon R9 200 / HD 7900 Series (RADV TAHITI) | FirePro D700, `0000:06:00.0`, the non-display GPU with `/dev/dri/renderD128` |
| `1` | llvmpipe (LLVM 22.1.8) | software CPU Vulkan implementation |

The Ollama service runs as `ollama`, which has membership in both `video` and
`render`.  Its existing `GGML_VK_VISIBLE_DEVICES=1` therefore selects
llvmpipe, matching the service log (`Vulkan0: llvmpipe`) and disproving the
older comment that device 1 was the non-display D700.

## Required minimal correction

Change only `GGML_VK_VISIBLE_DEVICES` in
`/etc/systemd/system/ollama.service.d/zz-cpu-only-test.conf`, from `1` to `0`,
then restart `ollama.service` once.  Confirm the post-restart log identifies
the RADV TAHITI/D700 rather than llvmpipe before running the GPU test.

## Stop / block state

This session cannot write `/etc/systemd/system` or restart the system service:
non-interactive `sudo` requires a password.  Also, the documented
`ollama-safety-watchdog.service` was inactive during preflight.  No service
change, restart, or model evaluation was attempted from this session.
