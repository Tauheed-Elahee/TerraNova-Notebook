# Token Embedding Layer vs text-embedding-3-large

No LLM uses `text-embedding-3-large` internally — including OpenAI's own models. They are fundamentally different systems built for different purposes.

---

## Token Embedding Layer (inside every LLM)

Every transformer LLM has a lookup table at the start:

```
vocabulary of ~32,000–128,000 tokens
each token → one learned vector (e.g. 4096-dim for Llama-3)
```

- Trained **jointly with the rest of the model** via next-token prediction
- Vectors have no meaning at initialisation — they acquire meaning through backpropagation across billions of training tokens
- Embeds **one token at a time** — "Asthma" may be one token, but "myocardial infarction" is split into several tokens, each embedded separately before attention combines them
- The embedding for "Asthma" is whatever direction in 4096-dim space best helped the model predict what comes next after seeing "Asthma" across all training documents

---

## text-embedding-3-large

A completely separate model, purpose-built to produce **sentence/phrase-level semantic embeddings**:

```
"Asthma is a chronic respiratory condition" → [3072-dim vector]
```

- Entire input string is processed and collapsed into one vector capturing overall meaning
- Trained with **contrastive learning** — similar sentences pushed close together, dissimilar ones pushed apart
- Not trained for next-token prediction
- No intermediate layers to extract from — one vector out, period

---

## Side-by-Side

| | Token embedding layer | text-embedding-3-large |
|---|---|---|
| Purpose | Next-token prediction | Semantic similarity |
| Training objective | Cross-entropy (next token) | Contrastive loss |
| Input unit | One token | Full string |
| Output | One vector per token | One vector per string |
| Dimensions | Model-dependent (e.g. 4096) | 3072 |
| Layers | First of many | Single output |
| Used inside LLMs | Yes, every LLM has one | No |

---

## Role in This Project

The `text-embedding-3-large` database of SNOMED CT concepts acts as a **semantic oracle** — a clean reference for what the geometric relationships between medical concepts *should* look like. The research question becomes: at which layer of the LLM does the residual stream geometry most closely match this oracle, and does either align with the SNOMED CT ontological distances?[^1][^2]

---

[^1]: J. Engels, I. Liao, E. J. Michaud, W. Gurnee, and M. Tegmark, "Not All Language Model Features Are Linear," in *Proc. ICLR*, 2025. [[2405_14860_not-all-lm-features-are-linear|↗]]
[^2]: A. Modell et al., "The Origins of Representation Manifolds in Large Language Models," arXiv:2505.18235, 2025. [[2505_18235_the-origins-of-representation-manifolds-in-large-language-models|↗]]
