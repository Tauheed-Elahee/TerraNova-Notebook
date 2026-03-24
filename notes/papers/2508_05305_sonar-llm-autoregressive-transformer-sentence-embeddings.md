---
title: "SONAR-LLM: Autoregressive Transformer that Thinks in Sentence Embeddings and Speaks in Tokens"
id: 2508.05305
author: Dragunov, Rahmatullaev, Goncharova, Kuznetsov, Razzhigaev
publish_date: 2025-08
url: https://arxiv.org/abs/2508.05305
repo: https://github.com/FusionBrainLab/SONAR-LLM
summary: Hybrid architecture that processes internally at the concept level (SONAR sentence embeddings) but generates tokens at output — the closest architectural analogue to the semantic core pipeline where input and output remain token-level but internal processing is concept-level.
---

# SONAR-LLM: Autoregressive Transformer that Thinks in Sentence Embeddings and Speaks in Tokens

**arXiv:** 2508.05305 | Dragunov, Rahmatullaev, Goncharova, Kuznetsov, Razzhigaev, 2025

## Summary

Extends Large Concept Models by building a hybrid architecture: input tokens are encoded into SONAR sentence embeddings, an autoregressive transformer processes in that concept space, and the output is decoded back to tokens. The model "thinks" in sentence embedding space and "speaks" in tokens.

## Key Contributions

- Demonstrates a working hybrid architecture with token-level I/O and concept-level internal processing.
- Shows that internal concept-space reasoning improves coherence and semantic consistency over fully token-level models.
- Provides the closest real-world architectural analogue to the semantic core injection/extraction pipeline.

## Relevance to This Project

The most direct architectural reference for the combined-architecture pipeline: token input → encode to concept vector → concept-level reasoning → decode to token output. The difference is that SONAR-LLM uses an external SONAR concept space, while the semantic core hypothesis identifies this concept space as a layer range *within* a standard transformer.
