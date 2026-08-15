#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

required_dirs=(docs scripts test fixtures)
required_files=(README.md LICENSE Makefile .gitignore scripts/verify-docs.sh fixtures/README.md)

for path in "${required_dirs[@]}"; do
  [[ -d "$path" ]] || { printf 'Missing project directory: %s\n' "$path" >&2; exit 1; }
done

for path in "${required_files[@]}"; do
  [[ -f "$path" ]] || { printf 'Missing project file: %s\n' "$path" >&2; exit 1; }
done

printf 'PASS: public case-study layout is complete.\n'
