---
title: Single-Vector Concept Representations as Transformer Inputs
tags: [tokenization, single-vector, concept-embedding, MedTok, SNOMED, continuous-latent-space, activation-injection]
summary: The body of work on bypassing tokenisation by feeding single dense vectors as direct transformer inputs — from medical code tokenisers to continuous latent reasoning — and what this means for injecting detokenised SNOMED CT representations into upper model layers.
papers: [2502.04397, 2505.20133, 2412.06769, 2502.13063]
---

# Single-Vector Concept Representations as Transformer Inputs

## Motivation

Once a detokenised concept vector has been extracted from the lower layers of a model, a natural question arises: can it be fed back into the upper layers as a direct input, bypassing the tokenisation and embedding stage? The literature shows this is not only feasible but is being actively developed across several lines of work.

## Medical Code Tokenisation (MedTok)

The most directly relevant prior work for this project.[^1] MedTok encodes each SNOMED CT concept as a **single dense vector** combining:
- A language model encoder over the concept's text description
- A graph encoder over the concept's position in the SNOMED CT ontological hierarchy

The resulting vector is used as a drop-in replacement for BPE token sequences in transformer EHR models, with improved downstream clinical prediction performance. The gap this project fills: MedTok does not study the *geometry* of the resulting representation space against the ontological distances.

## Learning Single-Token Embeddings for Multi-Token Phrases (Token Distillation)

Token Distillation[^2] takes a frozen model and learns a new single input embedding for any multi-token phrase by minimising the divergence between the model's attention patterns under the original split tokens versus a single new token. The distillation target is intermediate hidden states — directly operationalising the inner lexicon finding. No fine-tuning of core model weights required.

## Continuous Latent Reasoning (Coconut)

Coconut[^3] demonstrates the most extreme version of this pattern: the model's last hidden state after each forward pass is fed directly back as the next input embedding, bypassing vocabulary projection entirely. The model reasons through a sequence of continuous vectors rather than discrete tokens, enabling BFS-like multi-path reasoning that discrete chain-of-thought cannot represent. This establishes the general technical pattern:

```
last_hidden_state[t] → input_embedding[t+1]
```

## Information Capacity of Single Vectors

A practical concern is whether a single vector can carry enough information to represent a complex multi-token medical concept. Empirically, a single 4096-dim input embedding to Llama-3.1-8B can encode information sufficient to reconstruct 1568+ tokens, with capacity scaling linearly with number of vectors.[^4] For a concept name of 5–10 tokens, capacity is not a limiting factor.

## Relevance to This Project

These papers collectively motivate the following pipeline for layer-wise SNOMED concept geometry analysis:

1. Forward pass each concept name through the lower layers (~layer 12)
2. Extract the last-token hidden state (the detokenised concept vector)
3. Inject this vector as a direct input to upper layers via activation patching
4. Extract residual stream across upper layers for geometric analysis against SNOMED distances

This separates the detokenisation computation (lower layers) from semantic/relational encoding (upper layers), enabling clean layer-wise manifold analysis on post-detokenisation representations.

---

[^1]: Y. Su et al., "MedTok: Multimodal Medical Code Tokenizer," in *Proc. ICML*, 2025. [[2502_04397_medtok-multimodal-medical-code-tokenizer|↗]]
[^2]: K. Dobler, D. Elliott, and G. de Melo, "Token Distillation: Attention-Aware Input Embeddings for New Tokens," 2025. [[2505_20133_token-distillation-attention-aware-input-embeddings-for-new-tokens|↗]]
[^3]: S. Hao et al., "Coconut: Training Large Language Models to Reason in a Continuous Latent Space," 2024. [[2412_06769_coconut-training-llms-to-reason-in-a-continuous-latent-space|↗]]
[^4]: Y. Kuratov, M. Arkhipov, A. Bulatov, and M. Burtsev, "Cramming 1568 Tokens into a Single Vector and Back Again," in *Proc. ACL*, 2025. [[2502_13063_cramming-1568-tokens-into-a-single-vector-and-back-again|↗]]
