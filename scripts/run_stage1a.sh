#!/bin/bash
# Run Stage 1 Part A: model setup, SNOMED graph, and layer calibration.
# After this completes, check data/stage1-baseline-geometry/layer_boundaries.json,
# update L_DET and L_PRED in src/config.py, commit, push, then run run_stage1b.sh.
#
# Usage: bash scripts/run_stage1a.sh [SESSION_NAME]
SESSION="${1:-terranova-stage1a}"

tmux new-session -d -s "$SESSION" \
  'python3 /data/run_notebooks.py \
     --workspace-dir /data \
     --workspace-subdir stage1-baseline-geometry \
     --verbose \
     /data/src/stage1-baseline-geometry/0-model-setup.ipynb \
     /data/src/stage1-baseline-geometry/0b-snomed-graph.ipynb \
     /data/src/stage1-baseline-geometry/1-layer-calibration.ipynb \
  && echo "" \
  && echo "=== Part A complete ===" \
  && echo "Next steps:" \
  && echo "  1. Check /data/data/stage1-baseline-geometry/layer_boundaries.json" \
  && echo "  2. Set L_DET and L_PRED in /data/src/config.py" \
  && echo "  3. git add src/config.py && git commit -m \"Set L_DET and L_PRED\" && git push" \
  && echo "  4. Run: bash /data/scripts/run_stage1b.sh"'

echo "Started session '$SESSION'. Attach with: tmux attach -t $SESSION"
