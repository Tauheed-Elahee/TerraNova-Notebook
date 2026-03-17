---
title: SAE Clustering and Manifold Geometry
tags: [SAE, clustering, manifold, geometry, cosine-similarity, context-variation]
summary: How cosine similarity clustering of SAE decoder vectors reveals multi-dimensional feature clusters, and why context variation across corpus occurrences produces continuous manifold geometry rather than discrete blobs.
papers: [2405.14860, 2505.18235]
---

# SAE Clustering and Manifold Geometry

## What is Being Clustered

The clustering is **not** applied to token activations directly. It is applied to the **SAE feature vectors** (the 24,576 dictionary elements) themselves. Specifically, the cosine similarity between the **decoder vectors** of SAE features is computed, and features with high mutual cosine similarity are grouped into clusters.

```python
# clustering.py clusters the 24,576 SAE decoder directions
# by cosine similarity — not the token activations themselves
```

## Why Clustering is Needed — Two Distinct Reasons

### 1. A concept is encoded by multiple SAE features, not one

Because of superposition, no single SAE feature perfectly captures "days of the week." Instead, a **group** of features collectively encodes the concept — some may fire more strongly for "Monday" in scheduling contexts, others in narrative contexts, others when the day is the subject vs. object of a sentence. These features share similar decoder directions (they all point roughly toward the "day-of-week subspace"), which is why clustering by cosine similarity finds them.

The papers[^1][^2] report the specific SAE feature indices for each discovered cluster in GPT-2 (layer 7):

- Days of week: 9 features — `[2592, 4445, 4663, 4733, 6531, 8179, 9566, 20927, 24185]`
- Months of year: 16 features — `[3977, 4140, 5993, 7299, 9104, 9401, 10449, 11196, 12661, 14715, 17068, 17528, 19589, 21033, 22043, 23304]`
- Years of 20th century: 10 features — `[1052, 2753, 4427, 6382, 8314, 9576, 9606, 13551, 19734, 20349]`

### 2. Context variation is the source of the manifold geometry

The same token ("Monday") produces slightly different activation vectors across thousands of Pile occurrences due to surrounding context. This is not noise to be eliminated — **it is the signal**. After identifying the cluster of day-of-week SAE features, the activation reconstruction:

```python
current_activations += sae_value * decoder_vecs[sae_index]
```

gives a cloud of points for each day. The cloud for "Monday" sits in one region, "Tuesday" in another, and so on. When all seven clouds are plotted together, they arrange into a **ring** — the circular manifold. The context-driven variation within each day's cloud is what gives the manifold its continuous structure rather than seven discrete blobs.

## The Full Pipeline Chain

```
Pile text → GPT-2 → residual stream activations (768-dim)
    → SAE encode → 24,576 sparse features per token
        → cluster SAE features by decoder cosine similarity
            → find day-of-week cluster (9 features for GPT-2)
                → reconstruct activations from cluster features only
                    → cloud of points per day → circular manifold
```

- **Clustering** finds *which features* encode the concept
- **Context variation** across Pile occurrences produces the *spread of points* that reveals the geometry

Both are essential: without clustering you have 24,576 noisy dimensions; without context variation you have seven identical points rather than a continuous manifold.

## Implication for Medical Concepts

For SNOMED CT concepts run through structured prompts rather than the Pile, there is a trade-off:

- **Controlled prompts** reduce context variation → fewer points per concept, less spread → the manifold may be less well-sampled
- **Multiple prompt templates** per concept (e.g. 3–5 different sentence frames) partially compensate by introducing deliberate variation in context
- The absence of a clustering step (since concepts are targeted directly rather than discovered) means the relevant SAE features must either be identified in advance or the full SAE encoding used directly for geometric analysis

---

[^1]: J. Engels, I. Liao, E. J. Michaud, W. Gurnee, and M. Tegmark, "Not All Language Model Features Are Linear," in *Proc. ICLR*, 2025. [[2405_14860_not-all-lm-features-are-linear|↗]]
[^2]: A. Modell et al., "The Origins of Representation Manifolds in Large Language Models," arXiv:2505.18235, 2025. [[2505_18235_the-origins-of-representation-manifolds-in-large-language-models|↗]]
