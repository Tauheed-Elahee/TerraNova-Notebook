# Plan: Geometric Analysis of text-embedding-3-large Vectors for Medical Disorders

Follows the colours/dates pipeline from `Representation-Manifolds`. Replaces hue distances with
SNOMED CT ontological distances and colour names with SNOMED CT disorder preferred terms.
Concepts are filtered to the `disorder` semantic tag. Embeddings are generated fresh using
`text-embedding-3-large` (3072-dim) via the OpenAI API.

---

## Phase 1 — Concept Selection (`1-snomed-concept-selection.ipynb`)

### 1a. Explore hierarchy interactively (snowstorm-azure MCP in Claude)

Before writing any notebook code, use the snowstorm-azure MCP to pick a suitable hierarchy root
and check concept counts. Target 100–300 `disorder` concepts for a first experiment.

```
ecl_query("<< 50043002")          # all respiratory disorders — check count
get_children("50043002")          # top-level subcategories
get_by_semantic_tag("disorder")   # confirm tool returns disorder concepts
```

Candidate starting hierarchies:

| Body system | SNOMED root | ECL |
|---|---|---|
| Respiratory disorders | `50043002` | `<< 50043002` |
| Cardiovascular disorders | `49601007` | `<< 49601007` |
| Infectious diseases | `40733004` | `<< 40733004` |

Use `ecl_query` with increasing depth limits to find a count in the 100–300 range before
committing. The ECL `<<2 50043002` restricts to concepts within 2 levels of the root.

### 1b. Retrieve disorder concepts (Snowstorm REST API in notebook)

The Snowstorm REST API supports a `semanticTag` parameter to filter results server-side,
avoiding the need to post-filter in Python:

```python
import requests
import pandas as pd

SNOWSTORM_URL = "https://snowstorm.snomedtools.org/snowstorm/snomed-ct"
BRANCH = "MAIN"

def get_disorder_concepts(ecl: str, limit: int = 300) -> list[dict]:
    url = f"{SNOWSTORM_URL}/{BRANCH}/concepts"
    params = {
        "ecl": ecl,
        "semanticTag": "disorder",
        "limit": limit,
        "active": True,
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()["items"]

concepts = get_disorder_concepts("<< 50043002", limit=300)
concept_ids     = [c["conceptId"] for c in concepts]
preferred_terms = [c["pt"]["term"] for c in concepts]
fsns            = [c["fsn"]["term"] for c in concepts]

df_concepts = pd.DataFrame({
    "concept_id":     concept_ids,
    "preferred_term": preferred_terms,
    "fsn":            fsns,
})
df_concepts.to_csv("data/concepts.csv", index=False)
```

### 1c. Compute pairwise SNOMED CT ontological distances

For each concept, retrieve its full ancestor chain. Pairwise distance is computed as the
shortest path through the IS-A hierarchy using the shared ancestor (LCA) approximation:

```
distance(A, B) = depth(A) + depth(B) − 2 × depth(LCA(A, B))
               ≈ |ancestors(A)| + |ancestors(B)| − 2 × |ancestors(A) ∩ ancestors(B)|
```

```python
import numpy as np

def get_ancestors(concept_id: str) -> set[str]:
    url = f"{SNOWSTORM_URL}/{BRANCH}/concepts/{concept_id}/ancestors"
    r = requests.get(url, params={"form": "inferred", "limit": 200})
    r.raise_for_status()
    return {c["conceptId"] for c in r.json()["items"]}

ancestor_sets = {cid: get_ancestors(cid) for cid in concept_ids}

def ontological_distance(a_id, b_id):
    anc_a = ancestor_sets[a_id]
    anc_b = ancestor_sets[b_id]
    lca_depth = len(anc_a & anc_b)
    return len(anc_a) + len(anc_b) - 2 * lca_depth

n = len(concept_ids)
D_snomed = np.zeros((n, n))
for i in range(n):
    for j in range(i + 1, n):
        d = ontological_distance(concept_ids[i], concept_ids[j])
        D_snomed[i, j] = d
        D_snomed[j, i] = d

pd.DataFrame(D_snomed).to_csv("data/ontological_distances.csv", index=False, header=False)
```

