# Medical Corpora, the Pile, and SAE Distribution

## Could a Medical Corpus Replace the Pile?

### Is the Pile a specifically constructed database?

Yes — the Pile is a deliberately curated dataset, not a raw internet crawl. EleutherAI made explicit choices about which 22 sources to include and in what proportions, specifically to create a diverse, high-quality training corpus for language models. Each source was weighted and filtered. PubMed Abstracts, GitHub, ArXiv, and legal text were all intentionally included alongside web text to produce broad coverage of language domains. It is not the whole internet — it is a specific, versioned, reproducible dataset.

### Medical corpus alternatives

In principle, any text corpus can be substituted for the Pile in `generate_feature_occurence_data.py` — the line:

```python
data = hf_dataset_to_generator("monology/pile-uncopyrighted")
```

can be swapped for any HuggingFace dataset or local text generator. Good medical candidates include:

| Corpus | Content | Availability |
|---|---|---|
| PubMed Central Open Access | Full-text biomedical journal articles | Open |
| `pubmed_abstracts` | 30M PubMed abstracts | Open |
| MIMIC-III / MIMIC-IV | Real clinical notes, discharge summaries | Credentialed (PhysioNet) |
| MedC | Large medical text pretraining corpus | Open |
| S2ORC | Semantic Scholar research papers incl. biomedical | Open |

### The distribution mismatch problem

Using a medical corpus introduces a two-level distribution mismatch:

1. **GPT-2 itself** was trained on WebText (Reddit-curated links) — highly specialised clinical language is outside its training distribution, so its internal representations for rare medical terms may be less structured
2. **The Bloom SAEs** were optimised to sparsely encode Pile-style activations — medical text may activate features in unexpected or less interpretable combinations

The prompt-based approach sidesteps this entirely. A sentence like `"The patient was diagnosed with asthma."` is plain grammatical English — well within GPT-2's distribution — with the medical term embedded in a familiar syntactic frame. This gives a reliable, in-distribution activation for every concept without needing a large medical corpus.

If a model trained on medical text were used instead (e.g. BioMedLM or GatorTron), a medical corpus as input would be the natural match and domain-specific SAEs could be trained on it. For GPT-2 with the Bloom SAEs, structured English prompts are the better fit.

---

## Does the Same Corpus Need to Be Used for SAE Training and Feature Extraction?

No.

### The SAE is a fixed function after training

Once trained, the SAE is a frozen learned matrix operation:

```
activation vector (768-dim) → SAE encoder → sparse feature vector (24576-dim)
```

The weights are fixed. Any activation vector can be passed through it regardless of what text produced that activation. The SAE has no memory of or dependency on the corpus used to train it.

### Why the Pile appears at two stages in the papers

The Pile is used at two points in the papers' pipeline[^1][^2], but for completely different reasons:

| Stage | Why the Pile is used | Required? |
|---|---|---|
| SAE training (done by Bloom 2024, not the papers) | To generate diverse activations so the SAE learns a broad dictionary of features | Yes — the SAE was trained on this distribution |
| `generate_feature_occurence_data.py` | To find natural occurrences of concept tokens in text and collect co-activation statistics | No — any corpus works; the Pile was convenient and already available |

The second use of the Pile is purely about finding tokens in context — streaming text, tokenising it, and recording activations wherever tokens naturally appear. Nothing about the SAE requires the Pile as input.

### The real concern — distribution shift

The meaningful question is not "does it need to be the same corpus" but "will the SAE features be interpretable for my inputs." The Bloom SAEs were trained on Pile activations, so:

- Activations from **Pile-like text** → SAE produces sparse, interpretable features (by design)
- Activations from **structured prompts** (e.g. `"The patient was diagnosed with asthma."`) → SAE still produces a sparse encoding, but features may be less cleanly interpretable because this style of text has a different activation distribution

In practice this is unlikely to be a major problem for short, grammatically simple prompts — GPT-2 has seen plenty of similar sentences in WebText. It becomes more of a concern with highly technical clinical language.

### Bottom line for this project

The Pile is not needed at all. The workflow is:

1. Load the pretrained Bloom SAE (`SAE.from_pretrained("gpt2-small-res-jb", ...)`)
2. Run medical prompts through GPT-2 via TransformerLens
3. Pass those activations through the SAE encoder

The SAE will encode them. The Pile was the papers' source of text to find natural token occurrences — it has no special status in the SAE itself.

---

[^1]: J. Engels, I. Liao, E. J. Michaud, W. Gurnee, and M. Tegmark, "Not All Language Model Features Are Linear," in *Proc. ICLR*, 2025. [[2405_14860_not-all-lm-features-are-linear|↗]]
[^2]: A. Modell et al., "The Origins of Representation Manifolds in Large Language Models," arXiv:2505.18235, 2025. [[2505_18235_the-origins-of-representation-manifolds-in-large-language-models|↗]]
