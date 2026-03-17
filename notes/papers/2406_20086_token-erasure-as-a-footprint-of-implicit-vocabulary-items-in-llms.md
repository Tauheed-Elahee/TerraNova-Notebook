---
title: Token Erasure as a Footprint of Implicit Vocabulary Items in LLMs
id: 2406.20086
author: Feucht, Atkinson, Wallace, Bau
publish_date: 2024-06-28
url: https://arxiv.org/abs/2406.20086
repo: https://github.com/sfeucht/footprints
summary: Information about preceding sub-word tokens is actively erased at the last-token position of named entities in early layers, revealing the mechanism by which LLMs assemble implicit vocabulary items from fragments.
---

# Token Erasure as a Footprint of Implicit Vocabulary Items in LLMs

**arXiv:** 2406.20086 | EMNLP 2024

## Summary

Identifies an "erasure" effect in early transformer layers: at the last-token position of multi-token words and named entities, information about the preceding tokens is rapidly forgotten. Interprets this as evidence of a mechanism assembling larger implicit vocabulary units from sub-word fragments.

## Key Contributions

- The erasure is measurable as a drop in decodability of preceding token identities from the last-token hidden state.
- Effect is strongest for named entities and compound nouns — the same class as medical terminology.
- Proposes a method to "read out" the LLM's implicit vocabulary by identifying positions where erasure occurs.
- Provides mechanistic evidence complementing the detokenization findings of "From Tokens to Words."

## Relevance to This Project

Named entities (like SNOMED CT concept names) show the strongest erasure signal, meaning the last-token hidden state most cleanly carries the unified concept representation for this class of term. This supports using last-token residual stream activations for medical concept geometry analysis — and suggests the optimal extraction layer is identifiable by measuring where erasure is maximal.
