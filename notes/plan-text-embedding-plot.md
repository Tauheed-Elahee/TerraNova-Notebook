# Plan: Geometric Analysis of text-embedding-3-large Vectors for Medical Terms

This plan follows the colours/dates pipeline from `Representation-Manifolds` — the closest analogue
to the medical concept use case. It replaces hue distances with SNOMED CT ontological distances
and colour names with medical preferred terms.

---

## Phase 1 — Concept Selection (`1-snomed-concept-selection.ipynb`)

### 1a. Choose a hierarchy root

Use the snowstorm-azure MCP interactively to identify a suitable starting point. A focused,
well-structured body system hierarchy with 200–500 concepts is ideal for a first experiment.
Candidates:

| Body system | SNOMED ECL | Approx. size |
|---|---|---|
| Respiratory disorders | `<< 50043002` | ~1,500 (filter down) |
| Cardiovascular disorders | `<< 49601007` | ~3,000 (filter down) |
| Infectious diseases | `<< 40733004` | ~4,000 (filter down) |

Use the MCP `ecl_query` to get counts and explore hierarchy depth before committing.

### 1b. Retrieve concepts programmatically

The snowstorm-azure MCP is available interactively in Claude but for notebook use call the
Snowstorm REST API directly:

```python
import requests

SNOWSTORM_URL = "https://snowstorm.snomedtools.org/snowstorm/snomed-ct"
BRANCH = "MAIN"

def ecl_query(ecl: str, limit: int = 500) -> list[dict]:
    url = f"{SNOWSTORM_URL}/{BRANCH}/concepts"
    params = {"ecl": ecl, "limit": limit, "active": True}
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()["items"]

concepts = ecl_query("<< 50043002", limit=500)
# Each item has: conceptId, fsn (fully specified name), pt (preferred term)
```

Collect for each concept:
- `concept_id` — SNOMED CT code
- `preferred_term` — human-readable label for embedding and display

### 1c. Compute pairwise ontological distances

For each concept, retrieve its full ancestor chain and compute pairwise shortest-path distances
through the is-a hierarchy:

```python
def get_ancestors(concept_id: str) -> list[str]:
    url = f"{SNOWSTORM_URL}/{BRANCH}/concepts/{concept_id}/ancestors"
    r = requests.get(url, params={"form": "inferred", "limit": 200})
    r.raise_for_status()
    return [c["conceptId"] for c in r.json()["items"]]

# Build ancestor sets for all concepts
ancestor_sets = {cid: set(get_ancestors(cid)) for cid in concept_ids}

# Pairwise ontological distance = path length through the hierarchy
# distance(A, B) = depth(A) + depth(B) - 2 * depth(LCA(A, B))
# Approximation: use size of symmetric difference of ancestor sets
def ontological_distance(a_id, b_id):
    anc_a = ancestor_sets[a_id]
    anc_b = ancestor_sets[b_id]
    lca_depth = len(anc_a & anc_b)   # shared ancestors = depth of LCA
    return len(anc_a) + len(anc_b) - 2 * lca_depth
```

Save:
- `data/concepts.csv` — columns: `concept_id`, `preferred_term`
- `data/ontological_distances.csv` — n×n pairwise distance matrix

---

## Phase 2 — Retrieve Embeddings (`2-retrieve-embeddings.ipynb`)

### 2a. Look up existing database

The existing `text-embedding-3-large` database covers all SNOMED CT concepts. Load it and
look up embeddings for the selected concept IDs:

```python
import pandas as pd
import numpy as np

# Load existing database (adjust path as needed)
db = pd.read_parquet("path/to/embedding_database.parquet")  # index = concept_id

concepts = pd.read_csv("data/concepts.csv")
embeddings = db.loc[concepts["concept_id"]]   # shape: [n_concepts, 3072]
```

### 2b. Generate any missing embeddings

For any concepts not in the database, generate using `get_embeddings()` — direct reuse from
`Reference_Papers/Representation-Manifolds/2-get_text_embeddings.ipynb`:

```python
# --- reused from 2-get_text_embeddings.ipynb ---
import openai, os

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

missing_ids = [cid for cid in concept_ids if cid not in db.index]
if missing_ids:
    missing_terms = concepts.set_index("concept_id").loc[missing_ids, "preferred_term"]
    new_embeddings = get_embeddings(missing_terms.tolist(), model="text-embedding-3-large")
```

