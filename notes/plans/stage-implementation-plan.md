---
title: Implementation Plan — Three-Stage Semantic Core Pipeline
tags: [plan, stage1, stage2, stage3, implementation, semantic-core, geometry, snomed, transformer-lens]
summary: Implementation plan for the three-stage geometric experiment described in combined-architecture-semantic-core-pipeline.md, covering baseline geometry (Stage 1), vocabulary expansion (Stage 2), and ontology-supervised upper bound (Stage 3).
---

# Implementation Plan — Three-Stage Semantic Core Pipeline

Reference design: [[combined-architecture-semantic-core-pipeline|↗]]

---

## Critical Prerequisite: Model Selection

**Must be decided before Stage 1 begins.** Layer boundaries (~12, ~20) differ per model — the figures in the design document were measured on GPT-2-scale models and must be re-derived empirically.

Constraints:
- TransformerLens-compatible (required for residual stream access)
- Medical pretraining preferred — rare SNOMED concepts need stronger representations
- Must fit GPU memory for ~1,879 concepts × ~50 tokens per concept

Candidates from `notes/goal.md`: `Mistral-7B`, `Llama-3-8B`, `BioMedLM` (2.7B, PubMed-trained), `Med42`.

---

## Stage 1 — Baseline Geometry

**Directory:** `src/stage1-baseline-geometry/`

**Goal:** Measure how much SNOMED ontological structure is implicitly encoded in frozen LLM residual stream representations.

### Notebooks

#### `0-model-setup.ipynb`
- Load chosen model via `HookedTransformer.from_pretrained` (TransformerLens)
- Verify GPU memory and run a test forward pass on a few SNOMED concept names
- Write model identifier to shared config

