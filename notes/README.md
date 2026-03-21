# Notes

Start at [[goal]] for the project goal.

## Structure

```
notes/
├── goal.md              # project goal and approach
├── plans/               # planning documents
├── experiments/         # one file per completed/running experiment
├── reference/           # stable lookup tables
├── exploration/         # conceptualizing different plans
├── understanding/       # conceptual notes on theory
│   └── sae/             # SAE-specific understanding notes
└── papers/              # per-paper annotation notes
```

## Folders

**`plans/`** — forward-looking documents: current experiment plan, long-term pipeline, archived drafts.

**`experiments/`** — one file per experiment run. Created when notebook 3 produces its first results. See template below.

**`reference/`** — stable lookup tables (model candidates, SNOMED hierarchy counts, implementation notes). Consult but rarely edit.

**`understanding/`** — conceptual notes on theory: SAEs, tokenisation, layer geometry, prompting strategies, the Pile corpus. The `sae/` subfolder groups SAE-specific notes. Split further if the folder exceeds ~25 files.

**`exploration/`** — notes on exploring and synthesising on combining different papers and understanding into ideas. Selected a subset of notes will produce plans.

**`papers/`** — one note per paper, named by arXiv ID. See [[papers/REFERENCES]] for the full index.

---

## Experiment File Template

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
