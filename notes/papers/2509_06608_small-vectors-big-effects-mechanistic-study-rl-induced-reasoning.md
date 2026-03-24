---
title: "Small Vectors, Big Effects: A Mechanistic Study of RL-Induced Reasoning via Steering Vectors"
id: 2509.06608
author: Sinii, Balagansky, Gerasimov, Laptev, Aksenov, Kurochkin, Gorbatovski, Shaposhnikov, Gavrilov
publish_date: 2025-09
url: https://arxiv.org/abs/2509.06608
repo: https://github.com/corl-team/steering-reasoning
summary: Detailed mechanistic analysis of steering vectors at different layers; shows middle layers de-emphasise non-English tokens and operate through MLP rather than attention, with small vectors producing large behavioural effects.
---

# Small Vectors, Big Effects: A Mechanistic Study of RL-Induced Reasoning via Steering Vectors

**arXiv:** 2509.06608 | Sinii, Balagansky, Gerasimov et al., 2025

## Summary

Provides a mechanistic analysis of how steering vectors applied at different transformer layers affect model behaviour, focusing on models trained with reinforcement learning. Finds that middle layers are the most effective intervention site, with MLP components carrying more steerable semantic content than attention components.

## Key Contributions

- Shows middle layers are the most efficient site for steering vector intervention — small vectors cause large behavioural changes.
- Identifies MLP blocks (not attention) as the primary carrier of steerable semantic content in middle layers.
- Shows RL training concentrates reasoning-relevant features in middle-layer MLPs.
- Demonstrates that de-emphasising non-English tokens in middle layers is a mechanism for multilingual concept alignment.

## Relevance to This Project

Supports the semantic core framing: if steering is most effective in middle layers, these layers encode the most malleable and semantically concentrated representations. The MLP-focus finding suggests that SAEs trained on MLP outputs in middle layers will capture the most semantically structured features relevant to SNOMED concept geometry.
