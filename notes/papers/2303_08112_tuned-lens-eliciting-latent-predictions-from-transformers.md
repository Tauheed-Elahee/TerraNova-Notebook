---
title: "Eliciting Latent Predictions from Transformers with the Tuned Lens"
id: 2303.08112
author: Belrose, Furman, Smith, Strauss, Nanda, Steinhardt
publish_date: 2023-03
url: https://arxiv.org/abs/2303.08112
repo: https://github.com/AlignmentResearch/tuned-lens
summary: A learned per-layer affine transformation maps intermediate hidden states to vocabulary distributions, revealing that next-token predictions stabilise well before the final layer — earlier and more accurately than the raw logit lens.
---

# Eliciting Latent Predictions from Transformers with the Tuned Lens

**arXiv:** 2303.08112 | Belrose, Furman, Smith, Strauss, Nanda, Steinhardt

## Summary

The *logit lens* (Nostalgebraist, 2020) projects intermediate hidden states directly through the unembedding matrix to read off token predictions at each layer. The tuned lens improves on this by training a small affine transformation (translator) per layer that maps the hidden state into the final-layer distribution more faithfully. This reveals that the model's output prediction crystallises well before the last layer — the symmetric output-side counterpart to Tokens2Words detokenization on the input side.

## Key Contributions

- Per-layer translators trained with a KL-divergence loss against the final layer's output distribution.
- Predictions are stable and accurate from around the middle layers onwards (~layer 20 for a 32-layer model), with earlier layers carrying noisy or incomplete predictions.
- The tuned lens is strictly more accurate than the raw logit lens, especially in early layers.
- Applicable to any autoregressive transformer without modifying model weights.
- Enables layer-wise interpretability: you can read off *what the model is about to predict* at any intermediate layer.

## Relevance to This Project

Provides the output-side complement to Tokens2Words. If detokenization (input assembly) completes at layer ~12, the tuned lens shows that re-tokenization (output prediction) stabilises around layer ~20. This defines a **semantic core** of approximately layers 12–20 where the model operates on unified concept representations without tokenization artefacts on either end.

Practical implication for the direct-injection pipeline:
- **Input**: inject concept vector at layer ~12, skipping detokenization layers 0–11
- **Output**: extract prediction at layer ~20 via the tuned lens translator, skipping re-tokenization layers 20–32
- Layers 12–20 become a pure concept-to-concept reasoning window
