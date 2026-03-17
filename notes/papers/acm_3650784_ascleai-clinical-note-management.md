---
title: "AscleAI: A LLM-based Clinical Note Management System for Enhancing Clinician Productivity"
id: acm_10.1145/3613905.3650784
author: Han, Park, Huh, Oh, Do, Kim
publish_date: 2024
url: https://dl.acm.org/doi/10.1145/3613905.3650784
doi: 10.1145/3613905.3650784
venue: CHI 2024 Extended Abstracts
summary: LLM-based system that auto-generates clinical notes from patient-clinician dialogues and supports real-time information retrieval; validated through clinician interviews and design probe study showing reduced cognitive burden.
---

# AscleAI: A LLM-based Clinical Note Management System for Enhancing Clinician Productivity

**ACM** | CHI 2024 Extended Abstracts | DOI: 10.1145/3613905.3650784

## Summary

System paper presenting AscleAI, which uses LLMs to automatically generate clinical notes from patient-clinician dialogues and supports real-time information retrieval during consultations. Motivated by interview findings with six clinicians and a design probe study. Targets reduced documentation burden and lower cognitive load.

## Key Contributions

- Automatic clinical note generation from patient-clinician dialogue using LLMs.
- Real-time information retrieval integrated into clinical workflow.
- Formative study (clinician interviews + design probe) grounding the system design in practitioner needs.
- Demonstrated lower cognitive burden and improved documentation accuracy in user evaluation.

## Relevance to This Project

Illustrates the downstream use case for grounded clinical concept representations: a system that generates structured clinical notes from free-form dialogue inherently needs to map spoken language to canonical medical concepts. The real-time retrieval component suggests a need for fast, accurate concept embedding lookup — the kind of geometry-aware retrieval this project aims to enable. The clinician productivity framing also motivates the practical value of reliable SNOMED-grounded representations over unconstrained LLM output.