---

## Phase 2 — Generate Embeddings (`2-generate-embeddings.ipynb`)

Re-embed preferred terms directly using `text-embedding-3-large` via the OpenAI API.
Direct reuse of `get_embeddings()` from `Reference_Papers/Representation-Manifolds/2-get_text_embeddings.ipynb`.

### 2a. Embed preferred terms

```python
# --- reused from 2-get_text_embeddings.ipynb ---
import openai, os, pandas as pd, numpy as np

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def get_embeddings(queries, model, **kwargs):
    queries = [q.replace('\n', ' ') for q in queries]
    embeddings_data = []
    for chunk in chunker(queries, 2048):
        response = client.embeddings.create(input=chunk, model=model, **kwargs)
        embeddings_data.extend(response.data)
    return pd.DataFrame([x.embedding for x in embeddings_data], index=queries)
# --- end reuse ---

df_concepts = pd.read_csv("data/concepts.csv")
X_raw = get_embeddings(df_concepts["preferred_term"].tolist(), model="text-embedding-3-large")
# shape: [n_concepts, 3072]

X_raw.to_csv("data/embeddings_raw.csv", index=False, header=False)
```

### 2b. Normalise and align with distance matrix

```python
D_snomed = pd.read_csv("data/ontological_distances.csv", header=None).values

norms = np.linalg.norm(X_raw.values, axis=1)
mask  = norms > 1e-3                                       # remove zero-norm rows
X     = X_raw.values[mask] / norms[mask, np.newaxis]      # unit sphere [n, 3072]

df_concepts = df_concepts[mask].reset_index(drop=True)
D_snomed    = D_snomed[np.ix_(mask, mask)]

pd.DataFrame(X).to_csv("data/embeddings_normalised.csv", index=False, header=False)
df_concepts.to_csv("data/concepts_filtered.csv", index=False)
pd.DataFrame(D_snomed).to_csv("data/ontological_distances_filtered.csv", index=False, header=False)
```

---

## Phase 3 — Geometric Analysis (`3-geometric-analysis.ipynb`)

Near-complete reuse of the colours section of
`Reference_Papers/Representation-Manifolds/3-reproduce_figures.ipynb`.
SNOMED CT ontological distances replace hue distances.

```python
import sys
sys.path.append("Reference_Papers/Representation-Manifolds")
from utils import knn_graph, largest_connected_component, interactive_3d_plot, distance_plot

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from scipy.spatial.distance import pdist, squareform
from scipy.sparse.csgraph import dijkstra
```

### 3a. Load

```python
X        = pd.read_csv("data/embeddings_normalised.csv", header=None).values
concepts = pd.read_csv("data/concepts_filtered.csv")
D_snomed = pd.read_csv("data/ontological_distances_filtered.csv", header=None).values
```

### 3b. PCA visualisation

```python
pca = PCA(n_components=3)
Xp  = pca.fit_transform(X)

interactive_3d_plot(
    Xp,
    labels=concepts["preferred_term"].values,
    color_values=D_snomed[0],     # colour by ontological distance from first concept
    colormap="Viridis",
    point_size=3,
)
```

### 3c. k-NN graph and geodesic distances

```python
k = 5
A = knn_graph(X, k)
A.data[A.data < 1e-3] = 1e-3
lcc_mask = largest_connected_component(A, verbose=True)

X_lcc        = X[lcc_mask]
D_snomed_lcc = D_snomed[np.ix_(lcc_mask, lcc_mask)]
concepts_lcc = concepts[lcc_mask].reset_index(drop=True)

A_lcc = knn_graph(X_lcc, k)
DXm   = dijkstra(A_lcc, return_predecessors=False)
DXc   = 1 - squareform(pdist(X_lcc, metric="cosine"))
```

