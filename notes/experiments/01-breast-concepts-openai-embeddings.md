# Exp 01 — Breast Concepts, OpenAI text-embedding-3-large

**Search term:** `"breast"` (1 879 concepts across all semantic tags)
**Date:** 2026-03-24

## Hypothesis

SNOMED CT ontological distance should correlate with geometric distance in the
embedding space — concepts that are semantically close in the hierarchy (e.g.,
two disorders of the nipple) should cluster together, while distant concepts
(e.g., a breast disorder vs. a breast-related organism) should be far apart.

## Method

- **Notebook 1** — Retrieved all active SNOMED CT concepts matching the term
  `"breast"` via the Snowstorm API; computed pairwise ontological distances
  using LCA approximation over the IS-A hierarchy.
  Output: `data/concepts.csv`, `data/ontological_distances.csv`.
- **Notebook 2** — Embedded each concept's preferred term with
  `text-embedding-3-large` (3 072 dims); normalised to the unit sphere.
  Output: `data/embeddings_normalised.csv`.
- **Notebook 3** — Built a 5-NN graph from the normalised embeddings; extracted
  the largest connected component (LCC); computed geodesic distances (Dijkstra)
  and cosine similarities; correlated both against SNOMED ontological distances;
  visualised with interactive 3-D PCA plots coloured by semantic tag.

## Results

| Metric | Value |
|--------|-------|
| Concepts retrieved | 1 879 |
| Concepts in LCC (k=5) | 1 777 / 1 879 (8 components) |
| PCA variance (PC1–PC3) | 16.39 % |
| Pearson ρ (manifold vs ontological, d<30) | ~0.30 |
| Chatterjee ξ (cosine sim vs ontological²) | — (not printed; see plot) |

Key plots: `data/plot_manifold_vs_ontological.png`,
`data/plot_cosine_vs_ontological.png`,
`data/interactive_3d_by_tag.html`.

## Interpretation

A moderate positive correlation (ρ ≈ 0.30) between geodesic manifold distance
and SNOMED ontological distance suggests the embedding space does partially
encode the ontology, but substantial variance is unexplained. The low PCA
variance (16 % in 3 components) confirms the concept cloud is high-dimensional
and not well described by a simple low-rank manifold. Semantic tags form loose
clusters rather than clean separations in 3-D PCA.

## Open Questions

- What correlation do we get using a medical-domain model (e.g. BioMedLM)
  instead of the general-purpose `text-embedding-3-large`?
- Does ρ improve if we restrict to a single semantic tag (e.g. disorders only)?
- Can an SAE trained on a residual stream layer recover features that align
  with SNOMED semantic tags?
- How does correlation change layer-by-layer through an LLM's residual stream?
