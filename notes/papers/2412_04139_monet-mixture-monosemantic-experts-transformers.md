---
title: "Monet: Mixture of Monosemantic Experts for Transformers"
id: 2412.04139
author: Park, Ahn, Kim, Kang
publish_date: 2024-12
url: https://arxiv.org/abs/2412.04139
repo: https://github.com/dmis-lab/Monet
summary: Integrates sparse dictionary learning directly into MoE training; scales to 262k experts revealing mutual exclusivity of semantic knowledge across experts.
---

# Monet: Mixture of Monosemantic Experts for Transformers

**arXiv:** 2412.04139 | Park, Ahn, Kim, Kang, 2024

## Summary

Proposes training Mixture-of-Experts transformers where each expert is constrained to be monosemantic by integrating sparse dictionary learning into the training objective. At 262k experts, finds that semantic knowledge is mutually exclusive across experts — each expert specialises in a narrow, non-overlapping concept space.

## Key Contributions

- Integrates SAE-style monosemanticity constraints directly into MoE training (not post-hoc).
- Scales to 262k experts; at this scale, semantic knowledge partitions cleanly across experts.
- Demonstrates mutual exclusivity of semantic knowledge: activating one concept suppresses competing concepts.
- Shows that monosemanticity can be a first-class architectural property rather than an analysis tool.

## Relevance to This Project

Provides indirect evidence that monosemantic features are a natural attractor for sufficiently expressive models. For TerraNova, this suggests that SAEs trained on a medical LLM should find features that partition SNOMED semantic tags cleanly — if polysemanticity is an artefact of capacity constraints that SAEs resolve.
