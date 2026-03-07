# analysis/metrics/narrative_alignment.py

from __future__ import annotations

import pandas as pd
from src.config import CHARACTER_CLUSTER_LABELS


# ==========================================================
# Audience Bloc Dominance
# ==========================================================

def compute_audience_bloc_dominance(
    block_means: pd.DataFrame,
) -> pd.DataFrame:

    results: list[dict] = []

    for cluster, group in block_means.groupby("cluster"):

        top_row = group.loc[group["mean_rating"].idxmax()]

        results.append(
            {
                "cluster": cluster,
                "dominant_character_cluster": int(
                    top_row["character_cluster"]
                ),
                "dominant_mean": float(top_row["mean_rating"]),
            }
        )

    return pd.DataFrame(results).sort_values("cluster")


# ==========================================================
# Audience Preference Gap
# ==========================================================

def compute_audience_preference_gap(
    block_means: pd.DataFrame,
) -> pd.DataFrame:

    results: list[dict] = []

    for cluster, group in block_means.groupby("cluster"):

        sorted_group = group.sort_values(
            "mean_rating", ascending=False
        )

        top = sorted_group.iloc[0]
        second = sorted_group.iloc[1]

        top_bloc = int(top["character_cluster"])
        second_bloc = int(second["character_cluster"])

        results.append(
            {
                "cluster": cluster,
                "top_bloc": top_bloc,
                "top_bloc_label": CHARACTER_CLUSTER_LABELS[top_bloc],
                "second_bloc": second_bloc,
                "second_bloc_label": CHARACTER_CLUSTER_LABELS[second_bloc],
                "preference_gap": float(
                    top["mean_rating"] - second["mean_rating"]
                ),
            }
        )

    return (
        pd.DataFrame(results)
        .sort_values("cluster")
    )

# ==========================================================
# Narrative Alignment Index
# ==========================================================

def compute_narrative_alignment_index(
    block_means: pd.DataFrame,
) -> pd.DataFrame:

    results: list[dict] = []

    for cluster, group in block_means.groupby("cluster"):

        alignment = group["mean_rating"].std()

        results.append(
            {
                "cluster": cluster,
                "alignment_index": float(alignment),
            }
        )

    return pd.DataFrame(results).sort_values("cluster")
