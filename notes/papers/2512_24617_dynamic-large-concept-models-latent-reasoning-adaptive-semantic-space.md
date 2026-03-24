---
title: "Dynamic Large Concept Models: Latent Reasoning in an Adaptive Semantic Space"
id: 2512.24617
author: Qu, Wang, Huang, Hua, Yin, Zhu, Zhou, Min, Li, Zhang, Xing, Song, Zheng, Zeng, Lin, Zhang, Huang
publish_date: 2025-12
url: https://arxiv.org/abs/2512.24617
summary: Extension of LCMs with hierarchical, adaptive concept merging — tokens dynamically compress into concept representations mid-network with MoE-style compute allocation.
---

# Dynamic Large Concept Models: Latent Reasoning in an Adaptive Semantic Space

**arXiv:** 2512.24617 | Qu, Wang, Huang et al., 2025

## Summary

Extends the Large Concept Models framework with a dynamic, hierarchical concept representation. Rather than fixed sentence-level embeddings, concepts are formed by adaptively merging tokens based on content, with Mixture-of-Experts routing to allocate compute to the most semantically dense regions.

## Key Contributions

- Introduces adaptive concept granularity — the system decides how many tokens to merge into each concept based on semantic content.
- Uses MoE-style routing to vary compute per concept, spending more on semantically complex regions.
- Demonstrates improved performance over static LCMs on long-form reasoning tasks.

## Relevance to This Project

Reinforces that the token-to-concept boundary is not a fixed layer but an adaptive process. For the semantic core hypothesis, this suggests the injection boundary (where detokenization completes) may be concept-dependent rather than a single fixed layer number.
