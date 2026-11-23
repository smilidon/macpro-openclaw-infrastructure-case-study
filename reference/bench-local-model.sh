#!/usr/bin/env bash
# Standard benchmarks for one GGUF behind llama-server (OpenAI-compatible API).
#   BFCL v4 (official bfcl-eval package): simple_python + multiple, native tool calls
#   MMLU-Pro (EleutherAI lm-evaluation-harness, task default 5-shot CoT)
# Speed is measured separately with llama.cpp's own llama-bench, e.g.
#   llama-bench -m model.gguf -ngl 0 -dev none -t 12 -p 512 -n 64
#
# Setup (Python 3.12 venv):
#   uv venv evals --python 3.12
#   uv pip install --python evals/bin/python "lm-eval[api]==0.4.13" bfcl-eval==2026.3.23 soundfile "pyarrow<20"
#   (bfcl-eval pins NumPy 1.26; pyarrow 20+ needs NumPy 2)
# Fixed question subset: put a test_case_ids_to_generate.json in $BFCL_PROJECT_ROOT,
#   e.g. {"simple_python": [...50 ids...], "multiple": [...50 ids...]}
#
# usage: bench-local-model.sh <label> <model.gguf> ["<extra llama-server args>"]
#   env: LLAMA_BIN (dir with llama-server), EVALS (venv dir), BFCL_PROJECT_ROOT,
#        OUT (results dir), THREADS (12), MMLU_LIMIT (questions per subject, 10)
set -u
LABEL=$1 GGUF=$2 EXTRA=${3:-}
: "${LLAMA_BIN:?set LLAMA_BIN}" "${EVALS:?set EVALS}" "${BFCL_PROJECT_ROOT:?set BFCL_PROJECT_ROOT}"
OUT=${OUT:-./bench-results}; mkdir -p "$OUT"; OUT=$(cd "$OUT" && pwd)
PORT=${PORT:-8096}

"$LLAMA_BIN/llama-server" -m "$GGUF" --host 127.0.0.1 --port "$PORT" -ngl 0 -dev none \
  -t "${THREADS:-12}" -c 16384 -np 1 --jinja $EXTRA > "$OUT/$LABEL.server.log" 2>&1 &
SP=$!
trap 'kill $SP 2>/dev/null; wait $SP 2>/dev/null' EXIT
for _ in $(seq 180); do curl -sf "http://127.0.0.1:$PORT/health" >/dev/null && break; sleep 2; done

# BFCL: the gpt-4o FC handler speaks the OpenAI tools API; OPENAI_BASE_URL points it at llama-server
export OPENAI_BASE_URL=http://127.0.0.1:$PORT/v1 OPENAI_API_KEY=local BFCL_PROJECT_ROOT
cd "$BFCL_PROJECT_ROOT"
"$EVALS/bin/bfcl" generate --model gpt-4o-2024-11-20-FC --test-category simple_python,multiple \
  --run-ids --num-threads 1 --temperature 0 --result-dir "result-$LABEL" -o > "$OUT/$LABEL.bfcl-gen.log" 2>&1
"$EVALS/bin/bfcl" evaluate --model gpt-4o-2024-11-20-FC --test-category simple_python,multiple \
  --partial-eval --result-dir "result-$LABEL" --score-dir "score-$LABEL" > "$OUT/$LABEL.bfcl-eval.log" 2>&1
grep -E "Accuracy" "$OUT/$LABEL.bfcl-eval.log"

"$EVALS/bin/lm_eval" --model local-chat-completions \
  --model_args "model=local,base_url=http://127.0.0.1:$PORT/v1/chat/completions,num_concurrent=1,max_retries=3,tokenized_requests=False" \
  --tasks mmlu_pro --apply_chat_template --limit "${MMLU_LIMIT:-10}" \
  --gen_kwargs "max_gen_toks=1024,temperature=0" --output_path "$OUT/$LABEL.mmlu" --log_samples \
  > "$OUT/$LABEL.mmlu.log" 2>&1
grep -E "^\|mmlu_pro " "$OUT/$LABEL.mmlu.log" | head -1
