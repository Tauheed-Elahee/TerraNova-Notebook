# Plan: Geometric Analysis of text-embedding-3-large Vectors for Medical Terms

Follows the colours/dates pipeline from `Representation-Manifolds`. Replaces hue distances with
SNOMED CT ontological distances and colour names with medical preferred terms. Embeddings are
retrieved from the existing Azure AI Search database (bare preferred terms, text-embedding-3-large,
3072-dim).

---

## Phase 1 — Concept Selection (`1-snomed-concept-selection.ipynb`)

### 1a. Explore hierarchy interactively (snowstorm-azure MCP in Claude)

Before writing any notebook code, use the snowstorm-azure MCP to pick a suitable hierarchy root
and check concept counts:

- `ecl_query("<< 50043002")` — all respiratory disorders, check total count
- `get_children("50043002")` — top-level subcategories
- Adjust ECL depth filter (e.g. `<<2 50043002` = within 2 levels) to target 100–300 concepts

Candidate starting hierarchies:

| Body system | ECL |
|---|---|
| Respiratory disorders | `<< 50043002` |
| Cardiovascular disorders | `<< 49601007` |
| Infectious diseases | `<< 40733004` |

### 1b. Retrieve concepts (Snowstorm REST API in notebook)

```python
import requests, pandas as pd

SNOWSTORM_URL = "https://snowstorm.snomedtools.org/snowstorm/snomed-ct"
BRANCH = "MAIN"

def ecl_query(ecl: str, limit: int = 500) -> list[dict]:
    url = f"{SNOWSTORM_URL}/{BRANCH}/concepts"
    params = {"ecl": ecl, "limit": limit, "active": True}
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()["items"]

concepts = ecl_query("<< 50043002", limit=300)
concept_ids   = [c["conceptId"] for c in concepts]
preferred_terms = [c["pt"]["term"] for c in concepts]

df_concepts = pd.DataFrame({"concept_id": concept_ids, "preferred_term": preferred_terms})
df_concepts.to_csv("data/concepts.csv", index=False)
```

### 1c. Compute pairwise SNOMED CT ontological distances

```python
def get_ancestors(concept_id: str) -> set[str]:
    url = f"{SNOWSTORM_URL}/{BRANCH}/concepts/{concept_id}/ancestors"
    r = requests.get(url, params={"form": "inferred", "limit": 200})
    r.raise_for_status()
    return {c["conceptId"] for c in r.json()["items"]}

ancestor_sets = {cid: get_ancestors(cid) for cid in concept_ids}

def ontological_distance(a_id, b_id):
    anc_a = ancestor_sets[a_id]
    anc_b = ancestor_sets[b_id]
    lca_depth = len(anc_a & anc_b)   # shared ancestors ≈ depth of LCA
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

## Phase 2 — Retrieve Embeddings (`2-retrieve-embeddings.ipynb`)

Embeddings are already in Azure AI Search (bare preferred terms, text-embedding-3-large, 3072-dim).
No new embeddings need to be generated.

### 2a. Fetch from Azure AI Search

```python
import os
import numpy as np
import pandas as pd
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name=os.getenv("AZURE_SEARCH_INDEX"),
    credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_KEY"))
)

# Batch fetch by concept ID
id_filter = " or ".join([f"concept_id eq '{cid}'" for cid in concept_ids])
results = client.search(
    search_text="*",
    filter=id_filter,
    select=["concept_id", "preferred_term", "embedding_vector"],  # adjust field names to match index schema
    top=len(concept_ids)
)

embeddings = {r["concept_id"]: r["embedding_vector"] for r in results}
```

### 2b. Align with concept list and normalise

```python
df_concepts = pd.read_csv("data/concepts.csv")

X_raw = np.array([embeddings[cid] for cid in df_concepts["concept_id"]])  # [n, 3072]

# Remove zero-norm rows
norms = np.linalg.norm(X_raw, axis=1)
mask = norms > 1e-3
X = X_raw[mask] / norms[mask, np.newaxis]   # unit sphere

df_concepts = df_concepts[mask].reset_index(drop=True)
D_snomed = pd.read_csv("data/ontological_distances.csv", header=None).values
D_snomed = D_snomed[np.ix_(mask, mask)]

pd.DataFrame(X).to_csv("data/embeddings_normalised.csv", index=False, header=False)
df_concepts.to_csv("data/concepts_filtered.csv", index=False)
pd.DataFrame(D_snomed).to_csv("data/ontological_distances_filtered.csv", index=False, header=False)
```

---

## Phase 3 — Geometric Analysis (`3-geometric-analysis.ipynb`)

Near-complete reuse of the colours section of
`Reference_Papers/Representation-Manifolds/3-reproduce_figures.ipynb`.

```python
import sys
sys.path.append("Reference_Papers/Representation-Manifolds")
from utils import knn_graph, largest_connected_component, chatterjee_corr
from utils import interactive_3d_plot, distance_plot

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
Xp = pca.fit_transform(X)

interactive_3d_plot(
    Xp,
    labels=concepts["preferred_term"].values,
    color_values=D_snomed[0],     # colour by distance from first concept
    colormap="Viridis",
    point_size=3
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
DXm = dijkstra(A_lcc, return_predecessors=False)
DXc = 1 - squareform(pdist(X_lcc, metric="cosine"))
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
| Ontological distances | None — new | — |
| Embedding retrieval | None — Azure AI Search SDK | — |
| `get_embeddings()` | Not needed — DB already exists | — |
| Normalisation | Direct copy | `3-reproduce_figures.ipynb` (colours section) |
| `knn_graph()` | Direct import | `Representation-Manifolds/utils.py` |
| `largest_connected_component()` | Direct import | `Representation-Manifolds/utils.py` |
| Dijkstra geodesic distances | Direct copy | `3-reproduce_figures.ipynb` |
| `chatterjee_corr()` | Via `distance_plot` | `Representation-Manifolds/utils.py` |
| `interactive_3d_plot()` | Direct import | `Representation-Manifolds/utils.py` |
| `distance_plot()` | Direct import | `Representation-Manifolds/utils.py` |

---

## Open Questions

1. What are the exact field names in the Azure AI Search index schema (`concept_id`, `embedding_vector`, etc.)?
2. Which body system hierarchy to start with — confirm via snowstorm-azure MCP before running notebook
3. What ECL depth filter gives a concept count in the 100–300 range for the chosen hierarchy?
