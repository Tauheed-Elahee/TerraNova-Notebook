---
title: "From EHRs to Patient Pathways: Scalable Modeling of Longitudinal Health Trajectories with LLMs"
id: 2506.04831
author: Pellegrini, Özsoy, Bani-Harouni, Keicher, Navab
publish_date: 2025-06-05
url: https://arxiv.org/abs/2506.04831
summary: EHR2Path transforms EHR data into structured patient pathway representations using LLMs with topic-specific summary tokens that embed long-term context efficiently, enabling next time-step prediction and longitudinal simulation of vitals, labs, and length-of-stay.
---

# From EHRs to Patient Pathways: Scalable Modeling of Longitudinal Health Trajectories with LLMs

**arXiv:** 2506.04831 | 2025

## Summary

Proposes EHR2Path, a system converting EHR data into structured longitudinal patient pathway representations. Key mechanism: topic-specific summary tokens that compress long-term patient history into a compact context, improving token efficiency over text-only models while maintaining or exceeding performance. Evaluated on next time-step prediction and full longitudinal simulation tasks (vital signs, lab results, length-of-stay).

## Key Contributions

- EHR2Path pipeline: structured transformation of raw EHR into patient pathway representations.
- Topic-specific summary tokens as a compression mechanism for long-term clinical context.
- Outperforms competitive baselines on next time-step prediction and longitudinal simulation.
- Enables personalized patient trajectory simulation for forecasting clinical outcomes.

## Relevance to This Project

The topic-specific summary token mechanism is closely related to the problem of representing a medical concept (or a patient state) as a single compact vector that captures multi-event context — directly analogous to the token-to-concept aggregation problem this project investigates. EHR2Path's trajectory modeling makes explicit use of temporal ordering of clinical events, which maps onto SNOMED CT's hierarchical and associative structure as a prior. The longitudinal simulation framing also motivates geometric analysis: if patient pathways have predictable structure in representation space, that structure should reflect ontological relationships between concepts visited along the path.
