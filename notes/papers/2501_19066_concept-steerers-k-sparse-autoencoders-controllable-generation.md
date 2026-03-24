---
title: "Concept Steerers: Leveraging K-Sparse Autoencoders for Controllable Generations"
id: 2501.19066
author: Kim, Ghadiyaram
publish_date: 2025-01
url: https://arxiv.org/abs/2501.19066
repo: https://github.com/kim-dahye/steerers
summary: K-SAEs identify monosemantic concepts in embedding space; enables precise steering toward/away from semantic concepts without retraining by activating or suppressing specific SAE features.
---

# Concept Steerers: Leveraging K-Sparse Autoencoders for Controllable Generations

**arXiv:** 2501.19066 | Kim, Ghadiyaram, 2025

## Summary

Uses K-Sparse Autoencoders (K-SAEs, where exactly k features are active per input) to identify monosemantic concept features in transformer hidden states. By activating or suppressing specific SAE features at inference time, enables controllable generation toward or away from target concepts without any fine-tuning.

## Key Contributions

- K-SAE constraint (exactly k active features) produces more consistently monosemantic features than standard L1-penalised SAEs.
- Identifies concept-specific features that can be directly manipulated for generation control.
- Demonstrates that SAE features function as semantic primitives: steering in feature space steers in concept space.
- Provides a practical framework for concept-level control of LLM generation.

## Relevance to This Project

The concept-steerer framework is directly applicable to the injection phase of the TerraNova pipeline: if K-SAE features correspond to SNOMED concepts, steering via those features at middle layers would constitute a concept-injection mechanism. Also motivates using K-SAEs rather than standard SAEs for training on the medical LLM's residual stream.
