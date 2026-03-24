---
title: "Uncovering Hidden Geometry in Transformers via Disentangling Position and Context"
id: 2510.04861
author: Zhao, Zhou, Li, Chu, Zhang, Zheng, Wen, Ma, Wang, Chen, Meng, Zeng, Li, Xie, Ye, Wang, Chen, Cai
publish_date: 2025-10
url: https://arxiv.org/abs/2510.04861
summary: Decomposes hidden states into position, context, and residual components; reveals low-dimensional geometry of positional embeddings across layers with orthogonal semantic structure.
---

# Uncovering Hidden Geometry in Transformers via Disentangling Position and Context

**arXiv:** 2510.04861 | Zhao, Zhou, Li et al., 2025

## Summary

Decomposes transformer hidden states into three orthogonal components — positional, contextual, and residual — at each layer. Reveals that positional and semantic information are structured as low-dimensional, geometrically distinct subspaces, and that their relative contributions shift across layers.

## Key Contributions

- Introduces a decomposition framework separating positional from contextual geometry in hidden states.
- Shows positional information is concentrated in a low-dimensional subspace orthogonal to the semantic subspace.
- Demonstrates that the geometry of hidden states is more structured than raw PCA suggests once positional interference is removed.
- Provides evidence that middle layers are where the contextual (semantic) subspace is most dominant.

## Relevance to This Project

Directly relevant to the manifold analysis in TerraNova: the correlation between embedding geometry and SNOMED ontological distances may be obscured by positional components in the hidden states. Decomposing position from context before computing pairwise distances could improve the correlation signal and reveal cleaner geometric structure.
