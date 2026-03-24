---
title: "Rethinking Evaluation of Sparse Autoencoders through the Representation of Polysemous Words"
id: 2501.06254
author: Minegishi, Furuta, Iwasawa, Matsuo
publish_date: 2025-01
url: https://arxiv.org/abs/2501.06254
repo: https://github.com/gouki510/PS-Eval
summary: Shows deeper layers and attention modules distinguish polysemy, indicating semantic structure concentrates at depth; challenges shallow-layer SAE evaluation methods.
---

# Rethinking Evaluation of Sparse Autoencoders through the Representation of Polysemous Words

**arXiv:** 2501.06254 | Minegishi, Furuta, Iwasawa, Matsuo, 2025

## Summary

Examines how SAEs handle polysemous words (words with multiple distinct meanings) across different layers and module types. Finds that polysemy is resolved in deeper layers and in attention modules, suggesting that semantic structure is depth-dependent and that evaluation of SAEs should account for layer and module position.

## Key Contributions

- Shows polysemy disambiguation occurs in deeper layers — early SAEs capture surface form, deep SAEs capture semantic distinctions.
- Identifies attention modules as primary sites for polysemy resolution, with MLPs more focused on factual knowledge.
- Challenges the practice of evaluating SAEs on early-layer activations for semantic interpretability.
- Proposes evaluation protocols that account for the layer-dependent nature of semantic representation.

## Relevance to This Project

For TerraNova, SNOMED concepts have specific senses (e.g., "breast" as anatomy vs. "breast" in a disorder context). This paper suggests that SAEs on deeper layers will better separate these senses, and that attention-module SAEs may be particularly important for capturing context-sensitive semantic distinctions in medical text.
