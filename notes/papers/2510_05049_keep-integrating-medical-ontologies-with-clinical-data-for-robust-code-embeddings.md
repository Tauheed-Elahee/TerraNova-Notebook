---
title: "KEEP: Integrating Medical Ontologies with Clinical Data for Robust Code Embeddings"
id: 2510.05049
author: Elhussein, Meddeb, Newbury, Mirone, Stoll, Gursoy
publish_date: 2025-10-06
url: https://arxiv.org/abs/2510.05049
repo: https://github.com/G2Lab/keep
summary: Produces medical code embeddings (SNOMED CT, ICD) where ontological proximity is reflected in vector distance, by jointly training on knowledge graph structure and clinical co-occurrence data.
---

# KEEP: Integrating Medical Ontologies with Clinical Data for Robust Code Embeddings

**arXiv:** 2510.05049 | 2025

## Summary

Produces robust single-vector embeddings for medical codes (SNOMED CT, ICD) by integrating knowledge graph structure with clinical data. Explicitly incorporates ontological position — including ancestor counts and hierarchy depth — into the embedding training objective.

## Key Contributions

- Combines clinical co-occurrence signals with SNOMED CT / ICD graph structure via a joint training objective.
- Produces embeddings where ontological proximity (ancestor overlap, hierarchy depth) is reflected in vector distance.
- Compatible with any medical terminology that has an associated knowledge graph.
- Demonstrated to be more robust than text-only embeddings for rare and under-represented codes.

## Relevance to This Project

Directly relevant as a comparison baseline: KEEP embeddings encode ontological position by design, so their geometry against SNOMED distances should be a near-upper-bound on what is achievable. Comparing the geometric correlation of KEEP embeddings vs. text-embedding-3-large vs. LLM residual stream activations against SNOMED distances would quantify how much ontological structure each representation type captures.
