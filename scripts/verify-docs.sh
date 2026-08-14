#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

failures=0
checked_links=0
public_markdown=(README.md CHANGELOG.md docs evidence fixtures)

while IFS=: read -r source_file line_number target; do
  target="${target%%#*}"
  [[ -z "$target" || "$target" == http://* || "$target" == https://* || "$target" == mailto:* ]] && continue
  checked_links=$((checked_links + 1))
  if [[ ! -e "$(dirname "$source_file")/$target" ]]; then
    printf 'Broken local link: %s:%s -> %s\n' "$source_file" "$line_number" "$target" >&2
    failures=1
  fi
done < <(rg -n -o '\]\([^ )]+' --glob '*.md' "${public_markdown[@]}" | sed -E 's#^([^:]+):([0-9]+):.*\]\(([^ )]+)$#\1:\2:\3#')

if rg -n -i --glob '*.md' \
  '/home/|\\b(?:api[_-]?key|secret|token|password)\\b[[:space:]]*[:=]|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----' \
  "${public_markdown[@]}"; then
  printf 'Possible private path or secret-like material found.\n' >&2
  failures=1
fi

required=(README.md LICENSE Makefile .gitignore scripts/verify-docs.sh test/test-public-pack.sh docs/architecture.md docs/decision-record.md docs/evidence.md docs/building.md docs/known-issues.md docs/system-profile.md docs/safety-controls.md docs/qualification-protocol.md docs/operational-model.md fixtures/README.md)
for path in "${required[@]}"; do
  if [[ ! -f "$path" ]]; then
    printf 'Missing required public artifact: %s\n' "$path" >&2
    failures=1
  fi
done

if (( failures )); then
  exit 1
fi

printf 'PASS: %s local Markdown links checked; public-artifact and exposure checks passed.\n' "$checked_links"
