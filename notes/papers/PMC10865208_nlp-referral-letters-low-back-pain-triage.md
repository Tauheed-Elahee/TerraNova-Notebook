---
title: Natural Language Processing of Referral Letters for Machine Learning–Based Triaging of Patients With Low Back Pain to the Most Appropriate Intervention
id: PMC10865208
author: Fudickar, Bantel, Spieker, Töpfer, Stegeman, Schiphorst Preuper, Reneman, Wolff, Soer
publish_date: 2024-01-30
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC10865208/
doi: 10.2196/46857
journal: Journal of Medical Internet Research (JMIR)
summary: NLP extraction of referral letter content (reasons, patient goals) added to structured EHR data improves ML triage models for low back pain patients by up to 19.5% F1-score, though overall accuracy remains insufficient for clinical use.
---

# Natural Language Processing of Referral Letters for Machine Learning–Based Triaging of Patients With Low Back Pain

**PMC:** 10865208 | JMIR 2024 | DOI: 10.2196/46857

## Summary

Retrospective study of 1,608 low back pain patient records. Tested whether adding NLP-extracted qualitative features from referral letters (referral reasons, patient goals) improves ML models (SVM, kNN, MLP) for triaging patients to the most appropriate intervention. Found measurable improvement for two specific triage classes (anesthesiology and rehabilitation) but overall model accuracy remains too low for clinical deployment.

## Key Contributions

- NLP of unstructured referral letters (reasons, goals) extracts features that complement structured EHR variables.
- Up to 19.5% F1-score improvement for specific triage categories when referral letter features are included.
- SVM, kNN, and MLP compared across feature sets with and without NLP-derived content.
- Overall accuracy still insufficient for clinical application — identifies the gap rather than closing it.

## Relevance to This Project

Demonstrates that free-text clinical narratives carry triage-relevant signal not captured by structured codes. Motivates encoding clinical text alongside SNOMED codes rather than codes alone. The low-back-pain domain is a well-studied multi-class triage problem, making it a useful benchmark for evaluating concept embedding quality. The finding that only certain triage classes benefit from text enrichment suggests that some clinical concepts are better differentiated by ontological structure while others require linguistic context.
