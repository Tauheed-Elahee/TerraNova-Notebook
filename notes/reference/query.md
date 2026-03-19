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

## Breast Lump — search_concepts results (117 concepts)

### Core findings
| ID | FSN |
|---|---|
| `271940008` | Breast lump *(finding)* |
| `89164003` | Breast lump *(finding)* |
| `155958009` | Lump, breast - NOS *(disorder)* |
| `274113005` | Lump, breast - NOS *(finding)* |
| `290062006` | Lumpy breast *(finding)* |
| `827144003` | Cystic lump of breast *(disorder)* |
| `163440007` | Breasts: lumpy or irregular nodularity or O/E - shotty *(finding)* |
| `270537005` | Breast: dysplasia (& benign) or benign lump *(finding)* |
| `155947000` | Breast: dysplasia (& benign) or benign lump *(disorder)* |

### Characterisation
| ID | FSN |
|---|---|
| `792887000` | Soft lump of breast *(finding)* |
| `792891005` | Hard lump of breast *(finding)* |
| `792888005` | Smooth lump of breast *(finding)* |
| `792889002` | Irregular lump of breast *(finding)* |
| `816060007` | Mobile lump of breast *(finding)* |
| `816059002` | Fixed deep lump of breast *(finding)* |
| `816058005` | Lump of breast fixed to skin *(finding)* |
| `816057000` | Tethering of lump of breast *(finding)* |

### Size (examination)
| ID | FSN |
|---|---|
| `140682006` / `163475007` | Breast lump - pea size *(finding)* |
| `140683001` / `163476008` | Breast lump - plum size *(finding)* |
| `140684007` / `163477004` | Breast lump - tangerine size *(finding)* |
| `140685008` / `163478009` | Breast lump - orange size *(finding)* |
| `140686009` / `163479001` | Breast lump - grapefruit size *(finding)* |
| `140687000` / `163480003` | Breast lump - melon size *(finding)* |
| `140681004` / `163474006` | Breast lump size *(finding)* |
| `140688005` / `163481004` | Breast lump size NOS *(finding)* |

### Position / quadrant
| ID | FSN |
|---|---|
| `140674006` / `163467001` | Breast lump - nipple/central *(finding)* |
| `140675007` / `163468006` | Breast lump - upper inner quadrant *(finding)* |
| `140676008` / `163469003` | Breast lump - lower inner quadrant *(finding)* |
| `140677004` / `163470002` | Breast lump - upper outer quadrant *(finding)* |
| `140678009` / `163471003` | Breast lump - lower outer quadrant *(finding)* |
| `140679001` / `163472005` | Breast lump - axillary tail *(finding)* |
| `792890006` | Lump of axillary tail of breast *(finding)* |
| `1304235005` | Lump of subareolar area of breast *(finding)* |
| `816052006` | Lump of upper inner quadrant of breast *(finding)* |
| `816053001` | Lump of lower inner quadrant of breast *(finding)* |
| `816054007` | Lump of lower outer quadrant of breast *(finding)* |
| `816055008` | Lump of upper outer quadrant of breast *(finding)* |
| `140672005` / `163465009` | O/E breast lump palpated or position *(finding)* |
| `140673000` / `163466005` | No breast lump palpable *(finding/situation)* |
| `140680003` / `163473000` | Breast lump palpated NOS *(finding)* |
| `275964000` | On examination - breast lump position *(finding)* |
| `268951004` | On examination - breast lump palpated *(finding)* |

### Laterality
| ID | FSN |
|---|---|
| `12240181000119103` | Mass of left breast *(finding)* |
| `12240221000119106` | Mass of right breast *(finding)* |
| `16836091000119107` | Lump of subareolar area of left breast *(finding)* |
| `16837031000119106` | Lump of subareolar area of right breast *(finding)* |

### Consistency / regularity / tethering (examination)
| ID | FSN |
|---|---|
| `140689002` / `163482006` | Breast lump consistency *(finding)* |
| `140690006` / `163483001` | Breast lump soft *(finding)* |
| `140691005` / `163484007` | Breast lump cystic *(finding)* |
| `140692003` / `163485008` | Breast lump hard *(finding)* |
| `140694002` / `163486009` | Breast lump consistency NOS *(finding)* |
| `140695001` / `163487000` | Breast lump regularity *(finding)* |
| `140696000` / `163488005` | Breast lump smooth *(finding)* |
| `140697009` / `163489002` | Breast lump irregular *(finding)* |
| `140698004` / `163490006` | Breast lump regularity NOS *(finding)* |
| `140699007` / `163491005` | Breast lump tethering *(finding)* |
| `140700008` / `163492003` | Breast lump not tethered *(finding/situation)* |
| `140701007` / `163493008` | Breast lump fixed to skin *(finding)* |
| `140702000` / `163494002` | Breast lump fixed deep *(finding)* |
| `140703005` / `163495001` | Breast lump tethered NOS *(finding)* |
| `860671001` | No tethering of breast lump *(situation)* |

### Context / situation
| ID | FSN |
|---|---|
| `139440009` / `162160003` | Breast lump symptom *(finding)* |
| `139441008` / `162161004` | No breast lump *(situation)* |
| `139442001` / `162162006` | Breast lump present *(situation)* |
| `139443006` / `162163001` | Breast lump symptom NOS *(finding)* |
| `10750111000119108` | Breast lump in pregnancy *(finding)* |

### Procedures
| ID | FSN |
|---|---|
| `392021009` / `150299008` | Lumpectomy of breast *(procedure)* |
| `71222002` | Tylectomy *(procedure)* |
| `735085002` | Lumpectomy of left breast *(procedure)* |
| `735086001` | Lumpectomy of right breast *(procedure)* |
| `42125001` | Excisional biopsy of breast mass *(procedure)* |
| `172051009` / `310638008` | Wire guided excision of breast lump under radiological control *(procedure)* |
| `394021005` / `394911000` | Wire guided wide local excision of breast lump under radiological control *(procedure)* |
| `309546004` | Lumpectomy breast specimen *(specimen)* |

### Other
| ID | FSN |
|---|---|
| `763479005` | Metaplastic carcinoma of breast *(disorder)* |

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
