# Pushing outputs after a run

After notebooks complete, generated files in the `data/` and `output/` submodules need
to be committed and pushed to their respective repos (TerraNova-Data and TerraNova-Output),
then the parent repo updated to point at the new submodule commits.

Run these commands from the JupyterLab terminal:

## 1. Push data files

```bash
cd /data/data
git add .
git commit -m "Stage1 run: add generated data files"
git push
```

## 2. Push output files (executed notebooks + HTML)

```bash
cd /data/output
git add .
git commit -m "Stage1 run: add executed notebooks and HTML"
git push
```

## 3. Push log files

```bash
cd /data/log
git add .
git commit -m "Stage1 run: add logs"
git push
```

## 4. Update submodule pointers in the main repo

```bash
cd /data
git add data output log
git commit -m "Update submodule pointers after Stage1 run"
git push
```

## Pulling outputs on your local PC

```bash
git pull
git submodule update --remote
```

Or to pull only the data submodule:

```bash
cd data && git pull
```

Sync outputs to HuggingFace Bucket:
```bash
python3 -m venv /data/venv-hf-bucket
  /data/venv-hf-bucket/bin/pip install "huggingface_hub>=1.8.0" typer

# Then each time you sync:

  /data/venv-hf-bucket/bin/hf buckets sync /data hf://buckets/tauheed-elahee/TerraNova

# Store it under /data/ so it persists across Space restarts (unlike /home/user/ which is ephemeral). You could also add the sync command to scripts/push_outputs.md as the
# canonical sync step.
```
```
