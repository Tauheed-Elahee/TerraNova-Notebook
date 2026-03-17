# Prompt Structures and Pipelines Across Both Papers

## Full Experiment Table

| Concept | Model | Pipeline | Single token? | Prompt structure | How prompt was used |
|---|---|---|---|---|---|
| Days of week | GPT-2 small (layer 7) | SAE → cluster reconstruction | Yes | None — raw Pile corpus text | Model run over Pile; activations collected at every natural occurrence of the token in corpus text |
| Months of year | GPT-2 small (layer 7) | SAE → cluster reconstruction | Yes | None — raw Pile corpus text | Same as above |
| Years (20th century) | GPT-2 small (layer 7) | SAE → cluster reconstruction | Yes | None — raw Pile corpus text | Same as above |
| Days of week | Mistral-7B (layer 8) | SAE → cluster reconstruction | Yes | None — raw Pile corpus text | Same as above |
| Months of year | Mistral-7B (layer 8) | SAE → cluster reconstruction | Yes | None — raw Pile corpus text | Same as above |
| Days of week | Mistral-7B + Llama-3-8B | Intervention / probe | Yes | `"Let's do some days of the week math. {N} days from {StartDay} is"` | Activation extracted at the `<StartDay>` token position; model predicts next token (the answer day) |
| Months of year | Mistral-7B + Llama-3-8B | Intervention / probe | Yes | `"Let's do some calendar math. {N} months from {StartMonth} is"` | Activation extracted at the `<StartMonth>` token position; model predicts next token (the answer month) |
| Colours ("dark blue") | text-embedding-3-large | OpenAI API → geometric analysis | **No** | `"The color of the object is {color}. What color is the object?"` | Full sentence sent to OpenAI API; returned embedding vector used directly |
| Dates ("1st January") | text-embedding-3-large | OpenAI API → geometric analysis | **No** | `"{d}{suffix} {month}"` (bare date string, no template) | Date string sent to OpenAI API; returned embedding vector used directly |

---

## Key Observations

### The SAE pipeline used no prompts
The SAE pipeline (`generate_feature_occurence_data.py`) did not use structured prompts at all. It ran the model over the raw [Pile corpus](https://pile.eleuther.ai/) and recorded activations at every position where a token of interest naturally occurred in the text. There was no controlled context — the same token ("Monday", "1987", "January") was captured across thousands of different naturally occurring sentences.

### The intervention pipeline used arithmetic prompts
The intervention experiments used a different approach: structured arithmetic-style prompts that make the target token causally important to the model's prediction:

- Days: `"Let's do some days of the week math. {N} days from {StartDay} is"`
- Months: `"Let's do some calendar math. {N} months from {StartMonth} is"`

Activations were extracted at the `<StartDay>` or `<StartMonth>` token position, and the model was evaluated on whether it correctly predicted the answer token. This ensures the model is actively using the concept's representation, not just passively encoding it.

### Multi-token concepts bypassed the SAE pipeline entirely
Neither paper used multi-token terms in the SAE or intervention pipelines. The two concept sets that contain multi-token names — colours ("dark blue") and dates ("1st January") — were handled via a completely separate pipeline using `text-embedding-3-large` from the OpenAI API. The embedding vector returned by the API was used directly as the concept representation, skipping TransformerLens and SAELens entirely.

### Two activation regimes, same result
The SAE pipeline (organic corpus occurrences, no prompt) and the intervention pipeline (arithmetic prompts, causally active token) are fundamentally different activation regimes — yet both produced circular/manifold geometry for the same concepts.[^1][^2] This suggests the geometric structure is a robust property of how the model represents these concepts, not an artefact of a particular prompting strategy.

---

## Implication for Medical Concept Analysis

The existing `text-embedding-3-large` database of SNOMED CT concepts maps directly onto the colours/dates pipeline — the embedding vectors can be fed straight into the geometric analysis (normalise → PCA → k-NN → Dijkstra → Chatterjee correlation) without any LLM forward passes.

An open question is whether arithmetic-style prompts analogous to the intervention pipeline (e.g. `"The parent disorder of {concept} is"`) and running through the SAE pipeline would yield richer or different geometry compared to the text embedding approach — and whether the two can be directly compared on the same concept set.

---

[^1]: J. Engels, I. Liao, E. J. Michaud, W. Gurnee, and M. Tegmark, "Not All Language Model Features Are Linear," in *Proc. ICLR*, 2025. [[2405_14860_not-all-lm-features-are-linear|↗]]
[^2]: A. Modell et al., "The Origins of Representation Manifolds in Large Language Models," arXiv:2505.18235, 2025. [[2505_18235_the-origins-of-representation-manifolds-in-large-language-models|↗]]
