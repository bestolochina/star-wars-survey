# analysis/metrics/phase5_6_narrative_coalitions.py

from __future__ import annotations

import pandas as pd
import numpy as np
from networkx.algorithms.community import louvain_communities


# ==========================================================
# Build Cluster-Conditioned Networks
# ==========================================================

def build_cluster_conditioned_edges(
    alignment_matrix: pd.DataFrame,
    correlation_matrix: pd.DataFrame,
) -> pd.DataFrame:

    edges = []

    characters = correlation_matrix.columns.tolist()

    for cluster in alignment_matrix.index:

        preferences = alignment_matrix.loc[cluster]

        # Optional normalization (recommended)
        if preferences.std() != 0:
            preferences = (preferences - preferences.mean()) / preferences.std()

        for i, char_i in enumerate(characters):
            for j, char_j in enumerate(characters):

                if j <= i:
                    continue

                corr = correlation_matrix.loc[char_i, char_j]

                weight = (
                    corr
                    * preferences[char_i]
                    * preferences[char_j]
                )

                edges.append(
                    {
                        "cluster": cluster,
                        "char_1": char_i,
                        "char_2": char_j,
                        "correlation": corr,
                        "weight": weight,
                    }
                )

    return pd.DataFrame(edges)


# ==========================================================
# Filter Edges
# ==========================================================

def filter_edges(edges_df: pd.DataFrame, top_k: int = 3) -> pd.DataFrame:

    # -------------------------
    # 1. Keep only positive edges
    # -------------------------
    edges_df = edges_df[edges_df["weight"] > 0]

    # -------------------------
    # 2. Strength filter
    # -------------------------
    edges_df = edges_df[
        (edges_df["correlation"] >= 0.4) &
        (edges_df["weight"] >= 0.2)
    ]

    edges_df["abs_weight"] = edges_df["weight"].abs()

    # -------------------------
    # 3. Symmetric Top-K
    # -------------------------
    selected_edges = []

    for cluster in edges_df["cluster"].unique():
        df_c = edges_df[edges_df["cluster"] == cluster]

        node_edges = {}

        for _, row in df_c.iterrows():
            node_edges.setdefault(row["char_1"], []).append(row)
            node_edges.setdefault(row["char_2"], []).append(row)

        keep = set()

        for node, edges in node_edges.items():
            top_edges = sorted(edges, key=lambda x: abs(x["weight"]), reverse=True)[:top_k]
            for e in top_edges:
                keep.add((e["char_1"], e["char_2"]))

        df_filtered = df_c[
            df_c.apply(lambda r: (r["char_1"], r["char_2"]) in keep, axis=1)
        ]

        selected_edges.append(df_filtered)

    edges_df = pd.concat(selected_edges)

    # -------------------------
    # 4. REMOVE DUPLICATES (← HERE)
    # -------------------------
    edges_df[["char_1", "char_2"]] = np.sort(
        edges_df[["char_1", "char_2"]].values,
        axis=1
    )

    edges_df = edges_df.drop_duplicates(
        subset=["cluster", "char_1", "char_2"]
    )

    return edges_df.drop(columns="abs_weight")


# ==========================================================
# Detect Communities
# ==========================================================

def detect_communities(edges_df: pd.DataFrame) -> pd.DataFrame:

    import networkx as nx
    from networkx.algorithms.community import louvain_communities

    results = []

    for cluster in edges_df["cluster"].unique():

        cluster_edges = edges_df[
            edges_df["cluster"] == cluster
        ]

        G = nx.Graph()

        for _, row in cluster_edges.iterrows():
            G.add_edge(
                row["char_1"],
                row["char_2"],
                weight=row["weight"],
            )

        # 🔥 Louvain (real communities)
        communities = louvain_communities(
            G,
            weight="weight",
            resolution=1.2,  # tune this if needed
        )

        for community_id, nodes in enumerate(communities):
            for node in nodes:
                results.append({
                    "cluster": cluster,
                    "character": node,
                    "community_id": community_id,
                })

    return pd.DataFrame(results)