---
title: "Emergent Semantics Beyond Token Embeddings: Transformer LMs with Frozen Visual Unicode Representations"
id: 2507.04886
author: Bochkov
publish_date: 2025-07
url: https://arxiv.org/abs/2507.04886
repo: https://github.com/AVBochkov/Embeddings
summary: Shows high-level semantics emerge from middle transformer layers independent of what input embeddings encode — supporting the injection framing: semantic representation is not in the input layer but emerges in middle processing.
---

# Emergent Semantics Beyond Token Embeddings: Transformer LMs with Frozen Visual Unicode Representations

**arXiv:** 2507.04886 | Bochkov, 2025

## Summary

Trains transformers with frozen, randomly-initialised (or visually-derived) input embeddings for Unicode characters and finds that high-level semantic representations still emerge in middle layers. Demonstrates that the input embedding layer is not where semantic content is encoded — it emerges through processing.

## Key Contributions

- Shows semantic representations emerge in middle layers regardless of the quality of input embeddings.
- Demonstrates that the input embedding layer is a transducer rather than a semantic store.
- Supports a sharp separation between the input boundary (tokenization transduction) and the onset of semantic representation.
- Provides evidence that injection at middle layers (bypassing the transduction phase) is architecturally valid.

## Relevance to This Project

Strong support for the injection framing of the semantic core pipeline: if semantics emerge in middle layers regardless of input embeddings, then injecting a concept vector at the point where semantics emerge (skipping the transduction layers) is a principled operation, not a hack.
