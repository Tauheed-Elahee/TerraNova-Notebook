# SNOMED CT Disorder Hierarchy Counts

Queried via snowstorm-azure MCP (`ecl_query`, limit=1000). Counts marked 1000+ hit the query
limit — exact totals require the Snowstorm REST API `total` field directly.

| Body system | SNOMED root ECL | Concept ID | Count |
|---|---|---|---|
| Respiratory disorders | `<< 50043002` | `50043002` | 1000+ |
| Cardiovascular disorders | `<< 49601007` | `49601007` | 1000+ |
| Digestive disorders | `<< 53619000` | `53619000` | 1000+ |
| Malignant neoplastic disease | `<< 363346000` | `363346000` | 1000+ |
| Infectious disease | `<< 40733004` | `40733004` | 1000+ |
| Mental disorders | `<< 74732009` | `74732009` | 1000+ |
| Musculoskeletal disorders | `<< 928000` | `928000` | 1000+ |
| Autoimmune disease | `<< 85828009` | `85828009` | **788** |

Autoimmune disease is the only hierarchy that fits within the 1000 query limit at **788 concepts**,
making it a practical candidate for a first experiment — large enough for robust geometric analysis
and coherent as a clinical domain.
