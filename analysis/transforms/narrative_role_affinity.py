# analysis/transforms/narrative_role_affinity.py

from __future__ import annotations

import pandas as pd


def build_narrative_role_affinity(
    alignment_matrix: pd.DataFrame,
    character_roles: pd.DataFrame,
) -> pd.DataFrame:

    df = alignment_matrix.copy()

    # -------------------------
    # Ensure index is named
    # -------------------------
    if df.index.name != "audience_cluster":
        df.index.name = "audience_cluster"

    # -------------------------
    # Wide → long
    # -------------------------
    long_df = df.reset_index().melt(
        id_vars="audience_cluster",
        var_name="character",
        value_name="score",
    )

    # -------------------------
    # Attach roles
    # -------------------------
    merged = long_df.merge(
        character_roles[["character", "narrative_role"]],
        on="character",
        how="left",
    )

    # -------------------------
    # Aggregate
    # -------------------------
    affinity = (
        merged
        .groupby(["audience_cluster", "narrative_role"])["score"]
        .mean()
        .reset_index()
    )

    # -------------------------
    # Pivot
    # -------------------------
    pivot = affinity.pivot(
        index="audience_cluster",
        columns="narrative_role",
        values="score",
    ).fillna(0)

    return pivot.reset_index()