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
