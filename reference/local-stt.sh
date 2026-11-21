#!/bin/bash
# local-stt <audio-file> — CPU-only whisper.cpp transcription; prints plain text.
# Converts any input (Ogg/Opus voice notes, mp3, m4a...) to 16 kHz mono WAV first.
set -euo pipefail
tmp=$(mktemp --suffix=.wav); trap 'rm -f "$tmp"' EXIT
ffmpeg -nostdin -loglevel error -y -i "$1" -ar 16000 -ac 1 -c:a pcm_s16le "$tmp"
exec "whisper-cli" -m "${LOCAL_STT_MODEL:-/path/to/models/whisper/ggml-small.en.bin}" \
  -f "$tmp" -t 12 -nt -np 2>/dev/null | sed 's/^ *//'
