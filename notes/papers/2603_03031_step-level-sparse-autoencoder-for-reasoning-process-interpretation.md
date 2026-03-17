---
title: Step-Level Sparse Autoencoder for Reasoning Process Interpretation
id: 2603.03031
author: Yang, Liu, Lai, Xu, Huang, Miao
publish_date: 2026-03-03
url: https://arxiv.org/abs/2603.03031
summary: A step-level sparse autoencoder (SSAE) that interprets LLM reasoning by decomposing reasoning steps into sparsely activated dimensions, predicting correctness and logicality of reasoning steps and suggesting LLMs have implicit self-verification knowledge.
---

# Step-Level Sparse Autoencoder for Reasoning Process Interpretation

**arXiv:** 2603.03031 | 2026

## Summary

Proposes SSAE (Step-Level Sparse Autoencoder), which operates at the reasoning-step level rather than the token level. Uses an information bottleneck to separate critical from background information, decomposing representations into sparsely activated dimensions. Demonstrates prediction of both surface metrics (generation length, token distribution) and complex reasoning properties (step correctness and logicality).

## Key Contributions

- Step-level (rather than token-level) SAE that captures reasoning transitions and semantic shifts.
- Information bottleneck separates task-critical signal from background context.
- Sparse decomposition of reasoning steps allows interpretable feature identification.
- Models predict correctness and logicality of intermediate reasoning steps.
- Results suggest LLMs carry implicit knowledge about their own reasoning quality during generation.

## Relevance to This Project

Sparse autoencoders operating at a coarser (step/concept) level rather than the token level may be directly applicable to extracting medical concept representations. The finding that LLMs encode quality signals in their internal states echoes the hypothesis that SNOMED hierarchical structure is implicitly encoded in LLM geometry. The information bottleneck framing could inspire a method to isolate the "clinical meaning" component of a medical concept representation from surface form.
