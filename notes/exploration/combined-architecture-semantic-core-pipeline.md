---
title: Combined Architecture — Semantic Core Pipeline
tags: [architecture, tokenization, vocabulary-expansion, detokenization, tuned-lens, semantic-core, injection, layers, pipeline]
summary: A combined architecture exploiting the input-side detokenisation (layer ~12) and output-side prediction stabilisation (layer ~20) to define a semantic core window, enabling direct concept injection, vocabulary expansion, and a three-stage geometric analysis experimental design.
papers: [2410.05864, 2303.08112, 2502.04397, 2510.05049, 2505.20133, 2406.20086, 2405.14860, 2412.06769, 2508.17953, 2505.18235, 1907.08650, 2502.13063]
---

# Combined Architecture — Semantic Core Pipeline

## The Symmetric Layer Structure

Two findings bracket the middle layers of a transformer as a **semantic core**. Assembling them this way is itself a hypothesis: the two boundaries were measured independently on different models, and whether they are symmetric for any given model must be verified empirically before relying on the semantic core framing.

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

**Note on layer numbers and model choice.** The figures ~12 and ~20 are derived from experiments on specific models (GPT-2-scale for Token Erasure; similar scale for Tuned Lens). Model choice is therefore a prerequisite upstream of layer calibration: medical concept representation quality varies by pretraining corpus, and a model with PubMed or clinical text in training will have stronger representations for rare SNOMED concepts than a general model — independently of layer structure. Once a model is chosen, the boundaries must be re-derived empirically: use Token Erasure (2406.20086) to locate the detokenisation completion layer and Tuned Lens probing to locate the prediction stabilisation layer. The absolute numbers will differ. Detokenisation is a local, bottom-up process (assembling subword fragments), while prediction stabilisation depends on context depth and task complexity, so there is no a priori reason the two boundaries must be symmetric. Verify empirically for each model.

## Extraction and Injection at Layer ~12

### Extraction (required for all three stages)

Feed a concept name (e.g. `"invasive ductal carcinoma of breast"`) through the model's lower layers and extract the last-token hidden state `h₁₂` at the detokenisation layer. This vector is the concept representation used for geometric analysis in all three stages. No training is required, and there are no KV-cache complications: this is a standard single forward pass.

Mean-pooling of token hidden states at layer ~12 across all positions of the concept name is a co-equal alternative extraction method (see Subword Compositionality below). Both should be computed; if they agree on the geometry the result is robust to extraction method choice.

### Injection (separate inference pipeline)

For an inference-time speedup, instead of re-running layers 0–11 for a concept already in the extraction cache, inject `h₁₂` directly into the residual stream at layer ~12, bypassing layers 0–11. This is standard activation patching — the injected vector is already in the correct distribution because it came from layer 12. No training is required.

**The KV-cache problem is non-trivial.** Layers 12+ attend over all positions. Collapsing a 4-token concept to a single injection position requires replacing the 4-token KV entries with a single entry at the injection layer. This is not just a bookkeeping change: positions that attended to the original 4 tokens now attend to one, changing the effective attention pattern throughout the upper layers in a way the model has never seen during training. Whether the model degrades gracefully at this intervention is an empirical question and a potential failure mode, not a solved engineering problem.

This differs from Coconut[^4] (which feeds hidden states back to layer 0 and requires training) and from vocabulary expansion (which adds a new input embedding and runs all layers). The KV collapse must be validated experimentally before the injection pipeline is used for inference.

## Output Extraction at Layer ~20

Symmetrically, instead of running layers 20–32 to obtain the output token, extract the prediction at layer ~20 using the tuned lens translator:

```
h₂₀ → tuned_lens_translator[20] → logits → predicted token
```

Combined with input injection at layer ~12, the full pipeline for a known concept becomes:

```
h₁₂  →  [layers 12–20]  →  h₂₀  →  tuned lens  →  output
```

This pipeline operates entirely within the semantic core — no tokenisation artefacts at either boundary. The relevant property is semantic purity: both input and output representations are measured in the window where the model is known to operate on unified concept vectors.

## Three-Stage Geometric Experiment

The architecture supports a clean experimental progression to study whether ontological structure is present in LLM representations and where it comes from:

### Stage 1 — Baseline Geometry (frozen model, standard tokenizer)
Extract last-token hidden states at layer ~12 for SNOMED CT concepts using the standard tokeniser. Measure pairwise distances and compare to SNOMED ontological distances.

