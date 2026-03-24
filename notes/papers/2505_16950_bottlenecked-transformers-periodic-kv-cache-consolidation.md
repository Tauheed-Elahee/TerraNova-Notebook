---
title: "Bottlenecked Transformers: Periodic KV Cache Consolidation for Generalised Reasoning"
id: 2505.16950
author: Oomerjee, Fountas, Bou-Ammar, Wang
publish_date: 2025-05
url: https://arxiv.org/abs/2505.16950
summary: Information bottleneck theory applied to middle-layer KV consolidation; shows middle layers act as representational hubs that compress and consolidate information for downstream reasoning.
---

# Bottlenecked Transformers: Periodic KV Cache Consolidation for Generalised Reasoning

**arXiv:** 2505.16950 | Oomerjee, Fountas, Bou-Ammar, Wang, 2025

## Summary

Applies information bottleneck theory to the KV cache of transformers, proposing periodic consolidation of KV entries at middle-layer checkpoints. Shows that middle layers act as representational hubs where information is compressed and reorganised, and that consolidating at these hubs improves generalisation on reasoning tasks.

## Key Contributions

- Identifies middle layers as information bottlenecks in the KV cache where cross-token information is most concentrated.
- Periodic KV consolidation at these hubs reduces memory while preserving reasoning ability better than uniform pruning.
- Provides a theoretical grounding (information bottleneck) for the empirical finding that middle layers are semantically rich.
- Shows consolidation hubs correspond to the same layer range identified by Tokens2Words and Tuned Lens.

## Relevance to This Project

Provides theoretical (information-bottleneck) grounding for the semantic core window. Middle layers as information hubs is consistent with the hypothesis that this layer range is where concept-level representations are most accessible — the period after detokenization but before re-tokenization.