### 2c. Normalise and save

```python
norms = np.linalg.norm(embeddings.values, axis=1)
mask = norms > 1e-3                          # remove zero-norm rows
X = embeddings.values[mask] / norms[mask, np.newaxis]   # unit sphere

embeddings_df = pd.DataFrame(X)
embeddings_df.to_csv("data/embeddings_normalised.csv", index=False, header=False)
concepts[mask].to_csv("data/concepts_filtered.csv", index=False)
```

---

## Phase 3 — Geometric Analysis (`3-geometric-analysis.ipynb`)

Near-complete reuse of the colours section from
`Reference_Papers/Representation-Manifolds/3-reproduce_figures.ipynb`.
Substitute SNOMED CT ontological distances for hue distances.

```python
import sys
sys.path.append("Reference_Papers/Representation-Manifolds")
from utils import knn_graph, largest_connected_component, chatterjee_corr
from utils import interactive_3d_plot, distance_plot
```

### 3a. Load data

```python
import pandas as pd, numpy as np
from sklearn.decomposition import PCA
from scipy.spatial.distance import pdist, squareform
from scipy.sparse.csgraph import dijkstra

X = pd.read_csv("data/embeddings_normalised.csv", header=None).values
concepts = pd.read_csv("data/concepts_filtered.csv")
D_snomed = pd.read_csv("data/ontological_distances.csv", header=None).values
```

### 3b. PCA visualisation — reuse `interactive_3d_plot`

```python
pca = PCA(n_components=3)
Xp = pca.fit_transform(X)

interactive_3d_plot(
    Xp,
    labels=concepts["preferred_term"].values,
    color_values=D_snomed[0],          # colour by distance from a root concept
    colormap="Viridis",
    point_size=3
)
```

### 3c. k-NN graph and geodesic distances — reuse `knn_graph`, `largest_connected_component`

```python
k = 5
A = knn_graph(X, k)
A.data[A.data < 1e-3] = 1e-3
lcc_mask = largest_connected_component(A, verbose=True)

# Filter to largest connected component
X_lcc = X[lcc_mask]
D_snomed_lcc = D_snomed[np.ix_(lcc_mask, lcc_mask)]
concepts_lcc = concepts[lcc_mask]

A_lcc = knn_graph(X_lcc, k)
DXm = dijkstra(A_lcc, return_predecessors=False)       # manifold distances
DXc = 1 - squareform(pdist(X_lcc, metric="cosine"))   # cosine similarities
```

### 3d. Correlation with SNOMED distances — reuse `distance_plot`

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
| Concept retrieval | None — new (Snowstorm REST API) | — |
| Ontological distance | None — new | — |
| `get_embeddings()` | Direct copy | `2-get_text_embeddings.ipynb` |
| Normalisation | Direct copy | `3-reproduce_figures.ipynb` (colours section) |
| `knn_graph()` | Direct import | `Representation-Manifolds/utils.py` |
| `largest_connected_component()` | Direct import | `Representation-Manifolds/utils.py` |
| `dijkstra` geodesic distances | Direct copy | `3-reproduce_figures.ipynb` |
| `chatterjee_corr()` | Direct import (via `distance_plot`) | `Representation-Manifolds/utils.py` |
| `interactive_3d_plot()` | Direct import | `Representation-Manifolds/utils.py` |
| `distance_plot()` | Direct import | `Representation-Manifolds/utils.py` |

---

## Deliverables

| Notebook | Purpose |
|---|---|
| `1-snomed-concept-selection.ipynb` | ECL query → concept list + pairwise ontological distances |
| `2-retrieve-embeddings.ipynb` | Look up existing DB, generate missing, normalise, save |
| `3-geometric-analysis.ipynb` | PCA, k-NN, geodesic distances, correlation plots |

---

## Suggested First Experiment

Start with **respiratory disorders**, filtered to concepts within 4 hierarchy levels of the root
(to keep concept count manageable and ontological distances meaningful). This gives a well-defined
body system with clinical coherence and enough concepts to reveal structure (~100–200 after depth
filtering).

Use the snowstorm-azure MCP interactively first to check counts before running the notebook:
- `ecl_query("<< 50043002")` to see total concept count
- `get_children("50043002")` to see top-level subcategories
- Adjust ECL depth filter (`<<2 50043002` = within 2 levels) to hit target range
