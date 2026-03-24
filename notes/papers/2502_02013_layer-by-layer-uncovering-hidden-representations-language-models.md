---
title: "Layer by Layer: Uncovering Hidden Representations in Language Models"
id: 2502.02013
author: Skean, Arefin, Zhao, Patel, Naghiyev, LeCun, Shwartz-Ziv
publish_date: 2025-02
url: https://arxiv.org/abs/2502.02013
repo: https://github.com/OFSkean/information_flow
summary: Comprehensive analysis showing mid-depth embeddings often exceed last-layer performance on semantic tasks; proposes information-theoretic metrics for representation quality across layers.
---

# Layer by Layer: Uncovering Hidden Representations in Language Models

**arXiv:** 2502.02013 | Skean, Arefin, Zhao, Patel, Naghiyev, LeCun, Shwartz-Ziv, 2025

## Summary

Systematic investigation of representation quality at each layer of a transformer. Finds that mid-depth hidden states frequently outperform last-layer representations on semantic benchmarks, and introduces information-theoretic metrics to characterise representation quality without task-specific fine-tuning.

## Key Contributions

- Demonstrates that semantic information peaks in middle layers rather than the final layer.
- Introduces layer-wise information-theoretic quality metrics applicable across model families.
- Provides empirical evidence that the last layer is suboptimal for semantic extraction.
- Supports using intermediate layers as a richer source of concept representations.

## Relevance to This Project

Directly validates that middle layers carry more semantic information than the final layer. For the TerraNova pipeline, this supports extracting concept vectors from middle layers rather than last-layer token embeddings. The information-theoretic metrics could serve as a principled criterion for selecting which layer to use for concept extraction.
