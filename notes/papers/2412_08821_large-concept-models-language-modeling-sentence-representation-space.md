---
title: "Large Concept Models: Language Modeling in a Sentence Representation Space"
id: 2412.08821
author: LCM team — Barrault, Duquenne, Elbayad, Kozhevnikov, Alastruey, Andrews, Coria, Couairon, Costa-jussà, Dale, Elsahar, Heffernan, Janeiro, Tran, Ropers, Sánchez, San Roman, Mourachko, Saleem, Schwenk
publish_date: 2024-12
url: https://arxiv.org/abs/2412.08821
repo: https://github.com/facebookresearch/large_concept_model
summary: Proposes operating transformers entirely in sentence-embedding space (SONAR) as a higher-level abstraction over tokens; the concept space is explicit and external rather than a discovered middle-layer window.
---

# Large Concept Models: Language Modeling in a Sentence Representation Space

**arXiv:** 2412.08821 | LCM team (Meta FAIR), 2024

## Summary

Instead of predicting the next token, Large Concept Models (LCMs) predict the next sentence-level embedding in SONAR space — a language- and modality-agnostic sentence representation. The model reasons entirely at the concept level, with tokenization/detokenization handled by a separate encoder/decoder pair at the boundaries.

## Key Contributions

- Demonstrates end-to-end language modelling where the autoregressive unit is a dense sentence embedding rather than a token.
- Shows that SONAR provides a stable, multilingual concept space suitable for next-concept prediction.
- Separates the concerns of surface-form generation (tokenizer) and semantic reasoning (LCM), anticipating later hybrid architectures (SONAR-LLM).
- Establishes a proof of concept that concept-level LMs can be competitive with token-level LMs on certain tasks.

## Relevance to This Project

The closest architectural family to the semantic core hypothesis, but the concept space here is **external and explicit** (SONAR), not discovered as a layer range within a standard transformer. Useful as a reference design: the injection/extraction boundary idea in the combined-architecture pipeline is analogous to the encoder/decoder wrapper around LCM's concept-space reasoning.
