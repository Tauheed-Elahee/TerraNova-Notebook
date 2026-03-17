---
title: "TransformerLens & SAELens: Activation Extraction and SAE Training Pipeline"
tags: [pipeline, transformer-lens, sae-lens, activations, GPT-2, Mistral]
summary: Step-by-step pipeline for extracting per-layer residual stream activations with TransformerLens and training sparse autoencoders with SAELens, including model and layer coverage for GPT-2 and Mistral-7B.
papers: [2405.14860, 2505.18235]
---

# TransformerLens & SAELens: Activation Extraction and SAE Training Pipeline

## Tools

- **TransformerLens** — hooks into a transformer's internals during a forward pass, allowing you to intercept and save activations at any layer.
- **SAELens** — handles the SAE training loop on top of saved activations.

---

## Step 1 — Extract Activations with TransformerLens

Running a prompt through an LLM normally only returns the final output. TransformerLens exposes the residual stream (or any internal tensor) at every layer via a cache:

```python
model = HookedTransformer.from_pretrained("gpt2")
logits, cache = model.run_with_cache(tokens)

# Access any layer's activations
layer_7_activations = cache["resid_post", 7]  # shape: [batch, seq_len, d_model]
```

```
cache["resid_post", 7].shape == [batch_size, seq_len, d_model]
#                                     ↑           ↑        ↑
#                               sentences      tokens   768 dims
```

For a batch of 8 sentences each 128 tokens long, layer 7 produces `8 × 128 = 1024` activation vectors, each of size 768. **Every token position gets its own activation vector.**

These are saved to disk across many batches until you have a large flat dataset:

```
saved_activations_layer_7.shape == [N_tokens, d_model]
#                                     ↑            ↑
#                                  millions       768
```

Each row is one token from one position in one sentence. Sentence boundaries and positions are discarded — the SAE trains on an unordered set of vectors.

### Why Save to Disk First?

Saving activations decouples the forward pass from SAE training. You only need the large GPU for the forward pass. SAE training can then happen separately and repeatedly without re-running the model.

---

## Step 2 — Train SAEs with SAELens

A separate SAE is trained on each layer's saved activations:

```python
for layer in layers_to_train:
    activations = load_saved_activations(layer)   # load from disk
    sae = SparseAutoencoder(d_model=768, d_hidden=24576)
    sae.train(activations)                         # learn dictionary for this layer
    sae.save(f"sae_layer_{layer}.pt")
```

The SAE receives only the anonymous activation vectors — no token IDs, no text, no positions. It learns purely from the geometry of the activation space.

---

## Full Pipeline

```
Text corpus
    → TransformerLens (forward pass with cache)
        → Activations saved per layer to disk  [N_tokens, d_model]
            → SAELens trains one SAE per layer
                → Each SAE produces a dictionary of feature vectors  [d_hidden, d_model]
                    → Post-hoc: run SAE on labeled corpus to match features → tokens
                        → Engels et al.[^1]: cosine similarity clustering on decoder vectors
```

Modell et al.[^2] reuse the pre-computed activations from this pipeline directly (Part 1 of their paper), extending it with text embeddings from `text-embedding-3-large` to investigate why the manifold structures arise.

---

## GPT-2 vs Mistral Coverage

| Model | Layers with SAEs | Source |
|---|---|---|
| GPT-2 | All 12 layers | Bloom (2024), pre-trained and publicly available |
| Mistral-7B | Layers 8, 16, 24 only | Engels et al.[^1] trained these themselves |

Both sets of activations are reused without modification by Modell et al.[^2]

This asymmetry is why GPT-2 layer selection was exhaustive and Mistral layer selection was "best of three" (see `layer-selection-methodology.md`).

---

[^1]: J. Engels, I. Liao, E. J. Michaud, W. Gurnee, and M. Tegmark, "Not All Language Model Features Are Linear," in *Proc. ICLR*, 2025. [[2405_14860_not-all-lm-features-are-linear|↗]]
[^2]: A. Modell et al., "The Origins of Representation Manifolds in Large Language Models," arXiv:2505.18235, 2025. [[2505_18235_the-origins-of-representation-manifolds-in-large-language-models|↗]]
