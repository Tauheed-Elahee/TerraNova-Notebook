# The Origins of Representation Manifolds in Large Language Models

**Repo:** `Reference_Papers/Representation-Manifolds`

## Summary

Follow-on to Engels et al. (2025) that investigates *why* circular/manifold representations emerge in LLMs — tracing their origins rather than just documenting their existence.

## Key Contributions

- Reuses SAE activation data from Engels et al. for GPT-2 (layer 7) and Mistral-7B (layer 8) on periodic features (days of the week, months of the year, years of the 20th century).
- Augments with **text embeddings** from OpenAI `text-embedding-3-large` to study whether manifold structure is present in semantic embedding space independently of model internals.
- Reproduces and extends figures characterizing the geometry of representation manifolds to support theoretical claims about their formation.

## Relationship to MultiDimensionalFeatures

Engels et al. establishes *that* multi-dimensional circular features exist and are causally meaningful. This paper investigates *how and why* they arise — examining the origins of the manifold geometry.

## Pipeline

1. `1-process_sae_activations.ipynb` — Extract token activations via SAE (replicating Engels et al.)
2. `2-get_text_embeddings.ipynb` — Get OpenAI text embeddings for the same concept sets
3. `3-reproduce_figures.ipynb` — Reproduce all paper figures
