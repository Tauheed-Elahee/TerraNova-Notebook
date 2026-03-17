---
title: Ontology-Constrained Generation of Domain-Specific Clinical Summaries
id: polymtl_67792
author: Mehenni, Gaya
advisor: Zouaq, Amal
publish_date: 2025-08
url: https://publications.polymtl.ca/67792/
type: Master's thesis (Polytechnique Montréal, Génie informatique)
summary: Uses medical ontologies to constrain LLM generation of clinical summaries via ontology-based annotation, a Concept-Structured Representation (CSR) of clinical notes, and ontology-guided beam search decoding — reducing hallucinations and improving domain adaptation on MIMIC-III. Also introduces MedHal, a large-scale medical hallucination detection dataset.
---

# Ontology-Constrained Generation of Domain-Specific Clinical Summaries

**Polytechnique Montréal** | Master's thesis | August 2025

## Summary

Addresses LLM hallucination and domain adaptation in clinical summarization by integrating medical ontologies at multiple stages of the generation pipeline. Evaluated primarily on MIMIC-III. Two main contributions: (1) ontology-constrained generation system, (2) MedHal hallucination evaluation dataset.

## Key Contributions

- **Domain adaptation analysis:** Ontology-based annotation of clinical notes to identify and prioritize relevant concepts per specialty (e.g. radiology vs. oncology).
- **Concept-Structured Representation (CSR):** Ontology-based prompting extracts a structured intermediate representation of clinical note content.
- **Constrained decoding:** Novel beam search variant scoring candidates by ontological hierarchy, property alignment, and concept similarity — favours output that respects ontological relationships and reduces factual inconsistencies.
- **MedHal dataset:** Large-scale, multi-source, multi-task dataset for medical hallucination detection, with annotated explanations of factual inconsistencies. Addresses limitations of smaller single-task hallucination datasets.
- Demonstrated significant improvement in domain-adapted summary generation and hallucination reduction on MIMIC-III.

## Relevance to This Project

The Concept-Structured Representation (CSR) construction is directly analogous to building concept-level representations from clinical text for downstream geometric analysis. The constrained decoding mechanism — using ontological hierarchy and similarity scores during beam search — is a concrete example of injecting SNOMED-like structure into model outputs. MedHal provides a benchmark for evaluating factual consistency of medical text generation, which could serve as an evaluation layer for concept embedding quality. The overall thesis validates the hypothesis that ontological structure (hierarchy, properties, similarity) can be operationalized as a signal in LLM pipelines.
