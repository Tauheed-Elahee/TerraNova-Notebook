# Tuned Lens Options for Part 2b/2c

This note summarizes the issue seen in `Azure/run-22/log/stage1-baseline-geometry/1-layer-calibration.log` and the practical options for fixing or validating Part 2b and Part 2c in `src/stage1-baseline-geometry/1-layer-calibration.ipynb`.

## Current Issue

Part 2b makes Tuned Lens the canonical source for `L_pred`. In run-22, the Tuned Lens path completed, but the downstream stratification cell failed:

```text
AssertionError: _mr_stable[-1] = 0.6612021857923497
```

The relevant Part 2b result was:

```text
Tuned Lens threshold boundary: 31  (first layer >=80%: 0.621)
Per-concept tuned-lens L_pred distribution (n_stable=366, n_never_stable=24 = 6.2%)
```

So layer 31 was not a true threshold hit. It was a last-layer fallback. Among concepts that matched the final prediction at any layer, only about 66.1% still matched at the last probed layer. The later assertion assumed that "stable at any layer" implies "stable at the final layer", which does not hold for the current Tuned Lens computation.

There is also an important warning:

```text
The unembedding matrix hash does not match the lens' hash.
```

That warning does not prove the wrong Llama model was used, but it means the lens/model pairing is not perfectly verified.

## Residual Stream Hooks

TransformerLens exposes several snapshots inside each transformer block:

```text
resid_pre[L]
    |
    | normalize
    v
Attention
    |
    | add attention update
    v
resid_mid[L]
    |
    | normalize
    v
MLP
    |
    | add MLP update
    v
resid_post[L]
```

In equations:

```python
x = resid_pre[L]

attn_out = attention(norm1(x))
resid_mid[L] = x + attn_out

mlp_out = mlp(norm2(resid_mid[L]))
resid_post[L] = resid_mid[L] + mlp_out
```

Across layers:

```text
embedding output
      |
      v
resid_pre[0]
      |
   Block 0
      |
      v
resid_post[0] ~= resid_pre[1]
      |
   Block 1
      |
      v
resid_post[1] ~= resid_pre[2]
      |
     ...
      |
   Block 31
      |
      v
resid_post[31]
      |
 final norm + unembed
      |
 next-token logits
```

For token persistence or erasure, using `hook_resid_post` can be a reasonable "after each block" measurement. For Tuned Lens, the official convention is different.

## Official Tuned Lens Convention

Official Tuned Lens training/evaluation uses Hugging Face hidden states:

```python
output = model(..., output_hidden_states=True)
hidden_states = output.hidden_states[:-1]
```

For a 32-layer Llama model, this means:

```text
H0 -- Block 0 --> H1 -- Block 1 --> H2 ... H31 -- Block 31 --> H32
|                |                |       |
lens 0           lens 1           lens 2  lens 31

Tuned Lens uses H0..H31.
It does not use H32 as a translator input.
```

In TransformerLens terms, this maps most closely to:

```text
cache["resid_pre", L]
```

not:

```text
cache["resid_post", L]
```

The current notebook feeds `hook_resid_post[L]` into translator `L`, which is effectively one block later than the official convention.

Sources:

- Tuned Lens training loop uses `output.hidden_states[:-1]`: <https://github.com/AlignmentResearch/tuned-lens/blob/main/tuned_lens/scripts/train_loop.py#L398-L404>
- Tuned Lens eval loop uses `output.hidden_states[:-1]`: <https://github.com/AlignmentResearch/tuned-lens/blob/main/tuned_lens/scripts/eval_loop.py#L262-L268>
- Tuned Lens TransformerLens adapter defaults to `residual_component="resid_pre"` and feeds `cache[residual_component, layer]` to `lens.forward`: <https://github.com/AlignmentResearch/tuned-lens/blob/main/tuned_lens/plotting/prediction_trajectory.py#L185-L223>
- Hugging Face documents `hidden_states` as embeddings plus layer outputs: <https://huggingface.co/docs/transformers/main_classes/output>

## Hugging Face Pass

A real Hugging Face pass means running the native `transformers` model directly:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

tok = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")
hf_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Meta-Llama-3-8B",
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
hf_model.eval()

inputs = tok(" bronchitis", return_tensors="pt").to(hf_model.device)

with torch.no_grad():
    outputs = hf_model(
        **inputs,
        output_hidden_states=True,
        return_dict=True,
    )

stream = outputs.hidden_states[:-1]
for layer, h in enumerate(stream):
    logits = tuned_lens.forward(h, layer)
```

This exactly matches the activation API used by official Tuned Lens code. The existing notebook model is:

```python
model = HookedTransformer.from_pretrained("meta-llama/Meta-Llama-3-8B")
```

So the checkpoint ID is the same, but the Python model object and activation API are different:

```text
HF model:
  AutoModelForCausalLM.from_pretrained("meta-llama/Meta-Llama-3-8B")
  exposes output.hidden_states

TransformerLens model:
  HookedTransformer.from_pretrained("meta-llama/Meta-Llama-3-8B")
  exposes hook_resid_pre, hook_resid_mid, hook_resid_post
