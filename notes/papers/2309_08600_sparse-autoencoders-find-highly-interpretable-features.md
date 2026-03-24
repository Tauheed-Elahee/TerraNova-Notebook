---
title: "Sparse Autoencoders Find Highly Interpretable Features in Language Models"
id: 2309.08600
author: Cunningham, Ewart, Riggs, Huben, Sharkey

publish_date: 2023-09
url: https://arxiv.org/abs/2309.08600
summary: Foundational SAE work showing that sparse features extracted from middle transformer layers are more monosemantic than raw neurons, with features corresponding to interpretable human concepts.
---

# Sparse Autoencoders Find Highly Interpretable Features in Language Models

**arXiv:** 2309.08600 | Cunningham, Ewart, Riggs, Huben, Sharkey, 2023

## Summary

Trains sparse autoencoders (SAEs) on the residual stream and MLP activations of GPT-2 and finds that the resulting features are substantially more monosemantic than raw neurons. Individual SAE features correspond to interpretable human concepts (specific syntactic roles, named entity types, semantic categories).

## Key Contributions

- Establishes SAEs as the primary method for extracting interpretable features from transformer hidden states.
- Demonstrates monosemanticity: each SAE feature activates for a coherent, human-interpretable concept.
- Shows that polysemanticity of raw neurons is an artefact of superposition, resolvable by SAE decomposition.
- Provides the methodological foundation for the SAE-based component of the TerraNova pipeline.

## Relevance to This Project

Foundational methodology for the planned next phase of TerraNova. If SAE features are monosemantic, then SAE features extracted from middle layers of a medical LLM may correspond to SNOMED semantic tags or ontological clusters — directly testable against the ontological distance matrix.
