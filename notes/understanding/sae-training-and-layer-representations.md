# SAE Training & Layer-Wise Representations

## What Training an SAE Means

A Sparse Autoencoder (SAE) is a neural network trained to decompose an LLM's dense internal activations into a large, interpretable dictionary of features.

Given an LLM's hidden state (e.g. the 768-dim residual stream in GPT-2), the SAE learns to approximate it as:

```
hidden_state ≈ Σ aᵢ · dᵢ
```

where `dᵢ` are **dictionary vectors** (learned feature directions) and `aᵢ` are scalar activations — with most `aᵢ = 0` (sparsity constraint).

The SAE receives only an anonymous matrix of activation vectors — no token IDs, text, or positions:

```
Input to SAE: matrix of shape [N_tokens, d_model]
              e.g.            [1024,     768     ]
              N_tokens anonymous vectors, no labels, no token IDs, no positions
```

### Training Objective

```
minimize: reconstruction_loss (MSE) + λ · sparsity_penalty (L1 on activations)
```

- **Reconstruction loss**: the SAE output must closely match the original activation.
- **Sparsity penalty**: forces most features off at any given time, so each feature fires only on specific, semantically coherent inputs.

The tension between these two drives the SAE to find a dictionary where features are both useful and specific.

### Why Sparsity Matters for Interpretability

If each token only activates a few features, each feature tends to correspond to a coherent concept (e.g. "this token is a month name"). Dense representations lack this property — no single dimension has a clean meaning.

---

## Do the Same Concept's Directions Differ Across Layers?

**Yes — for two distinct reasons.**

### 1. The Representation Genuinely Changes Across Layers

Each layer transforms the residual stream. Early layers encode surface/syntactic features; middle layers build semantic content; later layers shift toward next-token prediction. The direction encoding "this token is a month" in layer 4 is doing different computational work than in layer 8 — they are not the same vector even if both are interpretable.

### 2. SAEs Are Trained Independently Per Layer

Each layer's SAE sees only that layer's activations and learns its own dictionary from scratch. There is no constraint tying layer 4's "month" feature to layer 8's. Even if the underlying representation were identical across layers, two independently trained SAEs would find different orientations — analogous to PCA finding the same subspace but rotated differently each run.

---

## A Further Subtlety: SAEs Aren't Unique Even Within One Layer

Paulo & Belrose (2025) — *"Sparse Autoencoders Trained on the Same Data Learn Different Features"* — show that two SAEs trained on the **same layer** with different random seeds find overlapping but distinct feature sets (~30% shared in some experiments). The dictionary is not unique; it's one of many valid decompositions.

---

## Implication for Engels et al.

This is why Engels et al.[^1] focus on the **subspace** spanned by a cluster of features rather than any individual feature direction. The circular geometry (the ring of month vectors) is more stable than any single dictionary element — the subspace is what the model actually uses, while the specific SAE basis within it is somewhat arbitrary.

---

[^1]: J. Engels, I. Liao, E. J. Michaud, W. Gurnee, and M. Tegmark, "Not All Language Model Features Are Linear," in *Proc. ICLR*, 2025. [[2405_14860_not-all-lm-features-are-linear|↗]]