**Preliminary validation.** Before running Stage 1 at scale, run Token Erasure probing on a sample of ~50–100 SNOMED concepts of varying length and rarity. This serves two purposes: (a) confirm the actual detokenization completion layer for medical terminology on the chosen model — it may differ from the ~12 figure measured on general English; (b) estimate the failure rate for this concept class. Tokens2Words reports ~23% of multi-token words fail to detokenize cleanly, but that figure is for general English. Named entities show the strongest erasure signal, which should help, but long latinate compounds like `"malignant neoplasm of upper outer quadrant of female breast"` are structurally unlike the words the failure rate was measured on.

**Extraction methods.** Run both last-token and mean-pooling extraction as co-primary methods. Subword Compositionality (2508.17953) shows composition ≈ addition in most LLMs, meaning mean-pooling of token hidden states at layer ~12 should produce nearly the same concept vector as last-token extraction without depending on the erasure mechanism. Mean-pooling is therefore the more robust default: it does not require identifying the erasure layer and is unaffected by the detokenisation failure rate. If the two methods agree on the geometric results, the finding is robust to extraction method choice. If they diverge, the discrepancy is itself informative.

**Pretraining frequency as a confound.** SNOMED concepts vary enormously in how often they appear in typical LLM pretraining data — breast cancer subtypes appear in millions of documents; rare orphan diseases appear in dozens. A low aggregate distance correlation could mean "LLMs don't encode SNOMED structure" or could mean "half the concept set is so rare the model never learned a stable representation." To separate these, either stratify results by estimated pretraining frequency (using a proxy such as Wikipedia article existence or Google NGram frequency) or restrict the primary analysis to a well-attested subset, reporting the full-concept-set result separately.

**SNOMED distance metric.** "Ontological distances" should be operationalised as two separate conditions: (1) shortest-path distance on the raw `is-a` graph, and (2) an information-content-based metric (Resnik or Lin similarity), which weights edges by how specific a concept is in the hierarchy. IC-based distances may correlate better with LLM representations because both reflect training data frequency — the model sees rarer concepts less often, and IC penalises common ancestors more heavily. Treat the two distance conditions as independent, not interchangeable.

**Expected effect size.** Snomed2Vec embeddings are a near-upper-bound on geometric correlation (graph-derived, explicitly trained on SNOMED structure); KEEP embeddings are a pretrained-embedding baseline already available for comparison at Stage 1 (see Relationship to Other Papers). LLM residual streams, which encode SNOMED structure only implicitly through pretraining, should produce a weaker correlation — realistically Spearman ρ ~ 0.2–0.4 for a well-attested concept subset. Concept set size and selection should be designed to detect a moderate effect: a broad random sample across SNOMED is likely underpowered, while a controlled set from a single subtree at varying depths (as noted in the Snomed2Vec discussion below) is better calibrated for this signal range.

> *What does the LLM implicitly know about SNOMED structure?*

### Stage 2 — Expanded Vocabulary Geometry (frozen model, new tokens)
Add SNOMED concepts as single tokens. The concept now enters at layer 0 as a single token rather than being assembled across layers 0–12. Re-run geometric analysis.

**Initialisation and the distribution mismatch.** New token embeddings cannot simply be initialised from Stage 1 layer-12 vectors: layer-12 residual stream representations are in a different distribution from layer-0 input embeddings, so feeding a layer-12 vector into layer-0 places the model out of distribution for the entire forward pass. The correct approach is Token Distillation[^7], which trains new input embeddings to reproduce the mid-layer attention patterns of the original multi-token sequence. This is not merely complementary to Stage 2 — it is the required method for Stage 2 to be a valid experiment.

**Stage 2 is not a purely frozen-model experiment.** The base model weights are frozen, but Token Distillation trains new embeddings. This introduces a confound: any delta between Stage 1 and Stage 2 could reflect tokenisation granularity *or* imperfect distillation (i.e., the new embedding does not perfectly reproduce the internal state the multi-token sequence would have produced). This limitation should be acknowledged when interpreting the Stage 1→2 comparison.

> *Does feeding concepts as atomic units change internal geometry? Does the semantic core shift?*

The delta between Stage 1 and Stage 2 isolates the effect of **tokenisation granularity**.

### Stage 3 — Ontology-Supervised Geometry (trained embeddings) [upper bound / future work]
Train a MedTok[^5]-style encoder so input representations explicitly encode ontological graph position. Re-run geometric analysis. This is the trained-from-scratch upper bound — maximum ontological signal by design.

Stage 3 requires training a full encoder, which is a qualitatively larger undertaking than Stages 1 and 2 (both frozen-model extraction experiments). It is the intended upper bound for comparison but is not a prerequisite for Stages 1 and 2. Note that KEEP[^6] embeddings, which integrate ontological structure with clinical co-occurrence data without requiring a new encoder to be trained from scratch, are available as a pretrained-embedding reference point at Stage 1 — a different and lower-cost baseline than Stage 3.

> *How much geometry is recoverable when ontology is explicitly supervised?*

