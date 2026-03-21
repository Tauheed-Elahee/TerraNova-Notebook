---
title: Combined Architecture — Semantic Core Pipeline
tags: [architecture, tokenization, vocabulary-expansion, detokenization, tuned-lens, semantic-core, injection, layers, pipeline]
summary: A combined architecture exploiting the input-side detokenisation (layer ~12) and output-side prediction stabilisation (layer ~20) to define a semantic core window, enabling direct concept injection, vocabulary expansion, and a three-stage geometric analysis experimental design.
papers: [2410.05864, 2303.08112, 2502.04397, 2510.05049, 2505.20133, 2406.20086, 2405.14860, 2412.06769]
---

# Combined Architecture — Semantic Core Pipeline

## The Symmetric Layer Structure

Two findings bracket the middle layers of a transformer as a **semantic core**:

| Side | Paper | Finding |
|---|---|---|
| Input | Tokens2Words (2410.05864) | Detokenisation completes at layer ~12: multi-token concept → unified vector |
| Output | Tuned Lens (2303.08112) | Next-token prediction stabilises at layer ~20: unified vector → output token |

```
Layers  0–11:  detokenisation  (sub-word fragments → concept)
Layer  ~12:    ── concept vector lives here ──────────────────
Layers 12–20:  semantic reasoning  (concept-to-concept)
Layer  ~20:    ── output prediction stable here ──────────────
Layers 20–32:  re-tokenisation  (concept → output token)
```

Layers 12–20 are therefore a window where the model operates on unified concept representations with no tokenisation artefacts on either end. This is the semantic core.

## Direct Injection at Layer ~12

Instead of running the full forward pass for a known concept, skip the detokenisation layers entirely:

1. **First pass (extraction)**: feed concept name `"invasive ductal carcinoma of breast"` → extract last-token hidden state `h₁₂` at the detokenisation layer
2. **Subsequent use (injection)**: inject `h₁₂` directly into the residual stream at layer ~12, bypassing layers 0–11

This is standard activation patching — no training required. The injected vector is already in the correct distribution because it came from layer 12.

The practical challenge is attention: layers 12+ attend over all positions including those that preceded the injection point. Collapsing a 4-token concept to a single injection position requires replacing the 4-token KV entries with a single entry at the injection layer.

This differs from Coconut[^4] (which feeds hidden states back to layer 0 and requires training) and from vocabulary expansion (which adds a new input embedding and runs all layers). Direct injection is cheaper, requires no training, and injects into the exact distribution the upper layers expect.

## Output Extraction at Layer ~20

Symmetrically, instead of running layers 20–32 to obtain the output token, extract the prediction at layer ~20 using the tuned lens translator:

```
h₂₀ → tuned_lens_translator[20] → logits → predicted token
```

Combined with input injection at layer ~12, the full pipeline for a known concept becomes:

```
h₁₂  →  [layers 12–20]  →  h₂₀  →  tuned lens  →  output
```

Only 8 layers of compute for concepts whose input and output representations are already known.

## Three-Stage Geometric Experiment

The architecture supports a clean experimental progression to study whether ontological structure is present in LLM representations and where it comes from:

### Stage 1 — Baseline Geometry (frozen model, standard tokenizer)
Extract last-token hidden states at layer ~12 for SNOMED CT concepts using the standard tokeniser. Measure pairwise distances and compare to SNOMED ontological distances.

> *What does the LLM implicitly know about SNOMED structure?*

### Stage 2 — Expanded Vocabulary Geometry (frozen model, new tokens)
Add SNOMED concepts as single tokens initialised from Stage 1 vectors. Re-extract representations — the concept now enters at layer 0 as a single token rather than being assembled across layers 0–12. Re-run geometric analysis.

> *Does feeding concepts as atomic units change internal geometry? Does the semantic core shift?*

The delta between Stage 1 and Stage 2 isolates the effect of **tokenisation granularity**.

