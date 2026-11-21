#!/usr/bin/env bash
# Local text-to-video (Wan2.1 T2V 1.3B via stable-diffusion.cpp on the FirePro D700s). Free and offline, but slow:
# about 15 minutes for 17 frames at 416x240 (~1 s of video). Set up 2026-11-21.
#
# Usage: local-video "prompt" [output.webm] [frames] [WIDTHxHEIGHT]
#   frames: 17 (default), 33 = ~2 s. Keep frames = 4k+1. Size default 416x240, max 832x480 (very slow).
# Shares ~/models/.gpu-media.lock with the local image service and the llama GPU gate,
# so it waits for running GPU jobs, and GPU chat requests are answered by the CPU model meanwhile.
set -euo pipefail
PROMPT=${1:?usage: local-video "prompt" [output.webm] [frames] [WxH]}
OUT=${2:-$HOME/models/wan/out/video-$(date +%Y%m%d-%H%M%S).webm}
FRAMES=${3:-17}
SIZE=${4:-416x240}
W=${SIZE%x*}; H=${SIZE#*x}
mkdir -p "$(dirname "$OUT")"
LOG="${OUT%.*}.log"
cd "$HOME/models/wan"
exec 9>"$HOME/models/.gpu-media.lock"
echo "waiting for GPU lock..." >&2
flock -x 9
# free the GPUs: unload GPU chat models from the router (embed and lfm3 run on CPU and stay)
for m in gemma-e4b qwen35-9b-abliterated; do
  curl -s -m 30 -X POST http://127.0.0.1:8082/models/unload -H 'Content-Type: application/json' -d "{\"model\":\"$m\"}" >/dev/null || true
done
echo "generating $FRAMES frames at ${W}x${H} -> $OUT (log: $LOG)" >&2
timeout 5400 "$HOME/stable-diffusion.cpp/build/bin/sd-cli" -M vid_gen \
  --diffusion-model wan2.1_t2v_1.3B_fp16.safetensors --vae wan_2.1_vae.safetensors --tae taew2_1.safetensors \
  --t5xxl umt5-xxl-encoder-Q4_K_M.gguf \
  -p "$PROMPT" -n "static, blurry, low quality, distorted, watermark, text, subtitles" \
  --cfg-scale 6.0 --sampling-method euler --flow-shift 3.0 --steps 20 -W "$W" -H "$H" \
  --video-frames "$FRAMES" --fps 16 --seed -1 \
  --backend diffusion=vulkan1,te=vulkan0,vae=vulkan0 --params-backend diffusion=vulkan1,te=vulkan0,vae=vulkan0 \
  --flash-attn on -o "$OUT" >"$LOG" 2>&1 || { echo "FAILED, see $LOG" >&2; grep '\[E\]' "$LOG" | tail -3 >&2; exit 1; }
echo "$OUT"
