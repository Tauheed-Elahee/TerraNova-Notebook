"""
Stage 1 utilities — functions not available in any Reference_Papers repo or pip package.

gromov_delta  : Gromov δ-hyperbolicity via the four-point condition.
ic_distances  : Pairwise IC-based semantic distances from a SNOMED IS-A graph.
"""

import math

import networkx as nx
import numpy as np


def gromov_delta(D, sample_size=500, seed=42):
    """Gromov δ-hyperbolicity via the four-point condition.

    For a random sample of 4-tuples (a, b, c, d) from the concept set,
    compute the three pairwise-sum combinations:
        S1 = d(a,b) + d(c,d)
        S2 = d(a,c) + d(b,d)
        S3 = d(a,d) + d(b,c)
    Sort descending; δ for that 4-tuple = (S1 - S2) / 2  (largest minus second-largest).
    Returns the mean δ across all sampled 4-tuples.

    A mean δ close to 0 indicates tree-like (hyperbolic) geometry.
    Euclidean space has δ = diam/2.

    Args:
        D           : np.ndarray (n, n) — symmetric pairwise distance matrix.
        sample_size : int — number of random 4-tuples to sample.
        seed        : int — random seed for reproducibility.

    Returns:
        float — mean δ across sampled 4-tuples.
    """
    rng = np.random.default_rng(seed)
    n = D.shape[0]

    if n < 4:
        raise ValueError(f"Need at least 4 points for Gromov δ; got {n}.")

    deltas = np.empty(sample_size)
    idx = np.arange(n)

    for k in range(sample_size):
        a, b, c, d = rng.choice(idx, size=4, replace=False)
        s1 = D[a, b] + D[c, d]
        s2 = D[a, c] + D[b, d]
        s3 = D[a, d] + D[b, c]
        top2 = sorted((s1, s2, s3), reverse=True)[:2]
        deltas[k] = (top2[0] - top2[1]) / 2.0

    return float(np.mean(deltas))


def ic_distances(snomed_graph, concepts, method="resnik"):
    """Pairwise IC-based semantic distances for a set of SNOMED concepts.

    Uses corpus-free structural IC derived from the IS-A hierarchy:
        IC(c) = -log( |ontological_descendants(c)| / |all_nodes| )

    Resnik similarity  : sim(c1, c2) = IC(LCS) / max_IC   (normalised to [0,1])
    Lin similarity     : sim(c1, c2) = 2·IC(LCS) / (IC(c1) + IC(c2))

    Distance = 1 − similarity, so 0 = identical, 1 = maximally distant.

    The graph must be a child→parent DiGraph (edges: sourceId → destinationId),
    as produced by 0b-snomed-graph.ipynb.

    Concepts absent from the graph receive NaN distances.

    Args:
        snomed_graph : nx.DiGraph — IS-A edges (child → parent).
        concepts     : list of SNOMED CT concept ID strings.
        method       : 'resnik' or 'lin'.

    Returns:
        np.ndarray (n, n) — symmetric pairwise distance matrix.
    """
    if method not in ("resnik", "lin"):
        raise ValueError(f"Unknown method {method!r}. Choose 'resnik' or 'lin'.")

    G = snomed_graph
    n_total = G.number_of_nodes()

    # --- Precompute IC for every node ---
    # In a child→parent DiGraph:
    #   nx.ancestors(G, c) = nodes that can reach c = ontological descendants of c
    # Subsumer count = |ontological descendants| + 1 (self)
    ic = {}
    for node in G.nodes():
        n_desc = len(nx.ancestors(G, node)) + 1
        ic[node] = -math.log(n_desc / n_total) if n_desc < n_total else 0.0

    max_ic = max(ic.values()) if ic else 1.0

    # --- Pairwise distances ---
    n = len(concepts)
    D = np.zeros((n, n), dtype=float)

    for i in range(n):
        for j in range(i + 1, n):
            c1, c2 = concepts[i], concepts[j]

            if c1 not in G or c2 not in G:
                D[i, j] = D[j, i] = np.nan
                continue

            # Ontological ancestors of c = nodes reachable from c in child→parent graph
            anc1 = nx.descendants(G, c1) | {c1}
            anc2 = nx.descendants(G, c2) | {c2}
            common = anc1 & anc2

            if not common:
                D[i, j] = D[j, i] = 1.0
                continue

            # Lowest common subsumer = common ancestor with highest IC (most specific)
            lcs = max(common, key=lambda c: ic.get(c, 0.0))
            ic_lcs = ic.get(lcs, 0.0)

            if method == "resnik":
                sim = ic_lcs / max_ic if max_ic > 0 else 0.0
            else:  # lin
                denom = ic.get(c1, 0.0) + ic.get(c2, 0.0)
                sim = (2.0 * ic_lcs / denom) if denom > 0 else 0.0

            D[i, j] = D[j, i] = 1.0 - sim

    return D
