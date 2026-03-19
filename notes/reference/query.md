# Breast Cancer — SNOMED CT Query Reference

## ECL Queries (use `<< concept_id` to include all descendants)

| Category | Root Concept ID | FSN | Count |
|---|---|---|---|
| Disorders | `254837009` | Malignant neoplasm of breast | 196 |
| Mammography (all) | `71651007` | Mammography | 62 |
| Screening procedures | `268547008` | Screening for malignant neoplasm of breast | 3 |
| Family history (situations) | `313102001` | Family history of neoplasm of breast | 7 |

---

## Screening Procedures (`<< 268547008`) — 3 concepts

| ID | FSN |
|---|---|
| `268547008` | Screening for malignant neoplasm of breast *(procedure)* |
| `716035006` | Scintimammography for malignant neoplasm screening *(procedure)* |
| `609223006` | Magnetic resonance imaging of breast for screening for malignant neoplasm *(procedure)* |

---

## Mammography (`<< 71651007`) — 62 concepts (selected)

| ID | FSN |
|---|---|
| `71651007` | Mammography *(procedure)* |
| `24623002` | Screening mammography *(procedure)* |
| `43204002` | Mammography of bilateral breasts *(procedure)* |
| `384151000119104` | Screening mammography of bilateral breasts *(procedure)* |
| `392521000119107` | Screening mammography of right breast *(procedure)* |
| `392531000119105` | Screening mammography of left breast *(procedure)* |
| `258172002` | Stereotactic mammography *(procedure)* |
| `450566007` | Digital tomosynthesis of breast *(procedure)* |
| `726551006` | Contrast enhanced spectral mammography *(procedure)* |
| `445171002` | Core needle biopsy of breast using mammography guidance *(procedure)* |
| `699132003` | Breast screening mammography offered *(situation)* |
| … | *(+ 51 more: bilateral/left/right variants, biopsy guidance, marker insertion, etc.)* |

---

## Family History (`<< 313102001`) — 7 concepts

| ID | FSN |
|---|---|
| `313102001` | Family history of neoplasm of breast *(situation)* |
| `429740004` | Family history of malignant neoplasm of breast *(situation)* |
| `430292006` | Family history of malignant neoplasm of breast in first degree relative *(situation)* |
| `143461000119107` | Family history of malignant neoplasm of breast in first degree relative <50 *(situation)* |
| `154141000119104` | Family history of malignant neoplasm of breast diagnosed before 45 *(situation)* |
| `143451000119105` | Family history of malignant neoplasm of breast at under 50 in second degree relative *(situation)* |
| `767310001` | Family history of malignant neoplasm of breast at under 50 in second degree female relative *(situation)* |

---

## Standalone Concepts (no ECL subtree, query by ID)

| ID | FSN | Tag |
|---|---|---|
| `134405005` | Malignant neoplasm of breast suspected | situation |
| `366980001` | Suspected breast cancer | situation |
| `12275351000119103` | Breast cancer screening declined | situation |
| `866242004` | At increased risk of malignant neoplasm of breast | finding |
| `705089007` | At risk of breast cancer | finding |
| `724451007` | Fear of breast cancer | finding |
| `406100007` | Seen by breast cancer nurse | finding |
| `9901000087105` | Investigation for breast cancer | finding |
| `10011000087104` | Breast cancer detected by self assessment | finding |
| `10041000087103` | Breast cancer detected by diagnostic imaging | finding |
| `10051000087100` | Breast cancer detected by clinical breast examination | finding |
| `10651000087109` | Breast cancer gene mutation positive | finding |
| `412734009` | BRCA1 gene mutation detected | finding |
| `412738007` | BRCA2 gene mutation detected | finding |
| `412736006` | BRCA1 gene mutation not detected | finding |
| `412739004` | BRCA2 gene mutation not detected | finding |
| `445333001` | Breast cancer genetic marker of susceptibility detected | finding |
| `445180002` | Breast cancer genetic marker of susceptibility not detected | finding |

---

## Python Query Reference

```python
BREAST_CANCER_ECL_QUERIES = {
    "disorders":      "<< 254837009",
    "mammography":    "<< 71651007",
    "screening":      "<< 268547008",
    "family_history": "<< 313102001",
}

BREAST_CANCER_STANDALONE_IDS = {
    # situations
    "suspected":      ["134405005", "366980001", "12275351000119103"],
    # risk findings
    "at_risk":        ["866242004", "705089007"],
    # detection findings
    "detection":      ["10011000087104", "10041000087103", "10051000087100"],
    # gene / marker findings
    "gene_marker":    ["10651000087109", "412734009", "412738007",
                       "412736006", "412739004", "445333001", "445180002"],
    # clinical / admin findings
    "clinical_admin": ["406100007", "9901000087105", "724451007"],
}
```
