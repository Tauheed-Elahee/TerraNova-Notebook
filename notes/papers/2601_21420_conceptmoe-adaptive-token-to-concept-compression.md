---
title: "ConceptMoE: Adaptive Token-to-Concept Compression for Implicit Compute Allocation"
id: 2601.21420
author: Huang, Zhou, Qu, Min, Zhang
publish_date: 2026-01
url: https://arxiv.org/abs/2601.21420
repo: https://github.com/ZihaoHuang-notabot/ConceptMoE
summary: Dynamic token-to-concept compression architecture using MoE routing; middle processing layers benefit from explicit concept representations with adaptive compute allocation.
---

# ConceptMoE: Adaptive Token-to-Concept Compression for Implicit Compute Allocation

**arXiv:** 2601.21420 | Huang, Zhou, Qu, Min, Zhang, 2026

## Summary

Proposes a mechanism for compressing sequences of tokens into concept-level representations using Mixture-of-Experts routing. Middle processing layers operate over concept representations, with compute dynamically allocated based on semantic complexity.

## Key Contributions

- Introduces token-to-concept compression as an explicit architectural primitive integrated into transformer training.
- Uses MoE routing to implicitly learn which token spans constitute concepts.
- Shows middle layers with explicit concept representations outperform standard attention on semantic reasoning tasks.

## Relevance to This Project

Provides architectural support for treating middle layers as operating on concept-level rather than token-level representations. The MoE routing mechanism for token-to-concept compression is analogous to the injection-side boundary in the semantic core pipeline.
