from __future__ import annotations

import pandas as pd


def compute_audience_character_cluster_means(
    matrix_raw: pd.DataFrame,
    respondent_clusters: pd.DataFrame,
    character_clusters: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compute mean rating of character clusters
    by audience clusters.

    Returns:
        cluster | character_cluster | mean_rating
    """

    # ----------------------------------
    # Wide → Long
    # ----------------------------------
    long_df = (
        matrix_raw
        .reset_index()
        .melt(
            id_vars="respondent_id",
            var_name="character",
            value_name="rating",
        )
        .dropna(subset=["rating"])
    )

    # ----------------------------------
    # Attach audience clusters
    # ----------------------------------
    long_df = long_df.merge(
        respondent_clusters,
        on="respondent_id",
        how="inner",
    )

    # ----------------------------------
    # Attach character clusters
    # ----------------------------------
    long_df = long_df.merge(
        character_clusters.rename(
            columns={"cluster": "character_cluster"}
        ),
        on="character",
        how="inner",
    )

    # ----------------------------------
    # Aggregate (THE KEY STEP)
    # ----------------------------------
    block_means = (
        long_df
        .groupby(
            ["cluster", "character_cluster"],
            as_index=False,
        )["rating"]
        .mean()
        .rename(columns={"rating": "mean_rating"})
        .sort_values(["cluster", "character_cluster"])
    )

    return block_means