# Draft Plan: GPT-2 Small SAE Encodings for Medical Terms

---

## Phase 1 — Concept Selection

1. Select a focused subset of SNOMED CT concepts to start (e.g. 200–500 concepts from a single body system hierarchy, e.g. respiratory disorders)
2. For each concept collect:
   - Preferred term (e.g. "Asthma")
   - SNOMED CT code
   - Parent/child relationships (for ground truth distance matrix)
3. Filter to concepts that tokenise to a **single token** in GPT-2's vocabulary — multi-token concepts are harder to analyse because the representation is spread across multiple positions

---

## Phase 2 — Prompt Construction

Design prompts that place the medical term in a consistent, meaningful context so the model encodes it with clinical meaning rather than as a random string:

```
"The patient was diagnosed with {concept}."
"The clinical finding was {concept}."
"{concept} is a disorder of the respiratory system."
```

Run multiple prompt templates per concept to average out prompt-specific noise.

---

## Phase 3 — Activation Extraction (TransformerLens)

For each prompt, extract the residual stream activation at the **medical term's token position** at every layer (0–12):

```python
model = HookedTransformer.from_pretrained("gpt2")
logits, cache = model.run_with_cache(tokens)

for layer in range(12):
    activation = cache["resid_post", layer][0, token_position, :]
    # shape: [768]
```

Save per concept per layer per prompt → shape `[n_concepts, n_prompts, 13_layers, 768]`

---

## Phase 4 — SAE Encoding (SAELens)

Load the Bloom (2024) pre-trained SAEs for each of GPT-2 small's 12 layers and encode the saved activations:

```python
from sae_lens import SAE

sae, _, _ = SAE.from_pretrained(
    release="gpt2-small-res-jb",
    sae_id="blocks.{layer}.hook_resid_pre"
)

feature_activations = sae.encode(activation)
# shape: [24576] — sparse, most values zero
```

Result: for each concept at each layer, a 24576-dim sparse feature vector.

---

## Phase 5 — Geometric Analysis (per layer)

For each layer, build a matrix of concept representations and analyse geometry — following the Representation-Manifolds approach:

1. **Normalise** feature vectors to unit sphere
2. **PCA** to 3D for visualisation
3. **k-NN graph** → Dijkstra geodesic distances
4. **Compare** pairwise manifold distances to:
   - SNOMED CT ontological distances (is-a hierarchy depth)
   - text-embedding-3-large pairwise cosine distances (semantic oracle)
5. **Correlation metric** (Chatterjee or Pearson) to quantify alignment at each layer

---

## Phase 6 — Cross-Layer Analysis

Track how geometric structure evolves from layer 0 → layer 11:

- Does alignment with SNOMED CT increase with depth?
- Does alignment with text-embedding-3-large peak at a middle layer?
- At which layer does the strongest clustering by body system emerge?

---

## Deliverables

| Notebook | Purpose |
|---|---|
| `1-concept-selection.ipynb` | SNOMED CT concept filtering, tokenisation check, prompt generation |
| `2-extract-activations.ipynb` | TransformerLens forward passes, save residual stream per layer |
| `3-sae-encoding.ipynb` | Load Bloom SAEs, encode activations, save sparse feature vectors |
| `4-geometric-analysis.ipynb` | PCA, k-NN graph, geodesic distances, correlation with SNOMED CT and text-embedding-3-large |
| `5-cross-layer.ipynb` | Layer-by-layer comparison plots |

---

## Code Reuse from Reference Papers

### Phase 1 — Concept Selection
No reusable code — entirely new work specific to SNOMED CT.

### Phase 2 — Prompt Construction
No reusable code — the papers used raw Pile text, not structured prompts around specific terms.

### Phase 3 — Activation Extraction
**High reuse** from `Reference_Papers/MultiDimensionalFeatures/sae_multid_feature_discovery/generate_feature_occurence_data.py`:
- TransformerLens `run_with_cache()` pattern with `names_filter` for a specific layer hook point
- Batching loop and token flattening via `einops.rearrange`

Main change: instead of saving all token activations from the Pile, filter to only save activations at the **medical term's token position**.

### Phase 4 — SAE Encoding
**High reuse** from `Reference_Papers/MultiDimensionalFeatures/sae_multid_feature_discovery/utils.py`:

```python
get_gpt2_sae(device, layer)        # loads Bloom (2024) SAE for any GPT-2 layer
get_sae(device, model_name, layer) # unified router
```

The `SAE.from_pretrained("gpt2-small-res-jb", ...)` call is already wired up — drop-in reuse.

### Phase 5 — Geometric Analysis
**High reuse** from `Reference_Papers/Representation-Manifolds/utils.py`:

| Function | Used for |
|---|---|
| `knn_graph(X, k)` | Build k-NN graph over concept representations |
| `largest_connected_component(A)` | Ensure graph is connected before Dijkstra |
| `chatterjee_corr(x, y)` | Correlation between manifold distances and SNOMED CT distances |
| `interactive_3d_plot(...)` | 3D PCA visualisation per layer |
| `distance_plot(DX, DY, ...)` | Plot manifold distance vs SNOMED CT / text-embedding distances |

The entire `3-reproduce_figures.ipynb` notebook structure (normalise → PCA → k-NN → Dijkstra → distance_plot) is the template — the only change is substituting SNOMED CT distances for calendar distances.

### Phase 6 — Cross-Layer Analysis
**Medium reuse** — the distance correlation loop across layers is new, but all individual functions (`knn_graph`, `chatterjee_corr`, `distance_plot`) are reused from Phase 5.

### Summary

| Phase | Reuse | Source |
|---|---|---|
| Concept selection | None | — |
| Prompt construction | None | — |
| Activation extraction | High | `generate_feature_occurence_data.py` |
| SAE encoding | High | `utils.get_gpt2_sae()` |
| Geometric analysis | High | `Representation-Manifolds/utils.py` |
| Cross-layer analysis | Medium | Same utils, new loop |

---

## Open Questions to Resolve First

1. How many SNOMED CT concepts tokenise to a single GPT-2 token?
2. Which SNOMED CT hierarchy/body system to start with?
3. How to handle multi-token concept names — average across token positions, or use only the final token?
4. How many prompt templates per concept gives stable representations?
