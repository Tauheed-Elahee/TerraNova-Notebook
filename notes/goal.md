# Project Goal

Find geometric structures within language model representations for medical concepts that have SNOMED CT concept codes — analogous to the circular manifolds found by Engels et al. for days of the week, months of the year, and years of the 20th century.

## Approach

Apply the Engels et al. pipeline (TransformerLens + SAELens) to medical concept tokens:

1. Choose a set of SNOMED CT concepts (e.g. all disorders of the respiratory system)
2. Generate prompts containing those concept names/descriptions
3. Extract activations layer-by-layer via TransformerLens
4. Train SAEs via SAELens on those activations
5. Run cosine similarity clustering and irreducibility scoring
6. Compare discovered geometry against SNOMED CT ontological relationships

## Why SNOMED CT Is a Good Anchor

SNOMED CT provides a ground-truth ontology against which discovered geometry can be validated:

- **Hierarchies** (is-a relationships) — does severity (mild → moderate → severe) form a linear or circular manifold?
- **Body system groupings** — do cardiovascular concepts cluster differently from respiratory ones?
- **Clinical relationships** (finding-site, associated-morphology, causative-agent) — do these encode as geometric relationships between concept vectors?

## Intended Model: GPT-OSS-20B

`openai/gpt-oss-20b` — Apache 2.0, released August 2025.

### Key Architecture Facts

| Property | Detail |
|---|---|
| Total parameters | 21B |
| Active parameters per token | 3.6B |
| Architecture | **Mixture of Experts (MoE)** |
| Quantization | MXFP4 |
| VRAM requirement | ~16GB |
| TransformerLens support | **No** |

### MoE Implications for the Pipeline

- The residual stream still exists and can be analysed layer by layer
- MLP layers are replaced by a router + N expert subnetworks; only a subset activate per token
- TransformerLens does not support the `gpt_oss` architecture — activation extraction requires manual `forward_hooks` on the raw HuggingFace model
- SAE training on MoE models is more complex: different tokens route through different experts, potentially making residual stream geometry noisier

### Alternative Models (if TransformerLens support is preferred)

| Model | MoE? | TransformerLens | Medical pretraining |
|---|---|---|---|
| GPT-OSS-20B | Yes (3.6B active) | No | No |
| Mistral-7B | No | Yes | No |
| BioMedLM (2.7B) | No | Likely yes | Yes |
| Llama-3 8B | No | Yes | No |
| Med42 (70B) | No | Partial | Yes |

---

## Existing Asset: text-embedding-3-large Database

A database of `text-embedding-3-large` embeddings already exists for all medical SNOMED CT concepts.

### Two Separate Embedding Systems

```
text-embedding-3-large
  "Asthma" → [3072-dim vector]   ← semantic embedding, already computed

LLM (e.g. Llama-3-8B)
  "Asthma" → token ID → [4096-dim lookup vector]   ← token embedding, layer 0
            → layer 1 residual stream [4096-dim]
            → layer 2 residual stream [4096-dim]
            → ...
            → layer 32 residual stream [4096-dim]   ← final representation
```

No LLM uses `text-embedding-3-large` as its token embedding — they each have their own learned lookup table. They are different spaces with different dimensions.

### Role of the text-embedding-3-large Database

The existing embeddings serve as the **ground truth semantic map** — analogous to how the Representation-Manifolds paper uses them to verify that manifold geometry in the LLM matches geometry in pure semantic space.

### Full Analysis Pipeline

```
text-embedding-3-large embeddings   ← already computed
        ↓ compare geometry
LLM token embedding layer (layer 0) ← how does the LLM initially encode the concept?
        ↓
Layer 1 residual stream             ← how does structure evolve?
        ↓
Layer 2 residual stream
        ↓
...
        ↓
Layer N residual stream             ← what structure has emerged by the end?
```

At each layer: run PCA, build k-NN graph, compute geodesic distances, compare to SNOMED CT hierarchy distances — exactly what the Representation-Manifolds paper does for dates/months/colours.

### Key Research Question

Does the geometric structure of medical concepts in the LLM's residual stream **converge toward** or **diverge from** the `text-embedding-3-large` structure as depth increases? And does either align with the SNOMED CT ontological distances?

This is a stronger experiment than Engels et al. because SNOMED CT provides a pre-existing structured ground truth, rather than having to infer expected geometry from first principles.