### 3d. Correlation plots

```python
# Manifold distance vs SNOMED ontological distance
fig, ax = distance_plot(
    DXm, D_snomed_lcc,
    labels=concepts_lcc["preferred_term"].values,
    corr_coef="pearson",
    xlabel="SNOMED CT ontological distance",
    ylabel="Manifold distance",
)

# Cosine similarity vs SNOMED ontological distance
fig, ax = distance_plot(
    DXc, D_snomed_lcc,
    labels=concepts_lcc["preferred_term"].values,
    corr_coef="chatterjee",
    square_distances=True,
    xlabel="Squared SNOMED CT ontological distance",
    ylabel="Cosine similarity",
)
```

---

## Code Reuse Summary

| Task | Reuse | Source |
|---|---|---|
| Concept retrieval | None — Snowstorm REST API | — |
| Semantic tag filtering | None — REST API `semanticTag` param | — |
| Ontological distances | None — new | — |
| `get_embeddings()` | Direct copy | `2-get_text_embeddings.ipynb` |
| Normalisation | Direct copy | `3-reproduce_figures.ipynb` (colours section) |
| `knn_graph()` | Direct import | `Representation-Manifolds/utils.py` |
| `largest_connected_component()` | Direct import | `Representation-Manifolds/utils.py` |
| Dijkstra geodesic distances | Direct copy | `3-reproduce_figures.ipynb` |
| `chatterjee_corr()` | Via `distance_plot` | `Representation-Manifolds/utils.py` |
| `interactive_3d_plot()` | Direct import | `Representation-Manifolds/utils.py` |
| `distance_plot()` | Direct import | `Representation-Manifolds/utils.py` |

---

## Deliverables

| Notebook | Purpose |
|---|---|
| `1-snomed-concept-selection.ipynb` | ECL query (disorder) → concept list + pairwise ontological distances |
| `2-generate-embeddings.ipynb` | Embed preferred terms with text-embedding-3-large, normalise, save |
| `3-geometric-analysis.ipynb` | PCA, k-NN, geodesic distances, correlation plots |

---

## Suggested First Experiment

Start with **respiratory disorders** (`<< 50043002`), filtered to `disorder` semantic tag.
This gives a clinically coherent body system with well-defined IS-A hierarchy structure.

Use the snowstorm-azure MCP interactively first to confirm concept counts:

```
ecl_query("<< 50043002")     # total count
ecl_query("<<2 50043002")    # within 2 levels — adjust depth to hit 100–300 disorders
get_children("50043002")     # inspect top-level subcategories
```

---

## Completed (2026-03-15)

### Phase 1a — Hierarchy exploration (done)

Ran snowstorm-azure MCP queries to find a hierarchy with 100–300 disorder concepts:

| ECL | Approx. count | Verdict |
|---|---|---|
| `<< 50043002` (all respiratory) | 500+ | Too large |
| `<< 128272009` (lower respiratory) | 350+ | Too large |
| `<< 275498002` (respiratory infections) | 350+ | Too large |
| `<< 195967001` (asthma) | ~115 | — |
| `<< 254837009` (breast cancer) | 176 | **Selected** |

**Decision:** use `<< 254837009` (breast cancer) for the first experiment.

### Notebooks created (done)

- `1-snomed-concept-selection.ipynb` — fetches breast cancer disorders, computes pairwise ontological distances
- `2-generate-embeddings.ipynb` — embeds preferred terms with `text-embedding-3-large`, normalises
- `3-geometric-analysis.ipynb` — PCA, k-NN, geodesic distances, Pearson + Chatterjee correlation plots

### Supporting files (done)

- `data/` directory created
- `utils.py` copied from `Reference_Papers/Representation-Manifolds/utils.py` to repo root
- Notebook 3 updated to import `utils` directly (no `sys.path` hack)

### Still to run

Notebooks 1–3 in order (notebook 1 makes ~176 Snowstorm API calls for ancestor chains).
