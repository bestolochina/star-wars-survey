# analysis/metrics/cluster_profiles.py

from __future__ import annotations

import pandas as pd


def compute_cluster_profiles(
    raw_matrix: pd.DataFrame,
    cluster_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compute interpretable character profiles for each cluster.

    Uses RAW (non-standardized) ratings.

    Returns
    -------
    profile_df : DataFrame
        columns = ["cluster", "character", "mean_rating"]
    """

    # ---------------------------------------
    # Wide → Long
    # ---------------------------------------

    long_df = (
        raw_matrix
        .reset_index(drop=True)
        .melt(
            var_name="character",
            value_name="rating",
        )
        .dropna(subset=["rating"])
    )

    # ---------------------------------------
    # Attach cluster labels
    # ---------------------------------------

    long_df = long_df.merge(
        cluster_df,
        on="character",
        how="left",
    )

    # ---------------------------------------
    # Mean rating per character within cluster
    # ---------------------------------------

    profile_df = (
        long_df
        .groupby(["cluster", "character"], as_index=False)
        .agg(mean_rating=("rating", "mean"))
        .sort_values(["cluster", "mean_rating"], ascending=[True, False])
    )

    return profile_df