---
title: "Cramming 1568 Tokens into a Single Vector and Back Again: Exploring the Limits of Embedding Space Capacity"
id: 2502.13063
author: Kuratov, Arkhipov, Bulatov, Burtsev
publish_date: 2025-02
url: https://arxiv.org/abs/2502.13063
summary: A single LLM input embedding vector can encode information equivalent to 1568+ tokens, with capacity scaling linearly with vector count, establishing the information-theoretic feasibility of single-vector concept representation.
---

# Cramming 1568 Tokens into a Single Vector and Back Again: Exploring the Limits of Embedding Space Capacity

**arXiv:** 2502.13063 | ACL 2025 (oral) | Kuratov, Arkhipov, Bulatov, Burtsev

## Summary

Empirical study of how much information a single input embedding vector can carry when fed to a large language model. Demonstrates that a single embedding vector to Llama-3.1-8B can encode enough information to reconstruct 1,500+ tokens, with capacity scaling roughly linearly with the number of vectors used.

## Key Contributions

- A single 4096-dim vector can losslessly represent ~1568 tokens when the model is prompted to reconstruct them.
- Capacity scales linearly with number of vectors: N vectors → ~N × 1568 tokens.
- Establishes an empirical upper bound for single-vector concept representation capacity.

## Relevance to This Project

Answers the theoretical objection that a single vector cannot carry enough information to represent a multi-token medical concept. The capacity of a single LLM embedding vector far exceeds what is needed for a short phrase like "invasive ductal carcinoma of breast." This supports the feasibility of any single-vector approach (last-token extraction, frame averaging, Token Distillation) for representing SNOMED concepts as transformer inputs.
