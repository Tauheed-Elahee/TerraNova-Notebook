#!/bin/bash
# Run all Stage 1 notebooks in order inside a detachable tmux session.
# Usage: bash scripts/run_stage1.sh [SESSION_NAME]
SESSION="${1:-terranova-stage1}"

tmux new-session -d -s "$SESSION" \
  'python3 /data/run_notebooks.py \
     --workspace-dir /data \
     --workspace-subdir stage1-baseline-geometry \
     --verbose \
     /data/src/stage1-baseline-geometry/0-model-setup.ipynb \
     /data/src/stage1-baseline-geometry/0b-snomed-graph.ipynb \
     /data/src/stage1-baseline-geometry/1-layer-calibration.ipynb \
     /data/src/stage1-baseline-geometry/2-concept-extraction.ipynb \
     /data/src/stage1-baseline-geometry/3-geometric-analysis.ipynb'

echo "Started session '$SESSION'. Attach with: tmux attach -t $SESSION"
