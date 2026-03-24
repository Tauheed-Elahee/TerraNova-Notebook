---
title: Papers on Semantic Core Architectures — Literature Survey
tags: [semantic-core, architecture, concept-space, middle-layers, injection, steering, large-concept-models]
summary: Survey of papers that have explicitly proposed or studied semantic core architectures, middle-layer concept spaces, or related ideas in transformers. None combine the two-boundary framing (detokenisation completion + prediction stabilisation) as a bracketed semantic core window — that synthesis appears novel.
---

# Papers on Semantic Core Architectures

## Key Gap vs. Combined Architecture Document

None of these papers combine the *two boundaries* (detokenisation completion + prediction stabilisation) to define a bracketed semantic core window as an explicit architectural primitive. The Large Concept Models line is the closest architectural family, but it externalises the concept space rather than discovering it as a layer range within a standard transformer. The framing in `combined-architecture-semantic-core-pipeline.md` appears to be a novel synthesis.

---

## Closest to Explicitly Proposing a Concept Space Architecture

**2412.08821 — Large Concept Models: Language Modeling in a Sentence Representation Space** (Meta Research, 2024)
Proposes operating transformers *entirely* in sentence-embedding space (SONAR) as a higher-level abstraction over tokens. The concept space is explicit and external, not a discovered middle-layer window.

**2508.05305 — SONAR-LLM: Autoregressive Transformer that Thinks in Sentence Embeddings and Speaks in Tokens** (2025)
Hybrid architecture — processes in continuous embedding space at the concept level, generates tokens only at output. Closest architectural analogue to the semantic core pipeline: input and output remain token-level, but internal processing is at concept level.

**2512.24617 — Dynamic Large Concept Models: Latent Reasoning in an Adaptive Semantic Space** (2025)
Extension of LCMs with hierarchical, adaptive concept merging. Tokens dynamically compress into concept representations mid-network with MoE-style compute allocation.

**2601.21420 — ConceptMoE: Adaptive Token-to-Concept Compression for Implicit Compute Allocation** (2026)
Dynamic token-to-concept compression architecture using MoE; middle processing layers benefit from explicit concept representations.

---

## Middle-Layer Completion / Early Semantic Stabilisation

**2303.09435 — Jump to Conclusions: Short-Cutting Transformers With Linear Transformations** (2023)
Shows intermediate layers already predict the final output via linear transformations — independently discovering something close to the Tuned Lens finding, and using it to propose bypass shortcuts. Directly relevant to the output-side boundary.

**2502.02013 — Layer by Layer: Uncovering Hidden Representations in Language Models** (2025)
Comprehensive analysis showing mid-depth embeddings often exceed last-layer performance on semantic tasks; proposes information-theoretic metrics for representation quality across layers.

**2412.08563 — Does Representation Matter? Exploring Intermediate Layers in Large Language Models** (2024)
Systematic evaluation of representation quality across layers; identifies bimodal entropy patterns in intermediate layers correlating with semantic processing.

---

## Mechanistic / Injection-Side

**2507.04886 — Emergent Semantics Beyond Token Embeddings: Transformer LMs with Frozen Visual Unicode Representations** (2025)
Shows high-level semantics emerge from middle transformer layers *independent* of what input embeddings encode — supporting the injection framing. Semantic representation is not in the input layer but emerges in middle processing.

**2510.04861 — Uncovering Hidden Geometry in Transformers via Disentangling Position and Context** (2023)
Decomposes hidden states into position, context, and residual components; reveals low-dimensional geometry of positional embeddings across layers with orthogonal semantic structure.

---

## Middle-Layer Steering & Intervention

**2509.06608 — Small Vectors, Big Effects: A Mechanistic Study of RL-Induced Reasoning via Steering Vectors** (2025)
Detailed mechanistic analysis of steering vectors at different layers; shows middle layers de-emphasise non-English tokens and operate through MLP rather than attention.

**2505.12584 — Improving Multilingual Language Models by Aligning Representations through Steering** (2025)
Shows single-layer steering in middle layers effectively reshapes representation spaces; demonstrates middle layers are critical bottlenecks for semantic alignment.

**2602.04428 — Fine-Grained Activation Steering: Steering Less, Achieving More** (2026)
Decomposes block-level activations into atomic units; shows middle layers contain heterogeneous features that can be precisely manipulated at sub-neuron granularity.

**2602.04935 — ASA: Training-Free Representation Engineering for Tool-Calling Agents** (2026)
Identifies failure modes decodable from mid-layer activations; proposes router-conditioned steering at middle layers.

**2503.10679 — LinEAS: End-to-end Learning of Activation Steering with a Distributional Loss** (2025)
Global loss accounting for layer-wise distributional shifts; middle layers shown crucial for steering without downstream unintended shifts.

**2602.05234 — Faithful Bi-Directional Model Steering via Distribution Matching and Distributed Interchange Interventions** (2026)
Proposes CDAS using distributed alignment search; reveals middle layers encode faithful causal variables.

---

## Sparse Autoencoders & Monosemantic Features

**2309.08600 — Sparse Autoencoders Find Highly Interpretable Features in Language Models** (2023)
Foundational SAE work showing sparse features extracted from middle layers are more monosemantic than neurons.

**2506.19382 — Measuring and Guiding Monosemanticity** (2025)
Introduces Feature Monosemanticity Score (FMS); proposes G-SAE conditioning on labeled concepts during training.

**2501.06254 — Rethinking Evaluation of Sparse Autoencoders through the Representation of Polysemous Words** (2025)
Shows deeper layers and attention modules distinguish polysemy, indicating semantic structure concentrates at depth.

**2501.19066 — Concept Steerers: Leveraging K-Sparse Autoencoders for Controllable Generations** (2025)
K-SAEs identify monosemantic concepts in embedding space; enables precise steering toward/away from semantic concepts without retraining.

**2412.04139 — Monet: Mixture of Monosemantic Experts for Transformers** (2024)
Integrates sparse dictionary learning directly into MoE training; scales to 262k experts revealing mutual exclusivity of semantic knowledge.

---

## Representational Hubs & Information Bottlenecks

**2505.16950 — Bottlenecked Transformers: Periodic KV Cache Consolidation for Generalised Reasoning** (2025)
Information bottleneck theory applied to middle-layer KV consolidation; shows middle layers act as representational hubs.

**2510.14095 — Unlocking Out-of-Distribution Generalization in Transformers via Recursive Latent Space Reasoning** (2025)
Proposes anchored latent representations via discrete bottleneck in middle layers; shows middle layers enable robust semantic reasoning beyond training distribution.

---

## Already in Repo — Directly Relevant

**2412.07334 — Frame Representation Hypothesis: Multi-Token LLM Interpretability and Concept-Guided Text Generation** (TACL 2025)
Extends the linear representation hypothesis to multi-token concepts as "frames" (ordered sequences whose average is the concept vector); proposes concept-guided decoding steering from that representation. Directly overlaps with the extraction/injection pipeline.
