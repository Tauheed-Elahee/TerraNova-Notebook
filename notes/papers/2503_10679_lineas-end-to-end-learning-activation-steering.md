---
title: "LinEAS: End-to-end Learning of Activation Steering with a Distributional Loss"
id: 2503.10679
author: Rodriguez, Klein, Gualdoni, Maiorca, Blaas, Zappella, Cuturi, Suau
publish_date: 2025-03
url: https://arxiv.org/abs/2503.10679
repo: https://github.com/apple/ml-lineas
summary: Global loss accounting for layer-wise distributional shifts during activation steering; shows middle layers are crucial for steering without causing unintended downstream shifts.
---

# LinEAS: End-to-end Learning of Activation Steering with a Distributional Loss

**arXiv:** 2503.10679 | Rodriguez, Klein, Gualdoni et al., 2025

## Summary

Proposes learning activation steering vectors end-to-end using a distributional loss that penalises unintended shifts in the output distribution. Finds that middle layers are the optimal intervention site: steering there achieves the target change with minimal collateral distribution shift.

## Key Contributions

- Introduces a distributional loss for training steering vectors that penalises unintended side effects.
- Shows middle layers are the optimal intervention depth — early layers cause too much collateral shift, late layers have insufficient effect.
- Provides a principled framework for identifying the layer depth where a concept is most cleanly encoded.
- Demonstrates that layer-wise distributional shift is a useful diagnostic for steering quality.

## Relevance to This Project

The distributional shift metric could serve as a principled criterion for selecting the extraction/injection layers in the TerraNova pipeline. The finding that middle layers minimise collateral shift aligns with the semantic core hypothesis that middle layers encode concepts most cleanly.
