---
title: "Jump to Conclusions: Short-Cutting Transformers With Linear Transformations"
id: 2303.09435
author: Yom Din, Karidi, Choshen, Geva
publish_date: 2023-03
url: https://arxiv.org/abs/2303.09435
repo: https://github.com/sashayd/mat
summary: Shows intermediate transformer layers already predict the final output via linear transformations; proposes bypass shortcuts. Independently discovers something close to the Tuned Lens finding and directly supports the output-side semantic core boundary.
---

# Jump to Conclusions: Short-Cutting Transformers With Linear Transformations

**arXiv:** 2303.09435 | Yom Din, Karidi, Choshen, Geva, 2023

## Summary

Demonstrates that a simple learned linear transformation applied to a middle-layer hidden state can recover the final-layer output with high fidelity. Uses this to propose bypass shortcuts that skip remaining layers, reducing inference compute without significant accuracy loss.

## Key Contributions

- Shows that intermediate hidden states are already close to the final output in a linear sense from around the middle layers onwards.
- Proposes layer-skipping shortcuts via linear maps, offering a practical inference speedup.
- Independently converges on the Tuned Lens finding: predictions stabilise well before the last layer.
- Provides a concrete lower bound on when the output-side semantic boundary occurs.

## Relevance to This Project

Directly supports the output-side boundary of the semantic core window. If a linear map from layer ~L to the final output is sufficient, then layers beyond L are doing refinement (re-tokenization) rather than conceptual reasoning. This is the output-side counterpart to the Tokens2Words detokenization boundary on the input side.
