---
title: Layer-Wise Concept Geometry and the Detokenisation Phase Transition
tags: [geometry, layers, detokenization, phase-transition, SNOMED, manifold, residual-stream, correlation]
summary: How the detokenisation phase transition in early-to-middle layers creates a meaningful extraction point for concept geometry analysis, and why the layer at which detokenisation completes is hypothesised to be where SNOMED ontological structure is best reflected in the residual stream.
papers: [2410.05864, 2406.20086, 2405.14860, 2505.18235]
---

# Layer-Wise Concept Geometry and the Detokenisation Phase Transition

## The Phase Transition

The detokenisation process is not uniform across layers — it concentrates in early-to-middle layers (~8–15 for mid-sized models).[^1] This creates a natural phase transition in the residual stream:

```
Layers 0–7:   fragmented sub-word representations
Layer ~12:    detokenisation complete — unified concept vector
Layers 12–N:  task-specific semantic reasoning, next-token prediction
```

The token erasure effect[^2] marks the transition point: at the layer where erasure of preceding sub-token identity is maximal, the last-token hidden state most cleanly carries the whole-concept representation.

## The Research Question

This phase transition sharpens the project's central question beyond simple correlation analysis:

> *At which layer does the residual stream geometry best reflect SNOMED CT ontological distances, and does this coincide with the layer where detokenisation completes?*

If the two align — if geometric structure becomes most ontologically coherent exactly at the layer where the model has assembled the concept — this suggests ontological organisation is encoded in the concept-level representation itself, not in downstream task-specific processing.

## Connection to the Manifold Papers

Engels et al.[^3] showed that periodic features (days, months, years) form circular manifolds at specific layers (GPT-2 layer 7, Mistral-7B layer 8). Modell et al.[^4] investigated why those manifolds arise. Neither paper studied medical concepts or multi-token terms. The detokenisation literature provides the missing methodological piece: a principled way to extract concept-level vectors from multi-token medical terms, enabling the same layer-wise manifold analysis to be applied to SNOMED CT.

## Proposed Extraction Protocol

```python
concept_layer_vectors = {}

for concept in snomed_concepts:
    tokens = tokenizer(concept["preferred_term"], return_tensors="pt")
    _, cache = model.run_with_cache(tokens)

    # Extract last-token hidden state at every layer
    concept_layer_vectors[concept["id"]] = {
        layer: cache["resid_post", layer][0, -1, :].detach()
        for layer in range(model.cfg.n_layers)
    }

# For each layer: compute pairwise manifold distances
# Compare against SNOMED ontological distances
# Track Pearson / Chatterjee correlation across layers
```

## Expected Correlation Profile

A correlation curve across layers with structure roughly as follows:

- **Very early layers**: low correlation — representations are fragmented sub-word tokens, not concept-level
- **Detokenisation zone (~layers 8–15)**: rising correlation — concept-level representation forming
- **Peak**: at or just after detokenisation completes
- **Later layers**: potentially declining as representations become increasingly task-specific (next-token prediction) and diverge from ontological structure

The location of the peak relative to the detokenisation completion point is the empirical finding of interest.

---

[^1]: R. Kaplan, S. Oren, U. Reif, and R. Schwartz, "From Tokens to Words: On the Inner Lexicon of LLMs," in *Proc. ICLR*, 2025. [[2410_05864_from-tokens-to-words-on-the-inner-lexicon-of-llms|↗]]
[^2]: S. Feucht, T. Atkinson, E. Wallace, and D. Bau, "Token Erasure as a Footprint of Implicit Vocabulary Items in LLMs," in *Proc. EMNLP*, 2024. [[2406_20086_token-erasure-as-a-footprint-of-implicit-vocabulary-items-in-llms|↗]]
[^3]: J. Engels, I. Liao, E. J. Michaud, W. Gurnee, and M. Tegmark, "Not All Language Model Features Are Linear," in *Proc. ICLR*, 2025. [[2405_14860_not-all-lm-features-are-linear|↗]]
[^4]: A. Modell et al., "The Origins of Representation Manifolds in Large Language Models," arXiv:2505.18235, 2025. [[2505_18235_the-origins-of-representation-manifolds-in-large-language-models|↗]]
