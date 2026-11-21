#!/bin/bash
# local-tts "text" out.wav  — CPU-only Piper speech synthesis (no GPU lock needed)
set -euo pipefail
printf '%s' "$1" | exec "piper" -m "/path/to/models/piper/en_US-lessac-medium.onnx" -f "$2" 2>/dev/null
