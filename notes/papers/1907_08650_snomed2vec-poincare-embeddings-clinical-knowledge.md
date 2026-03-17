---
title: "Snomed2Vec: Random Walk and Poincaré Embeddings of a Clinical Knowledge Base for Healthcare Analytics"
id: 1907.08650
author: Agarwal, Eftimov, Addanki, Choudhury, Tamang, Rallo
publish_date: 2019-07-19
url: https://arxiv.org/abs/1907.08650
venue: KDD Workshop on Applied Data Science for Healthcare (DSHealth '19)
summary: Graph-based embeddings of SNOMED-CT using random walks and Poincaré (hyperbolic) embeddings; achieves 5-6× improvement in concept similarity and 6-20% improvement in patient diagnosis tasks over state-of-the-art baselines.
---

# Snomed2Vec: Random Walk and Poincaré Embeddings of a Clinical Knowledge Base for Healthcare Analytics

**arXiv:** 1907.08650 | KDD DSHealth 2019

## Summary

Applies graph embedding methods — random walk-based (node2vec/DeepWalk-style) and Poincaré (hyperbolic) embeddings — directly to the SNOMED-CT knowledge graph to produce concept vectors for downstream healthcare analytics. Evaluates on concept similarity, node classification, link prediction, and patient state/diagnosis prediction. SNOMED-CT-derived embeddings substantially outperform general biomedical embeddings.

## Key Contributions

- Systematic comparison of Euclidean random walk embeddings vs. Poincaré (hyperbolic) embeddings on SNOMED-CT.
- 5-6× improvement in concept similarity scores over state-of-the-art baselines.
- 6-20% improvement on patient diagnosis prediction tasks.
- Evaluated across node classification, link prediction, and patient state prediction.
- Demonstrates that the hierarchical structure of SNOMED-CT is better captured by hyperbolic geometry than Euclidean space.

## Relevance to This Project

This is a direct predecessor to this project's core question: does the geometry of LLM hidden states for medical concepts reflect the SNOMED-CT hierarchy? Snomed2Vec establishes that (1) SNOMED-CT graph structure contains useful signal for clinical tasks, and (2) hyperbolic (Poincaré) geometry better captures that hierarchical structure than flat Euclidean embeddings. This motivates checking whether LLM representations of SNOMED concepts exhibit hyperbolic geometry, and whether distances in LLM space correlate with graph-based Poincaré distances. The concept similarity and patient diagnosis benchmarks are directly reusable as evaluation targets.