### Stage 3 — Ontology-Supervised Geometry (trained embeddings)
Train a MedTok[^5]- or KEEP[^6]-style encoder so input representations explicitly encode ontological graph position. Re-run geometric analysis. This is the upper bound — maximum ontological signal by design.

> *How much geometry is recoverable when ontology is explicitly supervised?*

The delta between Stage 2 and Stage 3 isolates the effect of **ontological supervision**.

| Stage | What varies | Key delta |
|---|---|---|
| 1 → 2 | Tokenisation granularity | Effect of atomic vs. assembled concept input |
| 2 → 3 | Ontological supervision | Effect of explicit graph structure in embeddings |

## Relationship to Other Papers

- **Token Distillation ([[2505_20133_token-distillation-attention-aware-input-embeddings-for-new-tokens|2505.20133]])**: provides an alternative to direct injection — distils mid-layer hidden states into new input embeddings by matching attention patterns. Complementary to Stage 2.
- **Subword Compositionality ([[2508_17953_understanding-subword-compositionality-of-large-language-models|2508.17953]])**: shows mean-pooling ≈ last-token extraction for most LLMs. Stage 1 can compare both extraction strategies.
- **Snomed2Vec ([[1907_08650_snomed2vec-poincare-embeddings-clinical-knowledge|1907.08650]])**: Poincaré embeddings as a geometric baseline — compare Stage 1 vectors to hyperbolic embeddings to test whether the LLM has implicitly learned hyperbolic-like ontological structure.
- **Not All Features Linear ([[2405_14860_not-all-lm-features-are-linear|2405.14860]]) + Origins of Manifolds ([[2505_18235_the-origins-of-representation-manifolds-in-large-language-models|2505.18235]])**: the geometric analysis toolkit for all three stages — circular manifolds, SAE clustering, causal validation.
- **Token Erasure ([[2406_20086_token-erasure-as-a-footprint-of-implicit-vocabulary-items-in-llms|2406.20086]])**: marks the detokenisation completion point — the layer of maximal erasure is the injection target for Stage 2.

---

[^1]: R. Kaplan, S. Oren, U. Reif, and R. Schwartz, "From Tokens to Words: On the Inner Lexicon of LLMs," in *Proc. ICLR*, 2025. [[2410_05864_from-tokens-to-words-on-the-inner-lexicon-of-llms|↗]]
[^2]: N. Belrose, Z. Furman, L. Smith, D. Strauss, N. Nanda, and J. Steinhardt, "Eliciting Latent Predictions from Transformers with the Tuned Lens," arXiv:2303.08112, 2023. [[2303_08112_tuned-lens-eliciting-latent-predictions-from-transformers|↗]]
[^3]: S. Feucht, T. Atkinson, E. Wallace, and D. Bau, "Token Erasure as a Footprint of Implicit Vocabulary Items in LLMs," in *Proc. EMNLP*, 2024. [[2406_20086_token-erasure-as-a-footprint-of-implicit-vocabulary-items-in-llms|↗]]
[^4]: S. Hao, S. Sukhbaatar, D. Su, X. Li, H. Hu, J. Weston, and Y. Tian, "Coconut: Training Large Language Models to Reason in a Continuous Latent Space," arXiv:2412.06769, 2024. [[2412_06769_coconut-training-llms-to-reason-in-a-continuous-latent-space|↗]]
[^5]: W. Su et al., "MedTok: Multimodal Medical Code Tokenizer," arXiv:2502.04397, 2025. [[2502_04397_medtok-multimodal-medical-code-tokenizer|↗]]
[^6]: A. Elhussein et al., "KEEP: Integrating Medical Ontologies with Clinical Data for Robust Code Embeddings," arXiv:2510.05049, 2025. [[2510_05049_keep-integrating-medical-ontologies-with-clinical-data-for-robust-code-embeddings|↗]]
