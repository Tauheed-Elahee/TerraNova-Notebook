---
title: "From Tokens to Words: On the Inner Lexicon of LLMs"
id: 2410.05864
author: Kaplan, Oren, Reif, Schwartz
publish_date: 2024-10
url: https://arxiv.org/abs/2410.05864
repo: https://github.com/schwartz-lab-NLP/Tokens2Words
summary: LLMs perform intrinsic detokenization in early-to-middle layers; by layers 8–15 the last-token hidden state of a multi-token word becomes a unified concept representation, robust to arbitrary splits and OOV terms.
---

# From Tokens to Words: On the Inner Lexicon of LLMs

**arXiv:** 2410.05864 | ICLR 2025 | Kaplan, Oren, Reif, Schwartz

## Summary

Identifies an intrinsic *detokenization* process inside LLMs: the hidden state at the final token position of a multi-token word gradually transforms into a representation of the whole word across early-to-middle layers. The model maintains a latent vocabulary beyond its tokenizer's explicit scope.

## Key Contributions

- Detokenization concentrates in layers 8–15 for mid-sized models; earlier layers carry fragmented sub-token information.
- The mechanism is robust to arbitrary splits, typos, and out-of-vocabulary words — the model can understand OOV words it has never seen as tokens.
- FFN layers act as key-value stores constituting an "inner lexicon."
- Demonstrates practical vocabulary expansion without fine-tuning: new multi-token concepts get a single embedding initialized from their mid-layer representation.
- ~23% of multi-token words fail to detokenize successfully at any layer.

## Relevance to This Project

Provides the theoretical justification for extracting last-token residual stream activations at the detokenization layer as a unified concept-level representation of multi-token SNOMED CT terms. Directly addresses the core obstacle of medical terms spanning multiple tokens.

The key practical implication: feed a concept name (e.g. `"invasive ductal carcinoma of breast"`) through the lower layers, extract the last-token hidden state at layer ~12, and use that as the concept vector for geometric analysis — no prompt templates required.
