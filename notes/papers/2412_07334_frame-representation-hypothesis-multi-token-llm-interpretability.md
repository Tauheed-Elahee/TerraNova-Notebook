---
title: "Frame Representation Hypothesis: Multi-Token LLM Interpretability and Concept-Guided Text Generation"
id: 2412.07334
author: Valois, Souza, Shimomoto, Fukui
publish_date: 2024-12-10
url: https://arxiv.org/abs/2412.07334
repo: https://github.com/phvv-me/frame-representation-hypothesis
summary: Multi-token words are represented as ordered sequences of vectors (frames); concepts are the average of frames, extending the Linear Representation Hypothesis to multi-token terms across Llama 3.1, Gemma 2, and Phi 3.
---

# Frame Representation Hypothesis: Multi-Token LLM Interpretability and Concept-Guided Text Generation

**arXiv:** 2412.07334 | TACL 2025

## Summary

Extends the Linear Representation Hypothesis (which only applies to single-token words) to multi-token words. Proposes that multi-token words are represented as "frames" — ordered sequences of vectors — and that concepts are represented as the average of word frames sharing that concept.

## Key Contributions

- Formalises the geometric structure of multi-token concept representations as frame averages.
- Demonstrates concept-guided text generation on Llama 3.1, Gemma 2, and Phi 3 using these representations.
- Shows the hypothesis holds across model families, suggesting it is a general property rather than model-specific.

## Relevance to This Project

Provides a geometric framework for multi-token medical concepts that is directly compatible with manifold analysis. If SNOMED CT concepts are represented as frame averages, then the mean-pooled token hidden states across a concept name form a principled concept vector. This could serve as an alternative to last-token extraction for constructing the concept embedding matrix used in correlation analysis.