#### `1-layer-calibration.ipynb`
- **Token Erasure** (2406.20086 — [sfeucht/footprints](https://github.com/sfeucht/footprints), `Reference_Papers/footprints`):
  - Run on ~50–100 breast SNOMED concepts of varying length and rarity
  - Identify layer of maximal erasure → detokenisation completion layer `L_det`
  - Estimate failure rate for medical terminology (paper baseline: ~23% for general English; named entities show strongest erasure signal)
- **Tuned Lens** (2303.08112 — [AlignmentResearch/tuned-lens](https://github.com/AlignmentResearch/tuned-lens), `Reference_Papers/tuned-lens`):
  - Identify layer where next-token prediction stabilises → `L_pred`
- Save `L_det`, `L_pred`, failure rate estimate to `data/stage1/layer_boundaries.json`

#### `2-concept-extraction.ipynb`
- Load `data/concepts.csv` (1,879 breast concepts — from Experiment 01)
- Forward pass for each concept; extract at `L_det`:
  - **Method A**: last-token hidden state
  - **Method B**: mean-pooling over all token positions (more robust: doesn't require erasure layer identification; unaffected by failure rate — see Subword Compositionality 2508.17953, no public repo)
- Save to `data/stage1/hidden_states_last_token.npy` and `hidden_states_mean_pool.npy`

#### `3-geometric-analysis.ipynb`
- Pairwise cosine distances in residual stream space
- Load `data/ontological_distances.csv` (from Experiment 01)
- Spearman rank correlation under two SNOMED distance conditions:
  1. Shortest-path distance on `is-a` graph (already computed)
  2. IC-based metric (Resnik or Lin similarity) — weights by concept specificity; may correlate better with LLM representations because both reflect training data frequency
- Stratify by pretraining frequency proxy (Wikipedia article existence or Google NGram)
- **Three-way comparison** against SNOMED distance matrix:
  - LLM residual stream (Stage 1 result)
  - `data/embeddings_normalised.csv` — OpenAI `text-embedding-3-large` (existing, ρ ≈ 0.30)
  - KEEP embeddings (2510.05049 — [G2Lab/keep](https://github.com/G2Lab/keep)) — off-the-shelf pretrained, no training required
- **Hyperbolic geometry tests** (motivated by Snomed2Vec 1907.08650 — [agarwal.khushbu/Snomed2Vec](https://gitlab.com/agarwal.khushbu/Snomed2Vec) showing Poincaré > Euclidean for SNOMED):
  - Gromov δ-hyperbolicity (four-point condition on pairwise distance matrix)
  - UMAP with hyperbolic metric (`umap-learn`, `output_metric='hyperboloid'`)
  - Hyperbolic probing classifier: does ancestor/descendant membership predict geometry in hyperbolic space?
- Run for both extraction methods A and B — if they agree, finding is robust to extraction choice
- **Reuse:** `src/concept-openai-embeddings/utils.py` — k-NN graph, distance matrices, Plotly 3D, Chatterjee correlation

**Expected effect size:** Spearman ρ ~ 0.2–0.4 for a well-attested concept subset (per design document). KEEP sets the pretrained upper bound; OpenAI embeddings are the existing baseline.

### Data outputs
```
data/stage1/
  layer_boundaries.json
  hidden_states_last_token.npy
  hidden_states_mean_pool.npy
  pairwise_distances.csv
  correlation_results.csv        # ρ under all conditions, both methods
  plots/
```

---

## Stage 2 — Expanded Vocabulary Geometry

**Directory:** `src/stage2-vocabulary-expansion/`

**Goal:** Measure how much geometric correlation changes when SNOMED concepts enter as single tokens rather than assembled subword fragments. The Stage 1→2 delta isolates the **tokenisation granularity effect**.

**Prerequisites:** Stage 1 complete (concept set fixed, model chosen, `L_det` known).

### Notebooks

#### `1-token-distillation.ipynb`
- Train new input embeddings for SNOMED concepts using Token Distillation (2505.20133 — [konstantinjdobler/token-distillation](https://github.com/konstantinjdobler/token-distillation))
- Method: new embedding at layer 0 is trained to reproduce the mid-layer attention patterns the original multi-token sequence produces
- **Important limitation to document:** any Stage 1→2 delta could reflect tokenisation granularity *or* imperfect distillation — acknowledge in notebook markdown
- For particularly long concept names (e.g. `"malignant neoplasm of upper outer quadrant of female breast"`), Cramming (2502.13063 — [yurakuratov/hidden_capacity](https://github.com/yurakuratov/hidden_capacity)) is an alternative initialisation strategy
- Save trained embedding matrix to `data/stage2/snomed_concept_embeddings.pt`

#### `2-concept-extraction.ipynb`
- Inject each new single-token embedding into model at layer 0
- Extract hidden states at `L_det`
- Save to `data/stage2/hidden_states.npy`

#### `3-geometric-analysis.ipynb`
- Re-run the same geometric analysis as Stage 1 notebook 3
- **Delta analysis:** Stage 1 ρ vs Stage 2 ρ under each condition — direction is the scientific finding
- Reuse `utils.py` throughout

### Data outputs
```
data/stage2/
  snomed_concept_embeddings.pt
  hidden_states.npy
  pairwise_distances.csv
  correlation_results.csv
  delta_vs_stage1.csv
  plots/
```

---

## Stage 3 — Ontology-Supervised Geometry (Stub / Future Work)

**Directory:** `src/stage3-ontology-supervised/`

A `README.md` planning document rather than runnable code. Documents:
- Train a MedTok-style (2502.04397 — [mims-harvard/MedTok](https://github.com/mims-harvard/MedTok), `Reference_Papers/MedTok`) encoder where ontological graph position is explicit in the input representation
- Stage 2→3 delta isolates the **ontological supervision effect** — the trained upper bound
- Proceed only if Stages 1 and 2 show meaningful geometry worth explaining
- KEEP embeddings (available at Stage 1) are a separate pretrained reference point — not equivalent to Stage 3's trained-from-scratch encoder

---

## Shared Infrastructure

### `src/config.py` — shared model/layer config
```python
MODEL_NAME = "..."     # Set after model selection
L_DET = None           # Set after layer calibration (Stage 1 notebook 1)
L_PRED = None          # Set after layer calibration (Stage 1 notebook 1)
CONCEPT_CSV = "data/concepts.csv"
ONTOLOGY_DISTANCES_CSV = "data/ontological_distances.csv"
```

### Reuse from Experiment 01

| Asset | Path | Used in |
|---|---|---|
| Concept list | `data/concepts.csv` | Stages 1, 2 |
| SNOMED distances | `data/ontological_distances.csv` | Stages 1, 2 |
| OpenAI embeddings | `data/embeddings_normalised.csv` | Stage 1 comparison |
| Graph + viz utilities | `src/concept-openai-embeddings/utils.py` | Stages 1, 2 |

### Final `src/` structure
```
src/
  config.py
  concept-openai-embeddings/       # Existing (Experiment 01)
  stage1-baseline-geometry/
    0-model-setup.ipynb
    1-layer-calibration.ipynb
    2-concept-extraction.ipynb
    3-geometric-analysis.ipynb
  stage2-vocabulary-expansion/
    1-token-distillation.ipynb
    2-concept-extraction.ipynb
    3-geometric-analysis.ipynb
  stage3-ontology-supervised/
    README.md
```

---

## Verification

- Stage 1 notebook 3: LLM residual stream ρ should be weaker than KEEP and stronger than random (ρ ~ 0.2–0.4 for well-attested subset)
- Stage 1 notebook 3: last-token and mean-pool extraction should produce consistent ρ (robustness check)
- Stage 2 notebook 3: delta from Stage 1 is the primary scientific result — direction (positive = atomisation helps, negative = assembly was fine) is the finding
- Three-way comparison (LLM vs. OpenAI vs. KEEP) at Stage 1 is immediately deployable and requires no training

---

## Referenced Implementations

| arXiv | Paper | GitHub | Used in |
|---|---|---|---|
| 2406.20086 | Token Erasure | [sfeucht/footprints](https://github.com/sfeucht/footprints) | Stage 1 layer calibration |
| 2303.08112 | Tuned Lens | [AlignmentResearch/tuned-lens](https://github.com/AlignmentResearch/tuned-lens) | Stage 1 layer calibration |
| 2508.17953 | Subword Compositionality | — (no public repo) | Stage 1 extraction method B |
| 2510.05049 | KEEP | [G2Lab/keep](https://github.com/G2Lab/keep) | Stage 1 three-way comparison |
| 1907.08650 | Snomed2Vec | [agarwal.khushbu/Snomed2Vec](https://gitlab.com/agarwal.khushbu/Snomed2Vec) | Stage 1 hyperbolic geometry baseline |
| 2405.14860 | Not All LM Features Are Linear | [Tauheed-Elahee/MultiDimensionalFeatures](https://github.com/Tauheed-Elahee/MultiDimensionalFeatures) | Stage 1 SAE clustering (optional) |
| 2505.18235 | Origins of Representation Manifolds | [alexandermodell/Representation-Manifolds](https://github.com/alexandermodell/Representation-Manifolds) | Stage 1 manifold geometry analysis |
| 2410.05864 | Tokens2Words | [schwartz-lab-NLP/Tokens2Words](https://github.com/schwartz-lab-NLP/Tokens2Words) | Stage 1 layer calibration reference |
| 2505.20133 | Token Distillation | [konstantinjdobler/token-distillation](https://github.com/konstantinjdobler/token-distillation) | Stage 2 embedding training |
| 2502.13063 | Cramming | [yurakuratov/hidden_capacity](https://github.com/yurakuratov/hidden_capacity) | Stage 2 alternative for long names |
| 2502.04397 | MedTok | [mims-harvard/MedTok](https://github.com/mims-harvard/MedTok) | Stage 3 (future) encoder design |
| 2412.06769 | Coconut | [facebookresearch/coconut](https://github.com/facebookresearch/coconut) | Background / contrast to injection pipeline |
