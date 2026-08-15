#!/usr/bin/env bash
set -euo pipefail

# Bounded functional checks for the admitted Offline lane. This is intentionally
# not a stress test, a tool-use test, or a qualification of automatic routing.

root="$(cd "$(dirname "$0")" && pwd)"
out_dir="$root/results"
mkdir -p "$out_dir"
stamp="$(date +%Y%m%dT%H%M%S%z)"
result="$out_dir/thumbo-safe-$stamp.json"
model="thumbo-safe:latest"
# On this host, prompt evaluation alone can take about 30 seconds.  A 75-second
# ceiling still bounds the run while avoiding false timeout failures.
max_time="${EVAL_MAX_TIME:-75}"
num_predict="${EVAL_NUM_PREDICT:-32}"
num_gpu="${EVAL_NUM_GPU:-4}"

cases='[
  {
    "id":"exact_retrieval",
    "system":"Reply only with the requested value.",
    "prompt":"Record A: routine note.\\nRecord B: cobalt key = HARBOR-7429.\\nRecord C: routine note.\\n\\nWhat is the cobalt key?",
    "expected":"HARBOR-7429",
    "kind":"exact"
  },
  {
    "id":"scope_classification",
    "system":"Reply with exactly one token: SAFE or REVIEW_REQUIRED.",
    "prompt":"Task: summarize supplied text without tools. Classify the task.",
    "expected":"SAFE",
    "kind":"exact"
  },
  {
    "id":"structured_output",
    "system":"Reply only with valid JSON matching exactly this schema: {\\\"label\\\":string}.",
    "prompt":"Label this supplied-text task as safe. Return the JSON object.",
    "expected":"{\"label\":\"safe\"}",
    "kind":"json"
  },
  {
    "id":"incident_note_summary",
    "system":"Use only the supplied note. Return exactly three concise Markdown bullets: observed event, engineering decision, and remaining limit. Do not recommend commands or add facts.",
    "prompt":"Incident note: A legacy AMD GPU host experienced Vulkan device loss and ring timeouts under sustained large-context local generation. Temperatures stayed below the configured stop thresholds. The system therefore removed the affected local generators from automatic routing and retained only an explicit, zero-tool offline lane for bounded text tasks. The exact root cause was not proven.",
    "expected":"human review required: source-grounded three-bullet summary with no added facts or commands",
    "kind":"manual"
  }
]'

if [ -n "${EVAL_CASE:-}" ]; then
  cases="$(jq --arg id "$EVAL_CASE" '[.[] | select(.id == $id)]' <<<"$cases")"
fi

faults_before="$(journalctl -k -n 160 --no-pager | rg -i 'amdgpu.*(ring|timeout|reset|error)|vulkan|device.*lost' || true)"

run_case() {
  local case_json="$1" id system prompt expected kind response code curl_status body content pass
  id="$(jq -r '.id' <<<"$case_json")"
  system="$(jq -r '.system' <<<"$case_json")"
  prompt="$(jq -r '.prompt' <<<"$case_json")"
  expected="$(jq -r '.expected' <<<"$case_json")"
  kind="$(jq -r '.kind' <<<"$case_json")"
  response="$(mktemp)"
  if code="$(curl --silent --show-error --output "$response" --write-out '%{http_code}' \
    --max-time "$max_time" http://127.0.0.1:11434/api/chat \
    -H 'Content-Type: application/json' \
    --data "$(jq -nc --arg model "$model" --arg system "$system" --arg prompt "$prompt" --argjson num_predict "$num_predict" --argjson num_gpu "$num_gpu" '
      {model:$model,stream:false,think:false,keep_alive:"0",
       options:{num_ctx:4096,num_gpu:$num_gpu,num_predict:$num_predict,temperature:0,seed:42},
       messages:[{role:"system",content:$system},{role:"user",content:$prompt}]}
    ')")"; then
    curl_status=0
  else
    curl_status=$?
  fi
  body="$(cat "$response" 2>/dev/null || true)"
  rm -f "$response"
  content="$(jq -r '.message.content // ""' <<<"$body" 2>/dev/null || true)"
  if [ "$kind" = exact ]; then
    [ "$content" = "$expected" ] && pass=true || pass=false
  elif [ "$kind" = json ]; then
    jq -e --argjson expected "$expected" '.message.content | fromjson == $expected' <<<"$body" >/dev/null 2>&1 && pass=true || pass=false
  else
    pass=null
  fi
  jq -nc --arg id "$id" --arg expected "$expected" --arg content "$content" \
    --arg code "$code" --argjson curl_status "$curl_status" --argjson pass "$pass" --argjson raw "${body:-null}" '
    {id:$id,http_status:$code,curl_status:$curl_status,pass:$pass,expected:$expected,content:$content,
     metrics:($raw | {total_duration,prompt_eval_count,eval_count})}
  '
}

results='[]'
while IFS= read -r case_json; do
  results="$(jq --argjson item "$(run_case "$case_json")" '. + [$item]' <<<"$results")"
done < <(jq -c '.[]' <<<"$cases")

faults_after="$(journalctl -k -n 160 --no-pager | rg -i 'amdgpu.*(ring|timeout|reset|error)|vulkan|device.*lost' || true)"
jq -n --arg generated_at "$(date --iso-8601=seconds)" --arg model "$model" --argjson num_predict "$num_predict" --argjson num_gpu "$num_gpu" \
  --arg faults_before "$faults_before" --arg faults_after "$faults_after" \
  --argjson cases "$results" '
  {generated_at:$generated_at,model:$model,
   settings:{num_ctx:4096,num_gpu:$num_gpu,num_predict:$num_predict,temperature:0,seed:42},
   kernel_faults_before:$faults_before,kernel_faults_after:$faults_after,cases:$cases}
  ' > "$result"
printf '%s\n' "$result"
