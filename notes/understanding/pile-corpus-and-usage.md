# The Pile Corpus — What It Is and How the Papers Use It

## What the Pile Is

The Pile is a large open-source text dataset assembled by EleutherAI, comprising ~825GB of diverse English text from 22 sources:

| Source type | Examples |
|---|---|
| Web crawl | Common Crawl, OpenWebText |
| Books | Books3, Project Gutenberg |
| Academic | PubMed Abstracts, ArXiv, FreeLaw |
| Code | GitHub |
| Reference | Wikipedia, DM Mathematics |
| Other | HackerNews, YouTube subtitles, Enron Emails, USPTO patents |

The papers[^1][^2] use the **uncopyrighted subset**, streamed directly from HuggingFace without a full local download:

```python
data = hf_dataset_to_generator("monology/pile-uncopyrighted")
```

## Medical Content in the Pile

PubMed Abstracts is one of the 22 sources, so some clinical language is present. However, specific SNOMED CT concept names (e.g. "bronchiectasis", "dyspnoea", "pneumothorax") appear **rarely** relative to the total volume of text. To collect enough activations per concept to do meaningful geometric analysis, an impractically large portion of the corpus would need to be processed. Common lay terms ("asthma", "fever", "pain") occur more frequently but still in highly variable contexts — a news article, a patient forum, and a clinical note all produce different residual stream activations for the same token.

## How the Papers Use the Pile

The script `generate_feature_occurence_data.py` streams raw Pile text, tokenises it in chunks of 256 tokens, runs each chunk through the model, encodes every token's residual stream activation through the SAE, and saves all nonzero feature activations to disk. It targets **1 billion SAE activation pairs** per layer:

```python
ctx_len = 256
num_sae_activations_to_save = 10**9  # 1 billion pairs

while total_pairs_saved < num_sae_activations_to_save:
    activations, tokens = next_batch_activations()   # raw Pile → tokenise → run_with_cache
    hidden_sae = ae.encode(activations)              # SAE encode all token positions
    nonzero_sae = hidden_sae.abs() > 1e-6            # keep only active features
    # ... save nonzero (feature_index, activation_value, token_position) triples
```

Four arrays are saved per layer in a compressed `.npz` file:

| Array | Content |
|---|---|
| `sparse_sae_values` | Activation strength for each nonzero SAE feature |
| `sparse_sae_indices` | Which SAE feature (0–24575 for GPT-2) fired |
| `all_token_indices` | Position in the full token stream where it fired |
| `all_tokens` | The actual token IDs for the entire processed corpus |

There is no concept filtering at this stage — **every token at every position is processed and saved**.

## How Token Filtering Works

Concept filtering happens afterwards in `1-process_sae_activations.ipynb`. The saved `all_tokens` array maps each position in the corpus to a token ID. To find all occurrences of e.g. "Monday":

1. Decode `all_tokens` using the model's tokenizer → list of token strings
2. Look up which positions contain the target token (e.g. `"▁Monday"` in Mistral's SentencePiece vocabulary)
3. Use `all_token_indices` to retrieve only the SAE activations that fired at those positions
4. Reconstruct the residual stream contribution from those SAE features using the decoder matrix

```python
# From 1-process_sae_activations.ipynb
token_strs = tokenizer.batch_decode(sparse_activations['all_tokens'])

days = []
mask_days = []
for i, token_i in enumerate(token_indices_days):
    token = token_strs[token_i].replace("▁", "").lower().strip()
    if token in days_of_week:          # {"monday": 0, "tuesday": 1, ...}
        mask_days.append(True)
        days.append(token)
    else:
        mask_days.append(False)

X_days = reconstructions_days[mask_days, :]   # keep only matched positions
```

A secondary filter is also applied for the years experiment — only tokens that are numeric strings in the range 1900–1999 are kept, discarding any year token that appears in a non-year context.

## Why This Approach Does Not Transfer to Medical Concepts

The Pile pipeline works for days/months/years because:
- Those tokens are **very common** in natural text — billions of occurrences across 825GB
- Each token is a single, unambiguous BPE unit ("Monday", "January", "1987")
- Context does not dramatically change the meaning — "Monday" always means the same day

For SNOMED CT concepts:
- Most precise clinical terms are **rare** in general text
- Many are **multi-token** (e.g. "bronchiectasis" → 4 tokens in GPT-2)
- Context is highly variable and domain-dependent

The practical alternative is to use **structured prompts** (e.g. `"The patient was diagnosed with {concept}."`) which give controlled, consistent context and guarantee one activation per concept regardless of corpus frequency.

---

[^1]: J. Engels, I. Liao, E. J. Michaud, W. Gurnee, and M. Tegmark, "Not All Language Model Features Are Linear," in *Proc. ICLR*, 2025. [[2405_14860_not-all-lm-features-are-linear|↗]]
[^2]: A. Modell et al., "The Origins of Representation Manifolds in Large Language Models," arXiv:2505.18235, 2025. [[2505_18235_the-origins-of-representation-manifolds-in-large-language-models|↗]]
