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

**Decision: `meta-llama/Meta-Llama-3-8B` (base)**

| Criterion | Status |
|---|---|
| TransformerLens support | Full — `HookedTransformer.from_pretrained("meta-llama/Meta-Llama-3-8B")` |
| Token Erasure probes | Pretrained on HF Hub for Llama-3-8B — no training sweep needed |
| Tuned Lens | Run `available_lens_artifacts()` at setup; train if no checkpoint exists |
| Base vs. instruct | Base — instruct RLHF artifacts distort residual stream geometry |
| Scientific question | Baseline: "does any LLM encode SNOMED structure?" — general model appropriate |

Alternatives ruled out: GPT-OSS-20B (MoE, no TransformerLens), BioMedLM (probes not pretrained, ~8h training sweep), Mistral-7B (no pretrained probes, no advantage over Llama-3-8B), Med42-70B (partial TransformerLens support).

---

## Stage 1 — Baseline Geometry

**Directory:** `src/stage1-baseline-geometry/`

**Goal:** Measure how much SNOMED ontological structure is implicitly encoded in frozen LLM residual stream representations.

### Notebooks

---

#### `0-model-setup.ipynb`

Load and verify the chosen model via TransformerLens before any layer calibration.

```python
from transformer_lens import HookedTransformer
model = HookedTransformer.from_pretrained(MODEL_NAME)
```

No Reference_Papers repos are needed here — TransformerLens is a pip package (`transformer-lens==2.3.0` in `requirements.txt`). Write `MODEL_NAME` to `src/config.py`.

**Memory and compatibility check (add before any forward passes):**
```python
import torch
d_model = model.cfg.d_model
n_layers = model.cfg.n_layers
n_concepts = 1879
max_tokens_per_concept = 50  # estimated upper bound for breast SNOMED terms
cache_bytes = n_concepts * max_tokens_per_concept * n_layers * d_model * 2  # fp16
print(f"d_model: {d_model}, layers: {n_layers}")
print(f"Estimated full cache: {cache_bytes / 1e9:.1f} GB")
print(f"Available VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
```
This guards against a costly late failure if the model doesn't fit. Stage 1 only needs activations at a single layer (`L_det`), so full-cache storage is not required — but the estimate surfaces any memory risk before calibration begins.

---

#### `0b-snomed-graph.ipynb`

Build the SNOMED CT IS-A `nx.DiGraph` from source files and save it as a shared prerequisite. This is required by two later steps: `ic_distances()` in Block A (condition 2) and the Poincaré training in Block C. Both fail without it, so it must run before `3-geometric-analysis.ipynb`.

**Input:** SNOMED CT RF2 release files — specifically the `sct2_Relationship_Snapshot_*.txt` file (available from SNOMED International or a national release centre). The relevant columns are `sourceId`, `destinationId`, `typeId`; IS-A edges have `typeId = 116680003`.

**Output:** `data/stage1/snomed_isa_graph.pkl` — a `networkx.DiGraph` where each node is a SNOMED concept ID (string) and each directed edge `(child, parent)` represents an IS-A relationship.

```python
import pandas as pd
import networkx as nx
import pickle

rel = pd.read_csv("path/to/sct2_Relationship_Snapshot.txt", sep="\t", dtype=str)
isa = rel[(rel["typeId"] == "116680003") & (rel["active"] == "1")]

G = nx.DiGraph()
G.add_edges_from(zip(isa["sourceId"], isa["destinationId"]))  # child → parent

with open("data/stage1/snomed_isa_graph.pkl", "wb") as f:
    pickle.dump(G, f)

print(f"Nodes: {G.number_of_nodes():,}, Edges: {G.number_of_edges():,}")
```

**Scope check:** restrict the saved graph to the subgraph reachable from the breast concept subset (ancestors of all concepts in `data/embeddings-concept-openai/concepts.csv`) to keep the pickle small. The full SNOMED IS-A graph has ~350k nodes; the breast hierarchy is a small fraction.

---

#### `1-layer-calibration.ipynb`

Two independent probes bracket the semantic core window. Both must run on the chosen model before extraction begins.

