---
title: Understanding Subword Compositionality of Large Language Models
id: 2508.17953
author: Peng, Chai, Søgaard
publish_date: 2025-08-25
url: https://arxiv.org/abs/2508.17953
summary: Sub-word token composition into word-level representations is approximately isometric to addition in most LLMs, meaning mean-pooled token hidden states faithfully approximate whole-word concept vectors.
---

# Understanding Subword Compositionality of Large Language Models

**arXiv:** 2508.17953 | 2025

## Summary

Systematic study of how six LLMs compose sub-word tokens into word-level representations. Finds three distinct compositional strategies across model families, with the dominant result being that composition is approximately isometric to addition.

## Key Contributions

- In most models, the composed representation of a multi-token word closely approximates the sum (or mean) of its sub-token representations.
- Semantic content is well-preserved under this additive composition.
- Formal properties (e.g. word length) are preserved only in some model families.
- Three compositional strategies identified across model families, suggesting architectural differences matter.

## Relevance to This Project

The "composition ≈ addition" finding provides a practical shortcut: mean-pooling token embeddings or hidden states across a concept name may give a good first approximation of the concept-level representation. This is useful both as a simple baseline and as a sanity check against more principled last-token or frame-average extractions. If the correlation with SNOMED distances is strong under mean-pooling, it suggests the geometry is robust to the choice of aggregation method.
