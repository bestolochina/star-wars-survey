# analysis/metrics/cluster_profiles.py

from __future__ import annotations
import pandas as pd


def compute_cluster_profiles(
    matrix_raw: pd.DataFrame,
    cluster_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compute mean character ratings within each character cluster.

    Returns LONG format:
        character | cluster | mean_rating
    """

    # -----------------------------------
    # Character → cluster mapping
    # -----------------------------------
    char_to_cluster = dict(
        zip(cluster_df["character"], cluster_df["cluster"])
    )

    # -----------------------------------
    # Wide → Long
    # -----------------------------------
    long_df = (
        matrix_raw
        .melt(
            var_name="character",
            value_name="rating"
        )
        .dropna(subset=["rating"])
    )

    # attach cluster labels
    long_df["cluster"] = long_df["character"].map(char_to_cluster)

    # -----------------------------------
    # Mean rating per character per cluster
    # -----------------------------------
    profile_df = (
        long_df
        .groupby(["character", "cluster"], as_index=False)["rating"]
        .mean()
        .rename(columns={"rating": "mean_rating"})
        .sort_values(["cluster", "character"])
    )

    return profile_df