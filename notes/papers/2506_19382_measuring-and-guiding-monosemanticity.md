---
title: "Measuring and Guiding Monosemanticity"
id: 2506.19382
author: Härle, Friedrich, Brack, Wäldchen, Deiseroth, Schramowski, Kersting
publish_date: 2025-06
url: https://arxiv.org/abs/2506.19382
repo: https://github.com/ml-research/measuring-and-guiding-monosemanticity
summary: Introduces Feature Monosemanticity Score (FMS) as a quantitative metric; proposes G-SAE that conditions on labeled concepts during training to produce more monosemantic features.
---

# Measuring and Guiding Monosemanticity

**arXiv:** 2506.19382 | Härle, Friedrich, Brack et al., 2025

## Summary

Introduces the Feature Monosemanticity Score (FMS), a quantitative metric for measuring how monosemantic a SAE feature is. Using FMS, proposes Guided SAE (G-SAE), which conditions feature learning on labeled concept examples during training to produce features that more reliably align with human-interpretable concepts.

## Key Contributions

- FMS: a principled metric for monosemanticity that enables comparison across SAE architectures and training runs.
- G-SAE: conditioning SAE training on labeled concept examples improves alignment between learned features and target concepts.
- Provides a feedback loop for SAE training: FMS can guide hyperparameter selection and dictionary size.
- Shows that standard SAE training produces variable monosemanticity; guided training concentrates it on desired concepts.

## Relevance to This Project

FMS could be used to evaluate whether SAE features trained on a medical LLM align with SNOMED semantic tags. G-SAE is particularly relevant: if SNOMED concepts are used as labeled examples during SAE training, the resulting features should be biased toward SNOMED-aligned monosemantic representations.
