---
title: SAE Token Matching & Intervention
tags: [SAE, token-matching, intervention, causal-validation, mechanistic-interpretability]
summary: How SAE features are post-hoc matched to tokens by running the encoder on a labelled corpus, and how hooking SAEs into the residual stream at inference time enables both inspection and causal intervention by rotating feature activations.
papers: [2405.14860]
---

# SAE Token Matching & Intervention

## Does the SAE Match Activations to Tokens?

**No — not during training.** The SAE trains on an anonymous matrix of activation vectors with no token IDs, text, or position information. It is purely geometric.

## Post-Hoc Token Matching (Interpretability Analysis)

After training, researchers run the SAE on a corpus where they *do* track which token produced which activation:

```python
for token, activation in zip(tokens, activations):
    feature_activations = sae.encode(activation)  # which features fired?
    for feature_idx, strength in feature_activations:
        log(feature_idx, token, strength)
```

This produces a lookup: **for each dictionary feature, which tokens caused it to fire?**

If feature #4445 consistently activates on "Monday", "Tuesday", "Wednesday" and rarely anything else — it gets labelled a "day of week" feature. This is the basis of all interpretability claims in Engels et al.[^1]

In the repo, `sae_multid_feature_discovery/generate_feature_occurrence_data.py` performs exactly this step.

### Token Position

Position is ignored entirely — by the SAE and in the matching step. Two activations from the same token type at different sentence positions are treated identically. This works because the LLM already encodes token identity consistently regardless of position.

## Full Analysis Pipeline

```
Train SAE         → no token awareness, purely geometric
        ↓
Analyze SAE       → run on labeled corpus, match features to tokens
        ↓
Interpret results → "feature #4445 = days of week"
        ↓
Cluster features  → cosine similarity between decoder vectors of co-firing features
```

---

## Hooking SAEs Into the Model for Inspection & Intervention

You don't replace model layers permanently — the LLM weights stay frozen. The SAE is inserted as a **transparent wrapper at inference time**:

```
Normal forward pass:
  token → layer 7 → residual stream (768-dim) → layer 8 → ...

With SAE hooked in:
  token → layer 7 → residual stream → SAE encode → sparse features → SAE decode → layer 8 → ...
```

Since the SAE reconstructs the residual stream faithfully, the rest of the model behaves nearly identically. The small discrepancy is called **reconstruction error**.

### Inspection

See which features fire on a given token at a given layer:

```python
features = sae.encode(activation)
# e.g. feature #4445 fires with strength 2.3 → "day of week" feature active
```

### Intervention (Causal Validation)

Modify the sparse features before decoding back into the residual stream:

```python
features = sae.encode(activation)
features[day_of_week_features] = rotate(features, 90_degrees)  # Monday → Thursday
modified_activation = sae.decode(features)
# inject modified_activation back into residual stream
```

Engels et al. used exactly this approach — rotating activations around the circular feature subspace and verifying the model's output changed accordingly (e.g. predicted a different day). This proved the circular features are **causally active**, not just correlational.

### Limitation

Reconstruction error accumulates if you hook SAEs into multiple layers simultaneously. In practice, researchers hook into **one layer at a time**.

---

[^1]: J. Engels, I. Liao, E. J. Michaud, W. Gurnee, and M. Tegmark, "Not All Language Model Features Are Linear," in *Proc. ICLR*, 2025. [[2405_14860_not-all-lm-features-are-linear|↗]]
