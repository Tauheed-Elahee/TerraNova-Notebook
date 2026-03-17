---
title: "MedTok: Multimodal Medical Code Tokenizer"
id: 2502.04397
author: Su, Messica, Huang, Johnson, Fesser, Gao, Sahneh, Zitnik
publish_date: 2025-02-06
url: https://arxiv.org/abs/2502.04397
summary: Encodes each medical code (SNOMED CT, ICD, ATC) as a single dense vector using both text description and ontological graph position, replacing BPE tokenization as a plug-and-play component for transformer EHR models.
---

# MedTok: Multimodal Medical Code Tokenizer

**arXiv:** 2502.04397 | ICML 2025

## Summary

Replaces standard text-BPE tokenization of medical codes (ICD, SNOMED CT, ATC, etc.) with a multimodal tokenizer that encodes each medical code as a single dense token vector. Uses both the code's textual description (via a language model encoder) and its position in the ontological hierarchy (via a graph encoder). Designed as a plug-and-play replacement for any transformer-based EHR model.

## Key Contributions

- Each medical code becomes a single dense vector regardless of how many tokens its text description spans.
- Graph encoder explicitly incorporates SNOMED CT ontological structure (parent-child relationships, hierarchy depth) into the token representation.
- Drop-in compatible with any transformer EHR model without architectural changes.
- Evaluated on downstream clinical prediction tasks with improved performance over BPE tokenization.

## Relevance to This Project

The most directly analogous existing work to the intended pipeline here. MedTok shows that SNOMED CT concepts can be usefully represented as single dense vectors incorporating both semantic and ontological information, and that these vectors work as transformer inputs. The key difference from this project: MedTok uses these vectors for downstream EHR task performance, not for studying the *geometry* of the representation space against the ontological distances. The geometric analysis angle is the gap this project could fill.
