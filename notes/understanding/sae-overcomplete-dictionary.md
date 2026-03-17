---
title: SAE Overcomplete Dictionaries
tags: [SAE, superposition, dictionary, sparsity, mechanistic-interpretability]
summary: Why SAE hidden dimensions greatly exceed model dimensions — the superposition hypothesis predicts LLMs pack thousands of features into fewer dimensions, and an overcomplete sparse dictionary unpacks them into one concept per direction.
papers: [2405.14860]
---

# SAE Overcomplete Dictionaries

## Why SAE Dimensions >> Model Dimensions

The SAE hidden dimension (e.g. 24576) is much larger than the model's residual stream (e.g. 768). This is intentional — it's called an **overcomplete dictionary**.

### The Superposition Hypothesis

A 768-dim space can only have 768 orthogonal directions. But a model trained on all of human language likely tracks thousands of distinct concepts simultaneously. LLMs handle this via **superposition**: cramming multiple features into the same dimensions by relying on the fact that most features are rarely active at the same time.

The SAE's job is to **unpack** that superposition into a larger space where each concept gets its own dedicated direction[^1]:

```
768 dims (superposed, dense)  →  SAE  →  24576 dims (sparse, one concept per dim)
```

### Why Sparsity Makes This Possible

Any given token activates maybe 20–50 of the 24576 features. If features fired densely, the overcomplete dictionary would be geometrically infeasible. Sparsity is what gives the expansion room to work.

### The Expansion Factor

24576 / 768 = **32× expansion**. This is a hyperparameter:
- Too small → misses concepts, features remain entangled
- Too large → expensive to train, harder to interpret
- Typical range in the literature: **8×–64×**

### Analogy

The 768-dim model space is like a ZIP file — all the information is there but entangled. The SAE's 24576-dim space is the unzipped version, where each file (feature) is separate and identifiable.

---

[^1]: J. Engels, I. Liao, E. J. Michaud, W. Gurnee, and M. Tegmark, "Not All Language Model Features Are Linear," in *Proc. ICLR*, 2025. [[2405_14860_not-all-lm-features-are-linear|↗]]