##### Token Erasure → find `L_det`
**Repo:** `Reference_Papers/footprints/` — [sfeucht/footprints](https://github.com/sfeucht/footprints)
**Reusability: CAN USE with new probes trained for target model**

| File | Function | Purpose | Reuse |
|---|---|---|---|
| `scripts/readout.py` | `get_doc_info(tokens, model, layer_start, layer_end, start_probes, end_probes, tokenizer)` | Runs probes across layer range; returns DataFrame of probdelta per token per layer | Direct |
| `scripts/readout.py` | `psi(doc_info, i, j)` | Computes erasure score for token span [i,j]: normalised probability delta | Direct |
| `scripts/readout.py` | `get_probe(layer, target_idx, model)` | Loads pretrained linear probe from HF Hub for a given layer/model | Needs new probes for target model |
| `scripts/training.py` | `train_epoch(epoch, probe, train_loader, ...)` / `test(probe, test_loader, ...)` | Train/evaluate probes from scratch on target model if pretrained not available | Direct |
| `scripts/training.py` | `class LinearModel(nn.Module)` | `nn.Linear(d_model, vocab_size)` — the probe architecture | Direct |

**Adaptation notes:**
- The repo uses `nnsight.LanguageModel`; the core erasure score functions (`psi`, `get_doc_info`) are model-agnostic but require probes trained for the specific model
- Check `sfeucht/footprints` on HF Hub first — pretrained probes exist for Llama-2-7b and Llama-3-8B. If the chosen model is not covered, train new probes:
  - **Training data:** Wikipedia sentences are the standard source; the repo's `data/` directory contains pre-split CSV files (`train.csv`, `val.csv`, `test.csv`) with `text` columns. For a new model, generate equivalent splits from any large text corpus.
  - **Training command:** `python scripts/train_probe.py --model <model_name> --layer <L> --target_idx -1` for each layer `L` from 0 to `n_layers`. Train a probe at each layer independently.
  - **Expected duration:** ~10–20 minutes per layer on a single GPU for a 7B model; full sweep across 32 layers ~8 hours. Run in parallel by layer if time is a constraint.
  - **Output path:** probes are saved to `data/probes/<model_name>/layer_<L>_target_<idx>.pt`; `get_probe()` in `readout.py` loads from this path.
- Run on ~50–100 breast SNOMED concepts; the layer with highest mean `psi` score across concept spans is `L_det`

##### Tuned Lens → find `L_pred`
**Repo:** `Reference_Papers/tuned-lens/` — [AlignmentResearch/tuned-lens](https://github.com/AlignmentResearch/tuned-lens)
**Reusability: CAN USE AS-IS if pretrained checkpoint available for chosen model; needs GPU training otherwise**

| File | Class / Function | Purpose | Reuse |
|---|---|---|---|
| `tuned_lens/nn/lenses.py` | `class TunedLens(Lens)` | Stores per-layer affine translators; `forward(h, idx)` → logits from hidden state at layer `idx` | Direct |
| `tuned_lens/nn/lenses.py` | `TunedLens.from_model_and_pretrained(model, lens_resource_id)` | Loads model + pretrained lens weights from HF Hub in one call | Direct |
| `tuned_lens/nn/lenses.py` | `TunedLens.transform_hidden(h, idx)` | Maps `h → translator[idx](h)` (the learned affine) | Direct |
| `tuned_lens/load_artifacts.py` | `load_lens_artifacts(resource_id, repo_id, ...)` | Fetches `config.json` + `params.pt` from HF Hub | Direct |
| `tuned_lens/load_artifacts.py` | `available_lens_artifacts(repo_id)` | Lists which models have pretrained lens checkpoints | Direct |

**Adaptation notes:**
- Check `available_lens_artifacts()` first — if the chosen model has a checkpoint, no training needed
- If not available: use `TunedLens.from_model(model)` and train with `tuned_lens/scripts/`
- `L_pred` = layer where `argmax(forward(h, L))` first matches `argmax(final_layer_logits)` across a sample of concept prompts
- **Fallback:** The `mat` repo (`Reference_Papers/mat/aux.py` → `linreg(x, y)`) implements the same idea with sklearn: fit a linear map between layer `L` and final layer representations, track R² by layer — the layer where R² plateaus is `L_pred`. Requires no pretrained checkpoints.

##### Save calibration results
```python
# data/stage1/layer_boundaries.json
{"L_det": 12, "L_pred": 20, "model": "...", "failure_rate_pct": 18.4}
```

---

#### `2-concept-extraction.ipynb`

Extract hidden states at `L_det` for all 1,879 breast concepts using two co-primary methods.

**No Reference_Papers repos required** — uses TransformerLens hooks directly:

```python
# Method A: last-token hidden state
_, cache = model.run_with_cache(tokens)
h_last = cache[f"blocks.{L_det}.hook_resid_post"][:, -1, :]

# Method B: mean-pool over all token positions
h_mean = cache[f"blocks.{L_det}.hook_resid_post"].mean(dim=1)
```

**SNOMED→OMOP mapping (required for Block B in notebook 3):**

Block B uses KEEP embeddings which are indexed by OMOP concept codes, not SNOMED CT IDs. Produce the mapping here so it is ready before `3-geometric-analysis.ipynb` runs.

```python
# Query OMOP CDM vocabulary (Athena: https://athena.ohdsi.org)
# Download CONCEPT.csv from Athena, filter to vocabulary_id = 'SNOMED'.
import pandas as pd

concept = pd.read_csv("path/to/CONCEPT.csv", sep="\t", dtype=str)
snomed = concept[concept["vocabulary_id"] == "SNOMED"][["concept_code", "concept_id"]]
# concept_code = SNOMED CT ID, concept_id = OMOP concept_id

concepts_df = pd.read_csv("data/embeddings-concept-openai/concepts.csv", dtype=str)
mapping = concepts_df.merge(snomed, left_on="conceptId", right_on="concept_code", how="left")
mapping[["conceptId", "concept_id"]].to_csv("data/stage1/snomed_omop_map.csv", index=False)
print(f"Mapped: {mapping['concept_id'].notna().sum()} / {len(mapping)} concepts")
```

Concepts without an OMOP mapping are excluded from Block B; document the coverage rate. Athena is freely available and covers the full SNOMED→OMOP mapping without manual curation.

**Optional — information-theoretic layer validation:**
**Repo:** `Reference_Papers/information_flow/` — [OFSkean/information_flow](https://github.com/OFSkean/information_flow)
**Reusability: CAN USE AS-IS**

| File | Function | Purpose | Reuse |
|---|---|---|---|
| `experiments/utils/metrics/metric_functions.py` | `compute_dime(hidden_states, alpha=1)` | DIME score per layer: diversity of representations across concept names | Direct |
| `experiments/utils/metrics/metric_functions.py` | `compute_infonce(hidden_states, temperature=0.1)` | InfoNCE loss per layer: contrastive discriminability of concept representations | Direct |
| `experiments/utils/metrics/metric_functions.py` | `normalize(R)` | L2 normalization: `(R - mean) / ||R||` | Direct |

Use these to confirm that `L_det` (from Token Erasure) coincides with the information peak — if it does, the calibration is consistent across two independent methods.

---

#### `3-geometric-analysis.ipynb`

The primary scientific notebook. Five analysis blocks.

##### Block A — Distance correlation

Compute pairwise cosine distances in residual stream space and correlate with SNOMED ontological distances under two conditions (shortest-path and IC-based).

**Primary source: `src/concept-openai-embeddings/utils.py`** — all the functions needed here already exist from Experiment 01. `Representation-Manifolds/utils.py` covers the same ground and can be used as a cross-check, but the existing file is the authoritative source to avoid duplication.

| File | Function | Covers |
|---|---|---|
| `src/concept-openai-embeddings/utils.py` | `knn_graph(X, k)` | k-NN graph on embedding matrix |
| `src/concept-openai-embeddings/utils.py` | `largest_connected_component(A)` | LCC mask before geodesic distance computation |
| `src/concept-openai-embeddings/utils.py` | `chatterjee_corr(x, y)` | Robust rank correlation ξ |
| `src/concept-openai-embeddings/utils.py` | `distance_plot(DX, DY, labels, corr_coef='chatterjee')` | Distance scatter with correlation annotation |
| `src/concept-openai-embeddings/utils.py` | `interactive_3d_plot(...)`, `interactive_3d_plot_by_tag(...)` | Plotly 3D PCA visualizations |

**Gap — IC-based SNOMED distance (condition 2):** `data/embeddings-concept-openai/ontological_distances.csv` only contains shortest-path distances. `keep/utils.py:calculate_all_similarities()` computes Resnik/Lin IC-based similarity but requires OMOP concept codes; the project works with SNOMED CT IDs directly. IC distances must be computed from the SNOMED IS-A graph — this is one of the two functions in the custom file (see below).

**Key pattern** (mirrors existing `3-geometric-analysis.ipynb` in Experiment 01):
```python
from scipy.spatial.distance import squareform, pdist
from scipy.sparse.csgraph import dijkstra

# Cosine distance matrix
DX_cosine = squareform(pdist(hidden_states, metric="cosine"))

# Geodesic (manifold) distance matrix
A = knn_graph(hidden_states, k=10)
lcc_mask = largest_connected_component(A)
DX_geo = dijkstra(A[lcc_mask][:, lcc_mask])

# Correlation with SNOMED shortest-path distances
DY = ontological_distances[lcc_mask][:, lcc_mask]
fig, ax = distance_plot(DX_geo, DY, labels, corr_coef='chatterjee')
```

##### Block B — Three-way comparison (KEEP, OpenAI, LLM)

**Repo:** `Reference_Papers/keep/` — [G2Lab/keep](https://github.com/G2Lab/keep)
**Reusability: CAN USE AS-IS for loading embeddings; KEEP uses OMOP codes, cross-reference with SNOMED codes needed**

| File | Function | Purpose | Reuse |
|---|---|---|---|
| `pretrained_embeddings/get_embeddings.py` | `extract_embeddings(omop_codes, tokenizer, model, omop_embedding, model_type)` | Loads KEEP embeddings indexed by OMOP code | Direct |
| `pretrained_embeddings/get_embeddings.py` | `dict_to_indexed_array(embedding_dict)` | Converts `{code: vector}` dict to numpy array | Direct |
| `utils.py` | `semantic_sim_correlation(semantic_similarities, embedding_tensor, cats, K1, K2, code_dict, ...)` | Pearson correlation between semantic similarity and cosine similarity | Direct |
| `utils.py` | `calculate_all_similarities(G, concept_pairs, similarity_type='both')` | Resnik/Lin IC-based similarity from SNOMED hierarchy graph | Direct |

**Adaptation note:** KEEP uses OMOP concept codes; `data/embeddings-concept-openai/concepts.csv` uses SNOMED CT IDs. The mapping is produced in `2-concept-extraction.ipynb` and saved to `data/stage1/snomed_omop_map.csv`. Concepts without an OMOP match are excluded from this block.

Run the same `distance_plot()` / `chatterjee_corr()` pipeline on KEEP vectors and `data/embeddings-concept-openai/embeddings_normalised.csv` (OpenAI, already computed) against the same SNOMED distance matrix to produce the three-way comparison.

##### Block C — Hyperbolic geometry tests

**Repo:** `Reference_Papers/Snomed2Vec/` — [agarwal.khushbu/Snomed2Vec](https://gitlab.com/agarwal.khushbu/Snomed2Vec)
**Reusability: REFERENCE — use gensim Poincaré API to load pretrained vectors for ordinal comparison**

| File | Function | Purpose | Reuse |
|---|---|---|---|
| `src/embedding_learning/poincare.py` | `load_snomed_isa_relations(path)` | Load SNOMED IS-A pairs for Poincaré training | Reference |
| `src/embedding_learning/poincare.py` | `get_poincare_model(relations, emb_size)` | Train Poincaré model on SNOMED hierarchy | Reference |
| gensim API | `model.kv.distance(c1, c2)` | Poincaré distance between two concepts | Direct (gensim) |
| gensim API | `model.kv.norm(concept)` | Hierarchical position (0 = root, 1 = leaf) | Direct (gensim) |

**Step 1 — Train Poincaré embeddings (prerequisite for test 3):**

No public pretrained Poincaré vectors for SNOMED CT exist. Train from the IS-A graph built in `0b-snomed-graph.ipynb`.

```python
import pickle
from Reference_Papers.Snomed2Vec.src.embedding_learning.poincare import get_poincare_model

with open("data/stage1/snomed_isa_graph.pkl", "rb") as f:
    G = pickle.load(f)
relations = [(str(u), str(v)) for u, v in G.edges()]  # (child, parent) pairs

if not os.path.exists("data/stage1/snomed_poincare.model"):
    model_poincare = get_poincare_model(relations, emb_size=100)
    model_poincare.save("data/stage1/snomed_poincare.model")
```

Expected duration: ~5–15 minutes on CPU for the breast-concept subgraph (~few thousand nodes).

**Step 2 — Run tests:**
1. **Gromov δ-hyperbolicity** — not in any Reference_Papers repo or pip package. Implemented in the custom file as `gromov_delta(D, sample_size=500)` (see below).
2. **UMAP with hyperbolic metric** — `umap-learn` pip package (already in `requirements.txt`): `umap.UMAP(output_metric='hyperboloid').fit_transform(hidden_states)`. No custom code needed.
3. **Ordinal comparison with Snomed2Vec** — load trained model and compare pairwise Poincaré distances against pairwise LLM cosine distances via Spearman ρ. Uses gensim API directly:
   ```python
   from gensim.models.poincare import PoincareModel
   poincare = PoincareModel.load("data/stage1/snomed_poincare.model")
   poincare_dist = lambda c1, c2: poincare.kv.distance(c1, c2)
   ```
4. **Hyperbolic probing classifier** — inline in notebook using `geoopt` (pip): logistic regression in hyperbolic space to predict ancestor/descendant membership.

##### Block D — SAE clustering and causal validation (optional)

**Repo:** `Reference_Papers/MultiDimensionalFeatures/` — [Tauheed-Elahee/MultiDimensionalFeatures](https://github.com/Tauheed-Elahee/MultiDimensionalFeatures)
**Reusability: CAN USE AS-IS for clustering; NEEDS ADAPTATION for causal validation (assumes circular manifolds)**

| File | Function | Purpose | Reuse |
|---|---|---|---|
| `sae_multid_feature_discovery/clustering.py` | `graph_cluster_sims(all_sims, top_k_for_graph=2, sim_cutoff=0.5)` | Graph-based clustering of SAE feature vectors by cosine similarity | Direct |
| `sae_multid_feature_discovery/clustering.py` | `spectral_cluster_sims(all_sims, n_clusters=1000)` | Spectral clustering on similarity matrix | Direct |
| `sae_multid_feature_discovery/saes/sparse_autoencoder.py` | `SparseAutoencoder.load_from_pretrained(path)` / `.W_dec` | Load SAE; access decoder weight matrix `(d_sae, d_in)` as feature basis | Direct |
| `intervention/circle_finding_utils.py` | `do_regression(task, explanatory_vecs, target) → (r², residuals, ...)` | Linear regression of hidden states onto candidate basis vectors | Direct |

**Adaptation note:** `find_c_circle()` assumes circular manifold structure (days/months). For SNOMED's DAG hierarchy, replace with a tree-structured basis: ancestor-depth features, information-content vectors, or one-hot hierarchy-level indicators. The `do_regression()` function itself is generic — only the basis vectors change.

**Repo:** `Reference_Papers/concept_das/` — [colored-dye/concept_das](https://github.com/colored-dye/concept_das)
**Reusability: NEEDS ADAPTATION — retarget contrast pairs from refusal/helpfulness to SNOMED parent/child concept pairs**

| File | Function | Purpose | Reuse |
|---|---|---|---|
| `cdas/models/cdas_model.py` | `CDASModel.train(examples)` | Trains low-rank subspace that separates concept pairs via JS divergence | Adapt |
| `cdas/utils/model_utils.py` | `gather_residual_activations(model, tokenizer, texts, layer)` | Extract residual stream activations at `layer` for a list of texts | Direct |
| `cdas/models/das_vector.py` | `class DASVector` | Rank-1 distributed concept subspace; `make_model(mode, low_rank_dimension)` | Adapt |

To adapt: replace refusal/helpfulness contrast pairs with SNOMED concept pairs — e.g., `("invasive ductal carcinoma", "carcinoma in situ")` as positive/negative for a `malignancy` concept axis.

---

##### Block E — Verification (final cell)

Add as the last cell of `3-geometric-analysis.ipynb`. Asserts the expected outcomes and writes a machine-readable summary so results are reproducible and comparable across model choices.

```python
import json, warnings

results = {
    "model": MODEL_NAME,
    "L_det": L_DET,
    "L_pred": L_PRED,
    "spearman_rho_last_token_shortestpath": float(rho_last_shortestpath),
    "spearman_rho_mean_pool_shortestpath": float(rho_mean_shortestpath),
    "spearman_rho_last_token_ic": float(rho_last_ic),
    "spearman_rho_mean_pool_ic": float(rho_mean_ic),
    "method_agreement": abs(rho_last_shortestpath - rho_mean_shortestpath) < 0.05,
    "gromov_delta": float(delta),
    "n_concepts_lcc": int(lcc_mask.sum()),
}

# Expected range check (design document: ρ ~ 0.2–0.4 for well-attested subset)
rho_primary = results["spearman_rho_last_token_shortestpath"]
if not (0.05 < rho_primary < 0.6):
    warnings.warn(f"ρ = {rho_primary:.3f} is outside expected range (0.05–0.6)")

if not results["method_agreement"]:
    warnings.warn("Last-token and mean-pool extraction disagree by > 0.05 — investigate")

with open("data/stage1/verification_summary.json", "w") as f:
    json.dump(results, f, indent=2)
print("Verification summary written to data/stage1/verification_summary.json")
```

---

### Custom file: `src/stage1-baseline-geometry/utils.py`

Two functions are needed that no Reference_Papers repo provides and no pip package covers directly. Everything else in Stage 1 is served by `src/concept-openai-embeddings/utils.py` (existing), Reference_Papers repos, or pip packages.

```python
# src/stage1-baseline-geometry/utils.py

def gromov_delta(D, sample_size=500, seed=42):
    """Gromov δ-hyperbolicity via the four-point condition.

    For a random sample of 4-tuples (a, b, c, d) from the concept set,
    compute the three sums:
        S1 = d(a,b) + d(c,d)
        S2 = d(a,c) + d(b,d)
        S3 = d(a,d) + d(b,c)
    Sort descending; δ = (S1_max - S2_median) / 2.
    A δ close to 0 indicates hyperbolic geometry.

    Args:
        D: np.ndarray (n, n) pairwise distance matrix
        sample_size: number of random 4-tuples to sample
        seed: random seed

    Returns:
        float — mean δ across sampled 4-tuples
    """
    ...

def ic_distances(snomed_graph, concepts, method='resnik'):
    """Pairwise IC-based distances for a set of SNOMED concepts.

    Computes information content (IC) from concept frequency in the
    IS-A hierarchy, then applies Resnik or Lin similarity to all pairs.
    Uses the SNOMED hierarchy graph (NetworkX DiGraph of IS-A edges).

    Args:
        snomed_graph: nx.DiGraph — IS-A edges from SNOMED CT
        concepts: list of SNOMED concept IDs
        method: 'resnik' (IC of LCS) or 'lin' (normalised by IC sum)

    Returns:
        np.ndarray (n, n) — pairwise IC-based distance matrix
                            (1 - similarity, so 0 = identical)
    """
    ...
```

**Why not reuse KEEP's `calculate_all_similarities()`:** that function requires OMOP concept codes and a pre-built OMOP hierarchy graph. The project works with SNOMED CT IDs directly (from `data/embeddings-concept-openai/concepts.csv`), so the SNOMED→OMOP mapping would be needed before KEEP's function could be used. For a clean Stage 1 baseline, computing IC directly on the SNOMED hierarchy avoids that dependency.

**Implementation status:** Both functions are stubs (`...`) and must be implemented before `3-geometric-analysis.ipynb` runs. Both are pure NumPy/NetworkX — no new dependencies required beyond what is already in `requirements.txt`.

---

### Data outputs
```
data/stage1/
  snomed_isa_graph.pkl            # nx.DiGraph of IS-A edges (from 0b-snomed-graph.ipynb)
  snomed_omop_map.csv             # SNOMED CT ID → OMOP concept_id (from 2-concept-extraction.ipynb)
  snomed_poincare.model           # Trained gensim Poincaré model (from 3-geometric-analysis.ipynb Block C)
  layer_boundaries.json           # L_det, L_pred, model, failure_rate_pct
  hidden_states_last_token.npy    # (1879, d_model)
  hidden_states_mean_pool.npy     # (1879, d_model)
  pairwise_distances.csv          # cosine + geodesic distances
  correlation_results.csv         # Spearman ρ: all conditions × both methods
  keep_embeddings.npy             # KEEP vectors for OMOP-mapped concepts
  verification_summary.json       # ρ values, method agreement, δ, n_concepts_lcc
  plots/
    distance_scatter_llm.png
    distance_scatter_keep.png
    distance_scatter_openai.png   # from data/embeddings-concept-openai/embeddings_normalised.csv
    umap_hyperbolic.html
    interactive_3d.html
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
- Reuse `src/concept-openai-embeddings/utils.py` and `src/stage1-baseline-geometry/utils.py` throughout

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
MODEL_NAME = "meta-llama/Meta-Llama-3-8B"   # base model (decided 2026-03-25)
L_DET = None           # Set after layer calibration (Stage 1 notebook 1)
L_PRED = None          # Set after layer calibration (Stage 1 notebook 1)
CONCEPT_CSV = "data/embeddings-concept-openai/concepts.csv"
ONTOLOGY_DISTANCES_CSV = "data/embeddings-concept-openai/ontological_distances.csv"
```

### Reuse from Experiment 01

| Asset | Path | Used in |
|---|---|---|
| Concept list | `data/embeddings-concept-openai/concepts.csv` | Stages 1, 2 |
| SNOMED distances | `data/embeddings-concept-openai/ontological_distances.csv` | Stages 1, 2 |
| OpenAI embeddings | `data/embeddings-concept-openai/embeddings_normalised.csv` | Stage 1 comparison |
| Graph + viz utilities | `src/concept-openai-embeddings/utils.py` | Stages 1, 2 |

### Final `src/` structure
```
src/
  config.py
  concept-openai-embeddings/       # Existing (Experiment 01)
  stage1-baseline-geometry/
    0-model-setup.ipynb
    0b-snomed-graph.ipynb
    1-layer-calibration.ipynb
    2-concept-extraction.ipynb
    3-geometric-analysis.ipynb
    utils.py                         # gromov_delta(), ic_distances()
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

### Core pipeline

| arXiv | Paper | GitHub | In `Reference_Papers/` | Used in |
|---|---|---|---|---|
| 2406.20086 | Token Erasure | [sfeucht/footprints](https://github.com/sfeucht/footprints) | ✓ `footprints` | Stage 1 — locate `L_det` |
| 2303.08112 | Tuned Lens | [AlignmentResearch/tuned-lens](https://github.com/AlignmentResearch/tuned-lens) | ✓ `tuned-lens` | Stage 1 — locate `L_pred` |
| 2410.05864 | Tokens2Words | [schwartz-lab-NLP/Tokens2Words](https://github.com/schwartz-lab-NLP/Tokens2Words) | ✓ `Tokens2Words` | Stage 1 — layer calibration reference |
| 2508.17953 | Subword Compositionality | — (no public repo) | — | Stage 1 — extraction method B (mean-pool) |
| 2510.05049 | KEEP | [G2Lab/keep](https://github.com/G2Lab/keep) | ✓ `keep` | Stage 1 — three-way comparison baseline |
| 1907.08650 | Snomed2Vec | [agarwal.khushbu/Snomed2Vec](https://gitlab.com/agarwal.khushbu/Snomed2Vec) (GitLab) | ✓ `Snomed2Vec` | Stage 1 — hyperbolic geometry reference |
| 2505.20133 | Token Distillation | [konstantinjdobler/token-distillation](https://github.com/konstantinjdobler/token-distillation) | ✓ `token-distillation` | Stage 2 — new embedding training |
| 2502.13063 | Cramming | [yurakuratov/hidden_capacity](https://github.com/yurakuratov/hidden_capacity) | ✓ `hidden_capacity` | Stage 2 — alternative for long concept names |
| 2502.04397 | MedTok | [mims-harvard/MedTok](https://github.com/mims-harvard/MedTok) | ✓ `MedTok` | Stage 3 — ontology-supervised encoder |
| 2412.06769 | Coconut | [facebookresearch/coconut](https://github.com/facebookresearch/coconut) | ✓ `coconut` | Background — contrast to injection pipeline |

### Geometric analysis & layer theory

| arXiv | Paper | GitHub | In `Reference_Papers/` | Used in |
|---|---|---|---|---|
| 2405.14860 | Not All LM Features Are Linear | [Tauheed-Elahee/MultiDimensionalFeatures](https://github.com/Tauheed-Elahee/MultiDimensionalFeatures) | ✓ `MultiDimensionalFeatures` | Stage 1 — SAE clustering, causal validation |
| 2505.18235 | Origins of Representation Manifolds | [alexandermodell/Representation-Manifolds](https://github.com/alexandermodell/Representation-Manifolds) | ✓ `Representation-Manifolds` | Stage 1 — manifold geometry cross-check |
| 2412.07334 | Frame Representation Hypothesis | [phvv-me/frame-representation-hypothesis](https://github.com/phvv-me/frame-representation-hypothesis) | ✓ `frame-representation-hypothesis` | Background — multi-token concept representation |
| 2303.09435 | Jump to Conclusions (mat) | [sashayd/mat](https://github.com/sashayd/mat) | ✓ `mat` | Stage 1 — `L_pred` fallback (linear shortcut R²) |
| 2502.02013 | Layer by Layer | [OFSkean/information_flow](https://github.com/OFSkean/information_flow) | ✓ `information_flow` | Stage 1 — layer selection; semantic peak |
| 2412.08563 | Does Representation Matter | — (no public repo) | — | Stage 1 — entropy method for semantic layer ID |
| 2507.04886 | Emergent Semantics Beyond Token Embeddings | [AVBochkov/Embeddings](https://github.com/AVBochkov/Embeddings) | ✓ `Embeddings` | Background — supports injection framing |
| 2510.04861 | Hidden Geometry in Transformers | — (no public repo) | — | Stage 1 — positional/contextual subspace |
| 2603.03031 | Step-Level Sparse Autoencoder | — (no public repo) | — | Stage 1 — SAE layer analysis (optional) |
| 2505.16950 | Bottlenecked Transformers | — (no public repo) | — | Background — middle-layer KV consolidation |
| 2510.14095 | OOD Generalisation via Latent Reasoning | [Awni00/algorithmic-generalization-transformer-architectures](https://github.com/Awni00/algorithmic-generalization-transformer-architectures) | ✓ `algorithmic-generalization-transformer-architectures` | Background — discrete middle-layer bottleneck |
| 2411.18339 | Ridge Regression for Manifold-Valued Time Series | — (no public repo) | — | Stage 1 — Riemannian regression reference |

### SAE & monosemanticity

| arXiv | Paper | GitHub | In `Reference_Papers/` | Used in |
|---|---|---|---|---|
| 2309.08600 | Sparse Autoencoders (Cunningham et al.) | — (no public repo) | — | Stage 1 — SAE decomposition foundation |
| 2506.19382 | Measuring and Guiding Monosemanticity | [ml-research/measuring-and-guiding-monosemanticity](https://github.com/ml-research/measuring-and-guiding-monosemanticity) | ✓ `measuring-and-guiding-monosemanticity` | Stage 1 — SAE feature quality metrics |
| 2501.06254 | PS-Eval | [gouki510/PS-Eval](https://github.com/gouki510/PS-Eval) | ✓ `PS-Eval` | Stage 1 — SAE evaluation by layer/polysemy |
| 2501.19066 | Concept Steerers | [kim-dahye/steerers](https://github.com/kim-dahye/steerers) | ✓ `steerers` | Background — SAE-based concept steering |
| 2412.04139 | Monet | [dmis-lab/Monet](https://github.com/dmis-lab/Monet) | ✓ `Monet` | Background — monosemantic MoE architecture |
| 2601.21420 | ConceptMoE | [ZihaoHuang-notabot/ConceptMoE](https://github.com/ZihaoHuang-notabot/ConceptMoE) | ✓ `ConceptMoE` | Background — adaptive token-to-concept compression |
| 2602.05234 | Faithful Bi-Directional Steering (CDAS) | [colored-dye/concept_das](https://github.com/colored-dye/concept_das) | ✓ `concept_das` | Stage 1 — causal validation of concept subspaces |

### Activation steering

| arXiv | Paper | GitHub | In `Reference_Papers/` | Used in |
|---|---|---|---|---|
| 2509.06608 | Small Vectors, Big Effects | [corl-team/steering-reasoning](https://github.com/corl-team/steering-reasoning) | ✓ `steering-reasoning` | Background — middle-layer steering site |
| 2505.12584 | Multilingual Steering | [antonisa/lang2vec](https://github.com/antonisa/lang2vec) | ✓ `lang2vec` | Background — language-agnostic representations |
| 2602.04428 | Fine-Grained Activation Steering (AUSteer) | [zijian678/AUSteer](https://github.com/zijian678/AUSteer) | ✓ `AUSteer` | Background — sub-neuron concept targeting |
| 2602.04935 | ASA | — (no public repo) | — | Background — middle-layer failure detection |
| 2503.10679 | LinEAS | [apple/ml-lineas](https://github.com/apple/ml-lineas) | ✓ `ml-lineas` | Background — optimal steering depth |

### Concept-space architectures

| arXiv | Paper | GitHub | In `Reference_Papers/` | Used in |
|---|---|---|---|---|
| 2412.08821 | Large Concept Models | [facebookresearch/large_concept_model](https://github.com/facebookresearch/large_concept_model) | ✓ `large_concept_model` | Background — explicit concept space architecture |
| 2508.05305 | SONAR-LLM | [FusionBrainLab/SONAR-LLM](https://github.com/FusionBrainLab/SONAR-LLM) | ✓ `SONAR-LLM` | Background — closest analogue to semantic core pipeline |
| 2512.24617 | Dynamic Large Concept Models | — (no public repo) | — | Background — adaptive concept merging |

### Clinical / medical NLP

| arXiv | Paper | GitHub | In `Reference_Papers/` | Used in |
|---|---|---|---|---|
| PMC10865208 | NLP of Referral Letters | — | — | Background |
| polymtl_67792 | Ontology-Constrained Generation | — | — | Background |
| PMC8388183 | Disease Trajectories from EHR | — | — | Background |
| acm_3650784 | AscleAI | — | — | Background |
| 2506.04831 | EHR2Path | — | — | Background |
| sage_1557_1390 | ICD-10 KG CoT | — | — | Background |

---

## GitHub Issue Mapping

| Plan Item | Issue |
|---|---|
| **Prerequisite: Model Selection** | [#2](https://github.com/Tauheed-Elahee/TerraNova-Notebook/issues/2) — `[Prerequisite] Model selection` |
| **Stage 1** (parent) | [#13](https://github.com/Tauheed-Elahee/TerraNova-Notebook/issues/13) — `[Stage 1] Baseline Geometry` |
| `0-model-setup.ipynb` | [#3](https://github.com/Tauheed-Elahee/TerraNova-Notebook/issues/3) — `[Stage 1] 0-model-setup.ipynb` |
| `0b-snomed-graph.ipynb` | [#4](https://github.com/Tauheed-Elahee/TerraNova-Notebook/issues/4) — `[Stage 1] 0b-snomed-graph.ipynb` |
| `utils.py` — `gromov_delta()` + `ic_distances()` | [#5](https://github.com/Tauheed-Elahee/TerraNova-Notebook/issues/5) — `[Stage 1] Implement gromov_delta() and ic_distances()` |
| `1-layer-calibration.ipynb` | [#6](https://github.com/Tauheed-Elahee/TerraNova-Notebook/issues/6) — `[Stage 1] 1-layer-calibration.ipynb` |
| `2-concept-extraction.ipynb` | [#7](https://github.com/Tauheed-Elahee/TerraNova-Notebook/issues/7) — `[Stage 1] 2-concept-extraction.ipynb` |
| `3-geometric-analysis.ipynb` | [#8](https://github.com/Tauheed-Elahee/TerraNova-Notebook/issues/8) — `[Stage 1] 3-geometric-analysis.ipynb` |
| **Stage 2** (parent) | [#14](https://github.com/Tauheed-Elahee/TerraNova-Notebook/issues/14) — `[Stage 2] Vocabulary Expansion` |
| `1-token-distillation.ipynb` (Stage 2) | [#9](https://github.com/Tauheed-Elahee/TerraNova-Notebook/issues/9) — `[Stage 2] 1-token-distillation.ipynb` |
| `2-concept-extraction.ipynb` (Stage 2) | [#10](https://github.com/Tauheed-Elahee/TerraNova-Notebook/issues/10) — `[Stage 2] 2-concept-extraction.ipynb` |
| `3-geometric-analysis.ipynb` (Stage 2) | [#11](https://github.com/Tauheed-Elahee/TerraNova-Notebook/issues/11) — `[Stage 2] 3-geometric-analysis.ipynb` |
| **Stage 3** (parent) | [#15](https://github.com/Tauheed-Elahee/TerraNova-Notebook/issues/15) — `[Stage 3] Ontology-Supervised Geometry` |
| `stage3/README.md` | [#12](https://github.com/Tauheed-Elahee/TerraNova-Notebook/issues/12) — `[Stage 3] README.md` |
