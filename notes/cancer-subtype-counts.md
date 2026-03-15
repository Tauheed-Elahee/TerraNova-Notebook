# SNOMED CT Cancer Subtype Concept Counts

Queried via snowstorm-azure MCP (`ecl_query`, limit=1000). Parent hierarchy:
**Malignant neoplastic disease** (`363346000`) — 6,110+ total concepts.

Counts are the number of concepts returned; entries marked 1000+ hit the query limit.

| Cancer type | SNOMED root | Concept ID | Count |
|---|---|---|---|
| Skin cancer | `<< 372130007` | `372130007` | **719** |
| Lymphoma | `<< 118600007` | `118600007` | **449** |
| Lung cancer | `<< 363358000` | `363358000` | **265** |
| Brain cancer | `<< 428061005` | `428061005` | **189** |
| Breast cancer | `<< 254837009` | `254837009` | **176** |
| Leukemia | `<< 93143009` | `93143009` | **156** |
| Pancreatic cancer | `<< 363418001` | `363418001` | **111** |
| Kidney cancer | `<< 363518003` | `363518003` | **102** |
| Ovarian cancer | `<< 363443007` | `363443007` | **90** |
| Colon cancer | `<< 363406005` | `363406005` | **84** |
| Cervical cancer | `<< 363354003` | `363354003` | **64** |
| Liver cancer | `<< 93870000` | `93870000` | **54** |
| Bladder cancer | `<< 93689003` | `93689003` | **36** |
| Thyroid cancer | `<< 363478007` | `363478007` | **31** |
| Prostate cancer | `<< 399068003` | `399068003` | **30** |

## Candidates for First Experiment (100–300 range)

| Cancer type | Count | Notes |
|---|---|---|
| Lung cancer | 265 | Good size; clinically coherent; well-structured by lobe/histology |
| Brain cancer | 189 | Good size; structured by brain region and tumour type |
| Breast cancer | 176 | Good size; structured by quadrant, histology, stage |
| Leukemia | 156 | Good size; structured by acute/chronic, myeloid/lymphoid |
| Pancreatic cancer | 111 | Slightly smaller; manageable for first experiment |
| Kidney cancer | 102 | Slightly smaller; well-structured by histology |

Lung cancer (`<< 363358000`, **265 concepts**) is a strong candidate:
clinically coherent, well-structured IS-A hierarchy by histological type and anatomical lobe,
and a comparable size to the asthma hierarchy already selected.
