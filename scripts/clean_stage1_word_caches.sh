#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CACHE_DIR="$REPO_ROOT/data/stage1/cache"

targets=(
  part1a
  part1b
  part1c
  part1e
  part1h_single_token_t0
  part2b_next_word_type
  part2c_next_word_type
  part2c_single_token_lens
)

if [[ ! -d "$CACHE_DIR" ]]; then
  echo "Cache directory does not exist: $CACHE_DIR"
  echo "Nothing to delete."
  exit 0
fi

echo "Deleting allowlisted Stage 1 word/cache files from: ${CACHE_DIR#$REPO_ROOT/}"
deleted=0
for stem in "${targets[@]}"; do
  for ext in pkl json; do
    path="$CACHE_DIR/$stem.$ext"
    if [[ -e "$path" ]]; then
      rm -v "$path"
      deleted=1
    fi
  done
done

if [[ "$deleted" -eq 0 ]]; then
  echo "No allowlisted cache files found."
fi

