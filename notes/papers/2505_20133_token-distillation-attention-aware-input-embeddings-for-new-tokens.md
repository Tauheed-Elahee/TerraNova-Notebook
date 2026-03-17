---
title: "Token Distillation: Attention-Aware Input Embeddings for New Tokens"
id: 2505.20133
author: Dobler, Elliott, de Melo
publish_date: 2025-05-26
url: https://arxiv.org/abs/2505.20133
summary: Distills intermediate hidden states of multi-token phrases into a single new input embedding by matching attention patterns, enabling frozen models to process novel multi-token concepts as single tokens without fine-tuning.
---

# Token Distillation: Attention-Aware Input Embeddings for New Tokens

**arXiv:** 2505.20133 | 2025

## Summary

For any new multi-token concept, distills the model's intermediate hidden states (obtained under original sub-word tokenization) into a single new input embedding by minimising the divergence between the model's behaviour with the original split tokens versus the single new token. No fine-tuning of the core model required.

## Key Contributions

- Operationalises the "From Tokens to Words" finding: early/middle-layer representations already carry whole-concept information, and that information can be transferred to a single input vector.
- Uses attention patterns as the distillation target — the new single token should produce the same attention distribution as the original split tokens.
- More efficient than re-training the full embedding table.
- Works for arbitrary new vocabulary items, including domain-specific compound terms.

## Relevance to This Project

Provides a practical method for creating single-vector input representations of SNOMED CT concept names that a frozen model will process equivalently to the original multi-token input. If geometric analysis requires feeding concepts back into a model as inputs (e.g. for layer-wise activation extraction), this method generates the appropriate input embeddings.
