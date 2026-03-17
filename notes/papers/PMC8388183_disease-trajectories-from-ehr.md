---
title: A Computational Method for Learning Disease Trajectories from Partially Observable EHR Data
id: PMC8388183
author: Oh, Steinbach, Castro, Peterson, Kumar, Caraballo, Simon
publish_date: 2021-07-27
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC8388183/
doi: 10.1109/JBHI.2021.3089441
journal: IEEE Journal of Biomedical and Health Informatics
summary: Extracts and filters disease trajectories from EHR data using association and temporal ordering criteria plus a likelihood function for progression risk. Validated on Mayo Clinic (53K patients) and M Health Fairview (59K patients); 10-20 filtered trajectories explain outcomes as well as the full set of 5,000.
---

# A Computational Method for Learning Disease Trajectories from Partially Observable EHR Data

**PMC:** 8388183 | IEEE JBHI 2021 | DOI: 10.1109/JBHI.2021.3089441

## Summary

Proposes a three-component pipeline for learning disease trajectories from EHR: (1) trajectory extraction algorithm, (2) filtering using disease association and temporal ordering criteria, and (3) a likelihood function scoring progression risk. Tested on Type 2 Diabetes complication progressions. Filtering achieves 80-100× reduction in trajectory count with only ~5% relative loss in explanatory power; 10-20 trajectories suffice to match the full 5,000-trajectory set.

## Key Contributions

- Extraction algorithm for disease trajectories from partially observable, longitudinal EHR data.
- Filtering criteria combining disease co-occurrence associations and temporal ordering to prune implausible trajectories.
- Likelihood function to score and rank progression risk along a trajectory.
- Outperforms causal inference and generative model baselines on explaining observed progressions.
- Validated on two independent large cohorts (Mayo Clinic and M Health Fairview).
- Clinically plausible T2D complication patterns recovered without manual curation.

## Relevance to This Project

Disease trajectories are sequences of clinical events ordered over time — a temporal extension of the static concept relationships encoded in SNOMED CT. The filtering criteria (association + temporal order) are analogous to using ontological parent-child and causal relationships to constrain concept graph traversal. The likelihood scoring function provides a template for how geometric proximity in concept embedding space could translate into a probabilistic progression model. The partial observability framing is important: EHR data is sparse and the method accounts for concepts being present but unobserved, which mirrors the challenge of grounding LLM representations to specific ontology nodes.
