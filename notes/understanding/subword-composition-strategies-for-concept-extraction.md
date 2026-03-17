---
title: Subword Composition Strategies for Concept Vector Extraction
tags: [tokenization, subword, composition, concept-extraction, mean-pooling, frame-hypothesis]
summary: Three theoretical frameworks for aggregating sub-word token representations into a single concept vector — last-token detokenisation, frame averaging, and additive composition — and their practical implications for extracting SNOMED CT concept representations from LLM residual streams.
papers: [2410.05864, 2412.07334, 2508.17953]
---

# Subword Composition Strategies for Concept Vector Extraction

## The Core Question

Given a multi-token concept like `"bronchiectasis"` split into several BPE fragments, how do you obtain a single vector that represents the concept? Three frameworks from the literature give different answers.

## 1. Last-Token Extraction (Detokenisation View)

The LLM resolves sub-word fragments into a unified whole-word representation at the **last token position** in early-to-middle layers.[^1] From this perspective, the correct extraction point is:

```python
# Run concept name through lower layers, extract at last token position
concept_vector = cache["resid_post", 12][0, -1, :]
```

This is theoretically well-motivated for autoregressive models where the last token has attended over all preceding tokens via causal attention.

## 2. Frame Averaging (Frame Representation Hypothesis)

Multi-token words are represented as ordered sequences of vectors called *frames*. A concept is the **average of the frames** of all words that express it.[^2]

```python
# Average hidden states across all tokens of the concept name
concept_vector = cache["resid_post", layer][0, :n_tokens, :].mean(dim=0)
```

This extends the Linear Representation Hypothesis to multi-token terms and has been validated across Llama 3.1, Gemma 2, and Phi 3.

## 3. Additive Composition

Empirically, sub-word composition is **approximately isometric to addition** in most LLMs — the composed representation of a multi-token word closely approximates the sum (or mean) of its sub-token representations.[^3] This is the weakest theoretical claim but has the broadest empirical support across model families.

## Comparison

| Strategy | Theoretical basis | Best suited to | Complexity |
|---|---|---|---|
| Last-token | Inner lexicon / detokenisation mechanism | Autoregressive (GPT, Llama, Mistral) | Low |
| Frame average | Frame Representation Hypothesis | Any architecture | Low |
| Additive / mean-pool | Empirical compositionality ≈ addition | Most model families | Lowest |

## Recommendation for This Project

Use **last-token extraction** at the detokenisation layer as the primary method — it has the strongest theoretical motivation for the autoregressive models (GPT-2, Mistral-7B) used in the Engels et al. pipeline. Use **mean pooling** as a baseline sanity check: if the correlation with SNOMED distances is similar under both methods, the geometry is robust to the choice of aggregation strategy.

---

[^1]: R. Kaplan, S. Oren, U. Reif, and R. Schwartz, "From Tokens to Words: On the Inner Lexicon of LLMs," in *Proc. ICLR*, 2025. [[2410_05864_from-tokens-to-words-on-the-inner-lexicon-of-llms|↗]]
[^2]: P. Valois, M. Souza, E. Shimomoto, and K. Fukui, "Frame Representation Hypothesis: Multi-Token LLM Interpretability and Concept-Guided Text Generation," *TACL*, 2025. [[2412_07334_frame-representation-hypothesis-multi-token-llm-interpretability|↗]]
[^3]: Y. Peng, S. Chai, and A. Søgaard, "Understanding Subword Compositionality of Large Language Models," 2025. [[2508_17953_understanding-subword-compositionality-of-large-language-models|↗]]
