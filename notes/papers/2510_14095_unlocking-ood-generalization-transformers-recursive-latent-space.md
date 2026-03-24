---
title: "Unlocking Out-of-Distribution Generalization in Transformers via Recursive Latent Space Reasoning"
id: 2510.14095
author: Altabaa, Chen, Lafferty, Yang
publish_date: 2025-10
url: https://arxiv.org/abs/2510.14095
repo: https://github.com/Awni00/algorithmic-generalization-transformer-architectures
summary: Proposes anchored latent representations via discrete bottleneck in middle layers; shows middle layers enable robust semantic reasoning beyond training distribution.
---

# Unlocking Out-of-Distribution Generalization in Transformers via Recursive Latent Space Reasoning

**arXiv:** 2510.14095 | Altabaa, Chen, Lafferty, Yang, 2025

## Summary

Proposes anchoring latent representations at a discrete bottleneck in middle transformer layers, enabling recursive latent-space reasoning. Finds that models with explicit middle-layer bottlenecks generalise significantly better to out-of-distribution inputs because the discrete representation forces abstraction away from surface-form memorisation.

## Key Contributions

- Introduces a discrete bottleneck at middle layers that anchors latent representations to abstract concept states.
- Demonstrates substantially improved OOD generalisation with this bottleneck compared to standard transformers.
- Provides evidence that middle layers, when constrained to be abstract, encode reasoning-relevant structure robustly.
- Recursive latent reasoning: the discrete bottleneck representation is fed back as input for multi-step reasoning.

## Relevance to This Project

The discrete bottleneck finding has implications for TerraNova: if middle-layer representations are most abstract and OOD-robust, then the geometric structure found there (correlating with SNOMED ontological distances) should be more stable across different prompting conditions and models than early- or late-layer geometry.
