---
title: Enhancing Clinical Note Generation with ICD-10, Clinical Ontology Knowledge Graphs, and Chain-of-Thought Prompting Using GPT-4
id: sage_10.1177/15578666251411390
author: Makohon, Najafi, Wu, Brochhausen, Li
publish_date: 2025-12-04
url: https://journals.sagepub.com/doi/10.1177/15578666251411390
doi: 10.1177/15578666251411390
journal: Journal of Computational Biology
summary: Chain-of-Thought prompting with GPT-4 augmented by ICD-10 codes and a clinical ontology knowledge graph outperforms standard one-shot prompting for clinical note generation on the CodiEsp dataset.
---

# Enhancing Clinical Note Generation with ICD-10, Clinical Ontology Knowledge Graphs, and Chain-of-Thought Prompting Using GPT-4

**SAGE / Journal of Computational Biology** | 2025 | DOI: 10.1177/15578666251411390

## Summary

Combines Chain-of-Thought (CoT) prompt engineering with GPT-4, ICD-10 diagnostic codes, and a clinical ontology-based knowledge graph to improve clinical note generation. Semantic search retrieves relevant ontology context at inference time. Evaluated on the CodiEsp dataset; CoT + ontology KG outperforms standard one-shot prompting.

## Key Contributions

- CoT prompting strategy that incorporates ICD-10 codes and patient information as structured context for GPT-4.
- Clinical ontology knowledge graph constructed to provide semantic context during generation.
- Semantic search over the KG to retrieve relevant ontology relations at inference time.
- Demonstrated improvement over one-shot baseline on CodiEsp (Spanish clinical NLP benchmark).

## Relevance to This Project

This paper is a direct example of injecting ontological structure (ICD-10 / clinical KG) into LLM generation via prompting rather than architectural changes. The CoT mechanism makes the ontological reasoning steps explicit, which is complementary to the geometric approach: while this paper encodes ontology in the prompt, this project asks whether that same ontological structure is already latent in the model's representation space. The CodiEsp dataset and ICD-10 grounding provide a concrete evaluation setup that could be adapted to SNOMED CT.