The delta between Stage 2 and Stage 3 isolates the effect of **ontological supervision**.

| Stage | What varies | Key delta | Scope |
|---|---|---|---|
| 1 → 2 | Tokenisation granularity | Effect of atomic vs. assembled concept input | Frozen model (base weights); new embeddings trained via Token Distillation |
| 2 → 3 | Ontological supervision | Effect of explicit graph structure in embeddings | Requires training |

Stages 1 and 2 are independent once the concept set is fixed. Token Distillation training for Stage 2 does not depend on Stage 1 results and can begin in parallel.

## Relationship to Other Papers

- **Token Distillation[^7]**: the required initialisation method for Stage 2 — distils mid-layer hidden states into new input embeddings by matching attention patterns, resolving the layer-0/layer-12 distribution mismatch that naive initialisation would introduce.
- **Cramming[^8]**: compresses long sequences into a single vector via cross-attention. An alternative initialisation strategy for Stage 2 for particularly long SNOMED concept names (e.g., `"malignant neoplasm of upper outer quadrant of female breast"`) where Token Distillation has more information to compress and less prior to anchor to.
- **Subword Compositionality[^9]**: shows mean-pooling ≈ last-token extraction for most LLMs (composition ≈ addition). This makes mean-pooling a primary extraction method for Stage 1, not just a sanity check: it does not require identifying the erasure layer and is unaffected by the detokenisation failure rate. If mean-pooling and last-token extraction agree on the geometric results, the finding is robust to extraction method choice.
- **Snomed2Vec[^10]**: Poincaré embeddings as a geometric baseline. Since hyperbolic and Euclidean embeddings live in different spaces, the comparison requires a proxy measure: compute rank correlation of pairwise distances (SNOMED shortest-path distance vs. cosine distance in the residual stream vs. hyperbolic distance in Snomed2Vec) across a fixed concept set. This tests whether LLM geometry preserves the same ordinal structure as an explicitly hyperbolic embedding, without requiring a projection between spaces. **Distance metric choice is also load-bearing.** The SNOMED side of the rank correlation should be computed under two conditions: (1) shortest-path distance on the `is-a` graph; (2) an IC-based metric (Resnik or Lin), which weights by concept specificity in the hierarchy. IC-based distances may correlate better with LLM representations because both reflect training data frequency — this should be treated as a separate condition, not a synonym for shortest-path. **Concept set selection is load-bearing here.** Concepts sampled broadly from across SNOMED's graph will be far apart in shortest-path distance and may show no meaningful distance gradient in LLM representations — not because the geometry is absent but because the training signal for distant concepts is weak or absent. A controlled set drawn from a single subtree at varying depths (e.g., a disease hierarchy) is more likely to be diagnostic.
- **Not All Features Linear[^11] + Origins of Manifolds[^12]**: the geometric analysis toolkit for all three stages — SAE clustering, causal validation, and manifold geometry analysis. Note on expected shape: Engels et al. find *circular* manifolds for periodic temporal features (days, months, years), which are ring-structured by construction. SNOMED's `is-a` hierarchy is a DAG. If manifold structure exists in LLM representations of SNOMED concepts it should be *hyperbolic* rather than circular — tree-like with exponential volume growth. This connects directly to Snomed2Vec's finding that Poincaré (hyperbolic) embeddings outperform Euclidean ones for SNOMED. The SAE clustering and causal validation methodology from Engels et al. transfers; the specific manifold shape hypothesis does not. For a DAG-structured ontology the appropriate geometric tests are: **Gromov δ-hyperbolicity** (does the metric space satisfy the four-point condition?), **UMAP with hyperbolic metric** (visualisation in hyperbolic space), and **hyperbolic probing classifiers** (do residual stream vectors predict ancestor/descendant relationships in hyperbolic space?).
- **Token Erasure[^3]**: marks the detokenisation completion point — the layer of maximal erasure is the model-specific injection target and the extraction layer for Stage 1.
- **KEEP[^6]**: produces embeddings where ontological proximity is reflected in vector distance by jointly training on SNOMED graph structure and clinical co-occurrence data. KEEP is a pretrained-embedding baseline for the Stage 1 geometric analysis — run the same pairwise distance correlation on KEEP embeddings, text-embedding-3-large, and LLM residual streams against the same SNOMED distance matrix. This three-way comparison directly quantifies how much ontological structure each representation type captures. KEEP sets the pretrained upper bound; Stage 3 sets the trained-from-scratch upper bound. These are distinct reference points.

### Cross-paper relationships worth emphasising

