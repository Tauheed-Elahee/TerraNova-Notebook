# TerraNova-Notebook

Investigating how much SNOMED CT ontological structure is encoded in LLM hidden representations.

## Experiment Overview

A three-stage pipeline applied to 1,879 breast cancer SNOMED CT concepts:

| Stage | Method | Question |
|---|---|---|
| **Baseline** (Experiment 01) | OpenAI `text-embedding-3-large` | What structure do off-the-shelf embeddings capture? (ρ ≈ 0.30) |
| **Stage 1** | LLM residual stream at detokenisation layer | How much ontological structure is in the frozen model's hidden states? |
| **Stage 2** | Token Distillation (single-token concepts) | Does tokenisation granularity explain the Stage 1 result? |
| **Stage 3** | MedTok-style ontology-supervised encoder | Upper bound with explicit ontological supervision (future work) |

## Implementation Plan

See [`notes/plans/stage-implementation-plan.md`](notes/plans/stage-implementation-plan.md) for the full design, notebook sequence, data outputs, and reference paper mapping.

## Data

SNOMED concept data is retrieved via the Snowstorm client at https://snowstorm.snomed.consultologist.ai

## Container Environment Variables

| Variable | Value | Effect |
|---|---|---|
| `HF_HOME` | `/data/.cache/huggingface` | Redirects all HuggingFace caching to the persistent Azure datastore |
| `HUGGINGFACE_TOKEN` | `<token>` | Authenticates access to gated models (e.g. Meta-Llama-3-8B) |
| `HF_HUB_DISABLE_SYMLINKS_WARNING` | `1` | Suppresses symlinks warning (Azure datastore does not support symlinks) |
| `HF_HUB_VERBOSITY` | `error` | Suppresses `Could not set the permissions` warnings (Azure datastore does not support chmod) |
| `TQDM_NOTEBOOK` | `0` | Forces tqdm into plain text mode (widget mode is unreliable on Azure datastore) |

### `HF_HUB_VERBOSITY` options

| Value | Effect |
|---|---|
| `debug` | All messages including internal debug output |
| `info` | Informational messages and above |
| `warning` | Warnings and above (default) |
| `error` | Errors only — suppresses all warnings including `Could not set the permissions` |
| `critical` | Critical errors only |

### All `HF_HUB_DISABLE_*` flags

| Flag | Suppresses |
|---|---|
| `HF_HUB_DISABLE_SYMLINKS_WARNING` | Symlinks not supported warning |
| `HF_HUB_DISABLE_PROGRESS_BARS` | All download progress bars |
| `HF_HUB_DISABLE_IMPLICIT_TOKEN` | Warning when token is used implicitly |
| `HF_HUB_DISABLE_EXPERIMENTAL_WARNING` | Experimental feature warnings |
| `HF_HUB_DISABLE_TELEMETRY` | Usage telemetry sent to HuggingFace |
| `HF_HUB_DISABLE_XET` | XetHub storage backend |

## License

Copyright 2026 Tauheed Elahee. All rights reserved.

This software is licensed under the [PolyForm Strict License 1.0.0](LICENSE).
The only permitted use is running the software to verify and reproduce the
research results described in this repository. No other use, modification,
or distribution is permitted without explicit written consent from the author.
