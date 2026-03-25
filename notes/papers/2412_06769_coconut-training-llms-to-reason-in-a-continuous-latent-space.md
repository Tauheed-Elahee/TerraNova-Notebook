---
title: "Coconut: Training Large Language Models to Reason in a Continuous Latent Space"
id: 2412.06769
author: Hao, Sukhbaatar, Su, Li, Hu, Weston, Tian
publish_date: 2024-12
url: https://arxiv.org/abs/2412.06769
repo: https://github.com/facebookresearch/coconut
summary: LLMs can reason in continuous latent space by feeding each forward pass's last hidden state directly as the next input embedding, bypassing tokenization and enabling BFS-like multi-path reasoning outperforming discrete chain-of-thought.
---

# Coconut: Training Large Language Models to Reason in a Continuous Latent Space

**arXiv:** 2412.06769 | December 2024 | Hao, Sukhbaatar, Su, Li, Hu, Weston, Tian (Meta FAIR)

## Summary

Introduces Chain of Continuous Thought (Coconut): the model's last hidden state after each forward pass is fed directly back as the embedding of the next "token," bypassing vocabulary projection and re-tokenization entirely. The model reasons in a continuous latent space where each thought step is a high-dimensional vector rather than a discrete word.

## Key Contributions

- Continuous latent "thoughts" can encode multiple branching reasoning paths simultaneously (BFS-like), which discrete token CoT cannot.
- Trained by gradually replacing discrete reasoning chain tokens with continuous latent steps.
- Achieves better performance than chain-of-thought on logical reasoning benchmarks with fewer decoding steps.
- Provides the purest implementation of the "hidden state as next input" paradigm.

## Relevance to This Project

Demonstrates that feeding a model's own intermediate hidden states as inputs is not only feasible but can improve reasoning. Establishes the technical pattern: `last_hidden_state[t] → input_embedding[t+1]`. For this project, the analogous idea is: extract mid-layer hidden states of medical concept names and inject them as direct inputs to the upper layers, bypassing the lower detokenization processing for concepts already known to the system.