**KEEP + LLM residual streams as a Stage 1 geometric comparison.** Running the same pairwise distance analysis on KEEP embeddings, text-embedding-3-large (from Origins of Manifolds), and LLM residual streams against the same SNOMED distance matrix — on the same concept set — produces a three-way comparison that directly quantifies how much ontological structure each representation type captures. This is the most immediately deployable comparison the design enables, and it requires no training: KEEP and text-embedding-3-large are both available off the shelf.

**Subword Compositionality + Token Erasure as complementary extraction strategies for the same problem.** Token Erasure identifies the detokenisation layer by tracking where erasure is maximal; Subword Compositionality shows mean-pooling works without identifying the layer at all. They approach the same question from opposite directions. If both methods produce the same geometric result for Stage 1, the finding is robust to extraction method choice. If they diverge, the discrepancy is informative about what the model is actually doing at the detokenisation layer.

**Origins of Manifolds + Snomed2Vec on the hyperbolic geometry question.** Origins of Manifolds extends Engels et al. to text-embedding-3-large, showing manifold structure is present in semantic embedding space beyond model internals. Snomed2Vec shows Poincaré (hyperbolic) embeddings outperform Euclidean for SNOMED. Together they frame the most scientifically specific testable prediction in this architecture: do representation manifolds for SNOMED concepts in LLM hidden states exhibit hyperbolic geometry — consistent with the structure Snomed2Vec found optimal — even without explicit ontological supervision?

---

[^1]: R. Kaplan, S. Oren, U. Reif, and R. Schwartz, "From Tokens to Words: On the Inner Lexicon of LLMs," in *Proc. ICLR*, 2025. [[2410_05864_from-tokens-to-words-on-the-inner-lexicon-of-llms|↗]]
[^2]: N. Belrose, Z. Furman, L. Smith, D. Strauss, N. Nanda, and J. Steinhardt, "Eliciting Latent Predictions from Transformers with the Tuned Lens," arXiv:2303.08112, 2023. [[2303_08112_tuned-lens-eliciting-latent-predictions-from-transformers|↗]]
[^3]: S. Feucht, T. Atkinson, E. Wallace, and D. Bau, "Token Erasure as a Footprint of Implicit Vocabulary Items in LLMs," in *Proc. EMNLP*, 2024. [[2406_20086_token-erasure-as-a-footprint-of-implicit-vocabulary-items-in-llms|↗]]
[^4]: S. Hao, S. Sukhbaatar, D. Su, X. Li, H. Hu, J. Weston, and Y. Tian, "Coconut: Training Large Language Models to Reason in a Continuous Latent Space," arXiv:2412.06769, 2024. [[2412_06769_coconut-training-llms-to-reason-in-a-continuous-latent-space|↗]]
[^5]: W. Su et al., "MedTok: Multimodal Medical Code Tokenizer," in *Proc. ICML*, 2025. [[2502_04397_medtok-multimodal-medical-code-tokenizer|↗]]
[^6]: A. Elhussein et al., "KEEP: Integrating Medical Ontologies with Clinical Data for Robust Code Embeddings," arXiv:2510.05049, 2025. [[2510_05049_keep-integrating-medical-ontologies-with-clinical-data-for-robust-code-embeddings|↗]]
[^7]: K. Dobler, D. Elliott, and G. de Melo, "Token Distillation: Attention-Aware Input Embeddings for New Tokens," 2025. [[2505_20133_token-distillation-attention-aware-input-embeddings-for-new-tokens|↗]]
[^8]: Y. Kuratov, M. Arkhipov, A. Bulatov, and M. Burtsev, "Cramming 1568 Tokens into a Single Vector and Back Again," in *Proc. ACL*, 2025. [[2502_13063_cramming-1568-tokens-into-a-single-vector-and-back-again|↗]]
[^9]: Y. Peng, S. Chai, and A. Søgaard, "Understanding Subword Compositionality of Large Language Models," 2025. [[2508_17953_understanding-subword-compositionality-of-large-language-models|↗]]
[^10]: V. Agarwal, T. Eftimov, R. Addanki, S. Choudhury, S. Tamang, and R. Rallo, "Snomed2Vec: Random Walk and Poincaré Embeddings of a Clinical Knowledge Base for Healthcare Analytics," in *KDD DSHealth*, 2019. [[1907_08650_snomed2vec-poincare-embeddings-clinical-knowledge|↗]]
[^11]: J. Engels, I. Liao, E. J. Michaud, W. Gurnee, and M. Tegmark, "Not All Language Model Features Are Linear," in *Proc. ICLR*, 2025. [[2405_14860_not-all-lm-features-are-linear|↗]]
[^12]: A. Modell, P. Rubin-Delanchy, et al., "The Origins of Representation Manifolds in Large Language Models," 2025. [[2505_18235_the-origins-of-representation-manifolds-in-large-language-models|↗]]
