---
title: "Faithful Bi-Directional Model Steering via Distribution Matching and Distributed Interchange Interventions"
id: 2602.05234
author: Bao, Zhang, Chen, Su, Cai, Peng, Sun, Weng, Yan, Yin
publish_date: 2026-02
url: https://arxiv.org/abs/2602.05234
repo: https://github.com/colored-dye/concept_das
summary: Proposes CDAS using distributed alignment search; reveals middle layers encode faithful causal variables — the most causally interpretable representations in the network.
---

# Faithful Bi-Directional Model Steering via Distribution Matching and Distributed Interchange Interventions

**arXiv:** 2602.05234 | Bao, Zhang, Chen et al., 2026

## Summary

Introduces Causal Distributed Alignment Search (CDAS), a method for finding distributed representations in transformer middle layers that faithfully encode causal variables. Shows that bi-directional steering (both toward and away from a concept) is achievable through middle-layer distributed interventions.

## Key Contributions

- CDAS identifies distributed middle-layer subspaces that causally encode specific concepts.
- Demonstrates bi-directional (amplify/suppress) concept steering via these subspaces.
- Shows middle layers contain the most causally interpretable representations — earlier layers are too local, later layers too entangled with output distribution.
- Provides evidence that concepts are distributed across multiple dimensions in middle layers rather than localised to single neurons.

## Relevance to This Project

The CDAS framework for finding causally faithful concept subspaces in middle layers is directly applicable to verifying whether SNOMED CT concept geometry in TerraNova corresponds to causally meaningful representations, or is merely a correlational artefact.
