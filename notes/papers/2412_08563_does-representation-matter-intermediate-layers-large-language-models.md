---
title: "Does Representation Matter? Exploring Intermediate Layers in Large Language Models"
id: 2412.08563
author: Kakkar, Mukherjee, Ragothaman, Mehta
publish_date: 2024-12
url: https://arxiv.org/abs/2412.08563
summary: Systematic evaluation of representation quality across layers; identifies bimodal entropy patterns in intermediate layers correlating with semantic processing.
---

# Does Representation Matter? Exploring Intermediate Layers in Large Language Models

**arXiv:** 2412.08563 | Kakkar, Mukherjee, Ragothaman, Mehta, 2024

## Summary

Conducts a systematic evaluation of representation quality at each layer of large language models using multiple downstream benchmarks. Identifies a characteristic bimodal entropy pattern in intermediate layers that correlates with the transition from syntactic to semantic processing.

## Key Contributions

- Identifies bimodal entropy patterns at specific intermediate layers as a signature of semantic processing.
- Demonstrates layer-specific representation quality differences that vary by task type (syntactic vs. semantic).
- Provides a method for identifying semantically rich layers without task fine-tuning.
- Shows representation quality is not monotonically increasing with depth.

## Relevance to This Project

The bimodal entropy pattern could provide a model-agnostic method for identifying the boundaries of the semantic core window. For TerraNova, this offers a principled criterion for selecting which layers to extract concept representations from rather than relying on layer-fraction heuristics.
