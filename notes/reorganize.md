# Notes Folder Reorganisation Plan

## Target Structure

```
notes/
│
├── goal.md                        # stays at root — anchors everything
│
├── plans/                         # all planning documents
│   ├── current.md                 # the active experiment (was plan-now.md)
│   ├── longterm.md                # GPT-2 + SAELens pipeline (was plan.md)
│   └── archive/                   # superseded drafts, kept for reference
│       └── plan-text-embedding-v1.md
│
├── experiments/                   # one file per completed/running experiment
│   ├── exp01-breast-cancer-embeddings.md   # what was done, what was found
│   ├── exp02-lung-cancer-embeddings.md
│   └── exp03-gpt2-residual-stream.md
│
├── reference/                     # stable lookup tables, no expiry
│   ├── models.md
│   ├── snomed-hierarchy-counts.md
│   └── cancer-subtype-counts.md
│
├── understanding/                 # conceptual notes on theory — no change
│   └── ...
│
└── papers/                        # per-paper annotation notes — no change
    └── ...
```

---

## File Moves

| Current | Destination |
|---|---|
| `plan-now.md` | `plans/current.md` |
| `plan.md` | `plans/longterm.md` |
| `plan-text-embedding-plot.md` | `plans/archive/plan-text-embedding-v1.md` |
| `models.md` | `reference/models.md` |
| `snomed-hierarchy-counts.md` | `reference/snomed-hierarchy-counts.md` |
| `cancer-subtype-counts.md` | `reference/cancer-subtype-counts.md` |

## Files to Delete

| File | Reason |
|---|---|
| `actions.md` | Empty |
| `plot-colorschemes.md` | Single implementation detail — inline as notebook comment |

---

## When to Create Each Folder

| Folder | Create when |
|---|---|
| `plans/` | Now |
| `reference/` | Now |
| `experiments/` | When notebook 3 produces its first results |
| `understanding/sae/` etc. | If `understanding/` exceeds ~25 files |

---

## Experiment File Template

Each file in `experiments/` should follow this structure:

```markdown
# Exp NN — <short title>

**Hierarchy:** `<< SNOMED_ID` (<name>, N concepts)
**Date:** YYYY-MM-DD

## Hypothesis
What geometric structure do we expect to find?

## Method
Which notebooks were run, with what parameters.

## Results
Key numbers: Pearson r, Chatterjee ξ, PCA variance explained.

## Interpretation
What does this tell us about how the model encodes this concept space?

## Open Questions
What to investigate next.
```
