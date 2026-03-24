---
title: "ASA: Training-Free Representation Engineering for Tool-Calling Agents"
id: 2602.04935
author: Wang, Zhou, Fu, Cao, Zeng, Lu, Fan, Zhao, Pan
publish_date: 2026-02
url: https://arxiv.org/abs/2602.04935
summary: Identifies failure modes decodable from mid-layer activations; proposes router-conditioned steering at middle layers for tool-calling agent reliability.
---

# ASA: Training-Free Representation Engineering for Tool-Calling Agents

**arXiv:** 2602.04935 | Wang, Zhou, Fu et al., 2026

## Summary

Applies representation engineering to improve tool-calling reliability in LLM agents. Finds that failure modes (incorrect tool selection, malformed calls) are detectable from middle-layer activations before generation occurs, and proposes training-free steering interventions at those layers.

## Key Contributions

- Demonstrates that middle-layer activations encode agent intent and failure modes before they manifest in output tokens.
- Proposes a router-conditioned steering approach: detect failure mode from mid-layer probe, apply corrective steering vector.
- Requires no fine-tuning — purely inference-time intervention.
- Provides evidence that middle layers carry actionable decision state for agent behaviour.

## Relevance to This Project

Shows that middle layers encode semantic intent (tool choice, action planning) in a form that can be read and manipulated. For TerraNova, this supports the interpretation that middle-layer geometry encodes higher-level conceptual states rather than surface-level token statistics.
