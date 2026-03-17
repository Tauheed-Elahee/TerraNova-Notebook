---
title: Not All Language Model Features Are Linear
id: 2405.14860
author: Engels, Liao, Michaud, Gurnee, Tegmark
publish_date: 2024-05
url: https://arxiv.org/abs/2405.14860
repo: https://github.com/Tauheed-Elahee/MultiDimensionalFeatures
summary: Some LLM features are encoded as multi-dimensional circular manifolds (rings/helices) rather than 1D directions, demonstrated via SAE clustering on GPT-2 and Mistral-7B with causal validation.
---

# Not All Language Model Features Are Linear

**Authors:** Joshua Engels, Isaac Liao, Eric J. Michaud, Wes Gurnee, Max Tegmark (MIT)
**arXiv:** 2405.14860
**Venue:** ICLR 2025
**Repo:** `Reference_Papers/MultiDimensionalFeatures`

## Summary

Challenges the linear representation hypothesis — the idea that LLMs encode all concepts as 1D directions in activation space. Shows that some features (days of the week, months of the year, years of the 20th century) are encoded as **multi-dimensional circular manifolds** (rings/helices) rather than single directions.

## Key Contributions

- **Discovery:** Used sparse autoencoder (SAE) feature co-activation patterns with spectral/graph clustering to find multi-dimensional feature clusters in GPT-2 and Mistral-7B.
- **Causal validation:** Intervention experiments (probing on sin/cos of the circular representation, then rotating it) confirm the circular structure is causally active in model behavior, not just a correlational artifact.
- **Formal metrics:** Introduced *reducibility* and *separability* indices to characterize when a multi-D feature cluster cannot be decomposed into independent 1D features.
- **Visualization:** Residual RGB plots show how regression on circular features explains variance in hidden states.

## Notable Feature Clusters (GPT-2 Layer 7 SAE)

- Days of week: features `[2592, 4445, 4663, 4733, 6531, 8179, 9566, 20927, 24185]`
- Months of year: 16 features with avg pairwise cosine sim ~0.53
- Years of 20th century: 10 features with avg pairwise cosine sim ~0.55
