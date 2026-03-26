#!/bin/bash
# Run Stage 1 Part B: concept extraction and geometric analysis.
# Requires L_DET and L_PRED to be set in src/config.py before running.
# Run run_stage1a.sh first, then update config.py and push before running this.
#
# Usage: bash scripts/run_stage1b.sh [SESSION_NAME]
SESSION="${1:-terranova-stage1b}"

tmux new-session -d -s "$SESSION" \
  'python3 /data/run_notebooks.py \
     --workspace-dir /data \
     --workspace-subdir stage1-baseline-geometry \
     --verbose \
     /data/src/stage1-baseline-geometry/2-concept-extraction.ipynb \
     /data/src/stage1-baseline-geometry/3-geometric-analysis.ipynb \
  && echo "" \
  && echo "=== Part B complete ===" \
  && echo "Next steps: push outputs — see scripts/push_outputs.md"'

echo "Started session '$SESSION'. Attach with: tmux attach -t $SESSION"
