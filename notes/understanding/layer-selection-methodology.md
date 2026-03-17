# Layer Selection: GPT-2 Layer 7 & Mistral-7B Layer 8

Notes on how Engels et al.[^1] arrived at these specific layers.

## Short Answer

Layer selection was driven by **SAE availability** and **empirical ranking**, not a pre-defined theoretical criterion.

---

## GPT-2 — Layer 7

- Bloom (2024) trained SAEs for *every* layer of GPT-2, giving full coverage.
- The authors ran their automated feature discovery pipeline across all 12 layers.
- Layer 7 was where the circular clusters (days, months, years) ranked highest by the combined prominence score (see below).

## Mistral-7B — Layer 8

- Due to computational cost, SAEs were only trained on **layers 8, 16, and 24** — not every layer.
- Layer 8 is the first of those three and showed the strongest circular signal.
- The paper explicitly notes "we only have layer 8 clustering results for Mistral" for some experiments, confirming availability was a binding constraint.

---

## How Prominence Was Calculated

### Step 1 — Graph-Based Clustering (Detection)

A complete graph is built over all SAE dictionary elements, with edge weights = **cosine similarity between decoder vectors**. Edges below a threshold are pruned. Connected components become candidate multi-dimensional feature clusters — groups of features pointing in geometrically related directions.

### Step 2 — Irreducibility Scoring (Ranking)

Each cluster is scored on two metrics (Definition 3 in the paper):

| Metric | What it measures | High score means… |
|---|---|---|
| **Epsilon-mixture index** | How often a feature's activation can be projected near zero while still active | Low → feature genuinely needs multiple dimensions |
| **Separability index** | Minimal mutual information across all possible lower-dimensional decompositions | High → cluster can't be split into independent sub-features |

**Combined score = `(1 − epsilon-mixture index) × separability index`**

All 1,000 clusters are ranked by this product. The interpretable clusters ranked:
- Days of the week: **9th**
- Years of the 20th century: **15th**
- Months of the year: **28th**

### Step 3 — Visual Confirmation

PCA projections of hidden states across prompts were inspected at various layers. The layer where the circular structure appeared clean and well-separated confirmed the quantitative ranking.

---

## Key Takeaway

For GPT-2, layer 7 was found by exhaustive search. For Mistral, layer 8 was the earliest of three feasible layers and happened to contain the strongest signal. Neither was chosen by prior hypothesis.

---

[^1]: J. Engels, I. Liao, E. J. Michaud, W. Gurnee, and M. Tegmark, "Not All Language Model Features Are Linear," in *Proc. ICLR*, 2025. [[2405_14860_not-all-lm-features-are-linear|↗]]
