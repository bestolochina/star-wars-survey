# analysis/transforms/coalition_ideology_mapping.py

from __future__ import annotations

import pandas as pd


def build_coalition_ideology_mapping(
    community_df: pd.DataFrame,
    ideology_df: pd.DataFrame,
    metrics_df: pd.DataFrame,
    alignment_matrix: pd.DataFrame,   # ← ADD THIS
) -> pd.DataFrame:
    """
    Build coalition-level ideology positions and merge with coalition metrics.

    Output columns:
    - audience_cluster
    - community_id
    - ideology_axis_1
    - ideology_axis_2
    - coalition_type  ✅ (from metrics_df)
    - n_characters
    - density
    - mean_weight
    - mean_preference
    """

    # -------------------------
    # 1. Attach ideology to characters
    # -------------------------
    merged = community_df.merge(
        ideology_df,
        on="character",
        how="left",
    )

    # -------------------------
    # 2. Aggregate to coalition level
    # -------------------------
    results = []

    for (audience_cluster, community_id), df in merged.groupby(
            ["audience_cluster", "community_id"]
    ):
        members = df["character"].tolist()

        coords = df.set_index("character")

        # 🔥 get preferences
        preferences = alignment_matrix.loc[audience_cluster, members]

        # normalize weights
        weights = preferences / preferences.sum()

        ideology_axis_1 = (coords["ideology_axis_1"] * weights).sum()
        ideology_axis_2 = (coords["ideology_axis_2"] * weights).sum()

        results.append({
            "audience_cluster": audience_cluster,
            "community_id": community_id,
            "ideology_axis_1": ideology_axis_1,
            "ideology_axis_2": ideology_axis_2,
        })

    coalition_positions = pd.DataFrame(results)

    # -------------------------
    # 3. Merge with metrics (🔥 includes coalition_type)
    # -------------------------
    coalition_ideology = coalition_positions.merge(
        metrics_df,
        on=["audience_cluster", "community_id"],
        how="left",
    )

    return coalition_ideology