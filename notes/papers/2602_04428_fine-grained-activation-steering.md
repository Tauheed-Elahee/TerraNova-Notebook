---
title: "Fine-Grained Activation Steering: Steering Less, Achieving More"
id: 2602.04428
author: Feng, Li, Zhu, Zhou, Qian, Zhang, Chua, Mak, Ng, Mao
publish_date: 2026-02
url: https://arxiv.org/abs/2602.04428
repo: https://github.com/zijian678/AUSteer
summary: Decomposes block-level activations into atomic units; shows middle layers contain heterogeneous features that can be precisely manipulated at sub-neuron granularity.
---

# Fine-Grained Activation Steering: Steering Less, Achieving More

**arXiv:** 2602.04428 | Feng, Li, Zhu et al., 2026

## Summary

Proposes decomposing transformer block activations into fine-grained atomic units (below the neuron level) for more precise steering. Demonstrates that middle layers contain heterogeneous feature mixtures that, when targeted precisely, allow larger behavioural changes with smaller interventions than block-level steering.

## Key Contributions

- Introduces sub-neuron decomposition of activations for steering, improving precision and reducing side effects.
- Shows middle layers encode heterogeneous, overlapping semantic features requiring fine-grained separation.
- Demonstrates that coarse steering vectors cause collateral concept activation; fine-grained targeting avoids this.
- Establishes a method for isolating specific concept dimensions in middle-layer representations.

## Relevance to This Project

Motivates using SAEs (which perform exactly this sub-neuron decomposition) for middle-layer analysis. The heterogeneity finding supports the TerraNova goal: individual SAE features in middle layers may align with specific SNOMED semantic tags or ontological clusters.
