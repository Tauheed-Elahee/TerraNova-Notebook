---
title: "Improving Multilingual Language Models by Aligning Representations through Steering"
id: 2505.12584
author: Mahmoud, Semage, Karimpanal, Rana
publish_date: 2025-05
url: https://arxiv.org/abs/2505.12584
repo: https://github.com/antonisa/lang2vec
summary: Shows single-layer steering in middle layers effectively reshapes representation spaces; demonstrates middle layers are critical bottlenecks for semantic alignment across languages.
---

# Improving Multilingual Language Models by Aligning Representations through Steering

**arXiv:** 2505.12584 | Mahmoud, Semage, Karimpanal, Rana, 2025

## Summary

Applies representation steering at a single middle layer to align multilingual language model representations across languages. Finds that a single-layer intervention in the middle of the network is sufficient to substantially improve cross-lingual semantic alignment, suggesting middle layers are the primary site of language-agnostic concept encoding.

## Key Contributions

- Demonstrates that middle layers encode language-agnostic concepts — a single steering vector applied there aligns representations across languages.
- Shows that steering at middle layers is more effective than at early or late layers for semantic alignment.
- Provides practical evidence that middle layers are semantic bottlenecks where language-specific surface form has been stripped.

## Relevance to This Project

Directly supports the hypothesis that middle layers encode a language-agnostic (and therefore token-agnostic) concept space. For TerraNova, this implies that SNOMED CT concept geometry should be most visible in middle layers, where the representation is maximally language/surface-form-independent.