```

The issue is likely not "wrong Llama model"; it is "same checkpoint ID, different activation indexing convention." The unembedding hash warning should still be investigated or at least reported.

## Option Comparison

| Approach | What It Means | Pros | Cons | Best Use |
|---|---|---|---|---|
| Keep `HookedTransformer` + use `hook_resid_post` | Current approach: feed "after block L" states into Tuned Lens translator `L` | Reuses existing cached activations; matches the notebook's "after each block" token-erasure framing; minimal compute | Misaligned with official Tuned Lens convention; translator `L` likely receives a state one block too late; makes `L_pred` unreliable; caused downstream assumption failure | Fine for token persistence / erasure probes, not ideal for Tuned Lens |
| Keep `HookedTransformer` + switch Tuned Lens to `hook_resid_pre` | Use "before block L" states for Tuned Lens translator `L` | Closest TransformerLens equivalent to official Tuned Lens convention; keeps interpretability tooling; cheaper than loading a second HF model | Requires recomputing/cache invalidation for Part 2b/2c; still depends on TL-to-HF equivalence; unembedding hash warning may remain | Best practical fix for this notebook |
| Use real HF `AutoModelForCausalLM` + `output_hidden_states=True` | Run the original Hugging Face model and feed `outputs.hidden_states[:-1]` into Tuned Lens | Exact match to official Tuned Lens training/eval convention; avoids TL hook-mapping ambiguity; best way to validate whether `hook_resid_pre` matches | More memory/compute; may require loading a second 8B model or refactoring model path; less convenient for existing TL probe code | Best validation/reference path |
| Use Logit Lens only | Drop Tuned Lens as canonical and use direct `ln_final + unembed` on TL residuals | Simple, transparent, uses existing activations; no external lens artifact/hash mismatch | Known basis mismatch; can make `L_pred` look artificially late; loses intended tuned-lens correction | Good baseline, not best canonical prediction-stabilization estimate |
| Keep Tuned Lens but treat it as diagnostic only | Do not let Tuned Lens overwrite canonical `layer_preds` / `L_pred`; report it separately | Avoids pipeline breakage; keeps all plots; no immediate redesign | Dodges the core question of canonical `L_pred`; leaves notebook conclusions less decisive | Good temporary fallback while debugging |
| Load HF model only for Part 2b/2c | Keep TL for token persistence, use HF hidden states just for Tuned Lens | Preserves existing notebook design; gives official-convention Tuned Lens for `L_pred`; isolates risk to prediction-stabilization section | Adds complexity and memory pressure; must ensure tokenization/order exactly matches cached concept set | Most rigorous long-term design if resources allow |

## HF Resource Feasibility

Part 2b/2c prompt volume is small:

```text
Part 2b: 390 multi-token prompts, max about 5 tokens including BOS
Part 2c: 701 single-token prompts, 2 tokens including BOS
Total:   1,091 prompts
```

The current run loaded `HookedTransformer` in `float32` and used about 34.55 GB of GPU memory. A Hugging Face fp32 Llama-3-8B load will be in the same rough range. The hidden states are not the main memory cost if batches are kept small; model weights are.

| Scenario | GPU Requirement | CPU RAM | Pros | Cons |
|---|---:|---:|---|---|
| HF model loaded alongside current fp32 `HookedTransformer` | ~52-75 GB depending HF dtype | ~10-25 GB extra | Can compare TL and HF directly in one process | Likely too much for a 40 GB GPU |
| Free TL model, then load HF fp32 | ~34-40 GB | ~10-25 GB extra during/after load | Closest dtype match to current notebook | Tight on 40 GB GPU; batching must be small |
| Free TL model, load HF bf16/fp16 | ~17-22 GB | ~8-20 GB | Much easier to fit; probably practical | Slight dtype differences can change rare argmax ties |
| HF model on CPU only | 0 GPU for model | ~35-45 GB+ | Avoids GPU pressure | Very slow for 1,091 prompts |
| HF with CPU/disk offload | Variable | High | Can fit constrained GPUs | Slow and operationally fiddly |

Activation memory is modest for these prompts. For example, all Part 2b hidden states at once in fp32 are approximately:

```text
33 hidden states * 390 prompts * 5 tokens * 4096 dims * 4 bytes
~= 1.0 GB
```

Part 2c all at once is approximately 0.75 GB fp32. With small batches, hidden-state memory is only a few MB.

The more likely activation-side trap is logits:

```text
batch * seq_len * vocab_size
```

For Llama-3's roughly 128k-token vocabulary, large batches can add substantial memory. Use small batches, or `logits_to_keep=1` if the installed Transformers version supports it.

## Recommended Path

Use `hook_resid_pre` for Tuned Lens in Part 2b and Part 2c, invalidate the relevant caches, and add metadata that records the activation stream convention. Then run a small HF `output_hidden_states=True` spot-check on 10-20 prompts to confirm that TransformerLens `resid_pre[L]` gives the same or near-identical Tuned Lens predictions as HF `hidden_states[L]`.

Also fix the downstream stratification cell:

- Keep the stable/never-stable count checks.
- Remove the assertion that `_mr_stable[-1] == 1.0`.
- Replace it with a diagnostic such as "last-probed-layer match among ever-stable concepts."
- Treat "no threshold hit" explicitly as `threshold_hit=False`, `threshold_layer=None`, `fallback_layer=31`, instead of printing "threshold boundary 31" as though the 80% threshold was reached.
