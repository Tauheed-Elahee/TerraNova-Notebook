---
title: Multi-Token Medical Terms and the Detokenisation Mechanism
tags: [tokenization, multi-token, detokenization, medical, SNOMED, mechanistic-interpretability]
summary: Why multi-token medical terms pose a challenge for residual stream extraction, and how the LLM's intrinsic detokenisation process resolves this by producing a unified concept representation at the last-token position in early-to-middle layers.
papers: [2410.05864, 2406.20086]
---

# Multi-Token Medical Terms and the Detokenisation Mechanism

## The Problem

TransformerLens and SAELens work cleanly when a concept is a single token — "Monday", "January", "1987" each occupy one position in the residual stream. Medical terminology does not have this property. A concept like `"invasive ductal carcinoma of breast"` is split into several sub-word tokens by any standard BPE tokeniser, so there is no single token position whose activation unambiguously represents the concept.

This is the core obstacle for applying the Engels et al. pipeline to SNOMED CT concepts. Four workarounds exist:

| Approach | Method | Trade-off |
|---|---|---|
| Last-token position | Extract residual stream at final token of concept name | Theoretically motivated (see below); requires knowing where concept ends |
| Mean pooling | Average hidden states across all concept tokens | Simple; less principled for causal models where early tokens haven't seen later ones |
| Prompt template | Wrap concept in a sentence, extract at a fixed position | Controls context; adds syntactic noise |
| BERT-style model | Use a bidirectional encoder with CLS pooling | Cleaner pooling semantics; requires different tooling than TransformerLens |

Filtering to single-token concepts is not viable — almost no precise SNOMED CT terms tokenise to a single token.

## The Detokenisation Mechanism

LLMs perform an intrinsic *detokenisation* process: across early-to-middle layers, the hidden state at the **last token position** of a multi-token word is gradually transformed from a representation of that sub-word fragment into a representation of the whole word.[^1]

Key properties:
- Process concentrates in layers 8–15 for mid-sized models
- Robust to arbitrary tokenisation splits and out-of-vocabulary words
- FFN layers act as key-value stores constituting an "inner lexicon"
- ~23% of multi-token words fail to detokenise successfully at any layer

## Evidence from Token Erasure

A complementary finding: in early layers, information about preceding sub-word tokens is **actively erased** at the last-token position of named entities.[^2] Rather than accumulating context, the model discards sub-word identity and replaces it with the assembled concept. The erasure is strongest for named entities — the same class as SNOMED CT concept names — making them particularly well-suited to last-token extraction.

## Practical Implication

Feed a concept name (e.g. `"invasive ductal carcinoma of breast"`) through the lower layers, extract the last-token hidden state at layer ~12, and use that vector for geometric analysis. No prompt template is required — the detokenisation mechanism handles multi-token assembly internally.

---

[^1]: R. Kaplan, S. Oren, U. Reif, and R. Schwartz, "From Tokens to Words: On the Inner Lexicon of LLMs," in *Proc. ICLR*, 2025. [[2410_05864_from-tokens-to-words-on-the-inner-lexicon-of-llms|↗]]
[^2]: S. Feucht, T. Atkinson, E. Wallace, and D. Bau, "Token Erasure as a Footprint of Implicit Vocabulary Items in LLMs," in *Proc. EMNLP*, 2024. [[2406_20086_token-erasure-as-a-footprint-of-implicit-vocabulary-items-in-llms|↗]]
