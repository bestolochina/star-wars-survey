# analysis/metrics/audience_cluster_metrics.py

from __future__ import annotations

import pandas as pd


# ==========================================================
# PHASE 3 — CHARACTER CLUSTER PROFILES
# ==========================================================

def compute_cluster_profiles(
    matrix_raw: pd.DataFrame,
    cluster_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Phase 3:
    Compute mean character ratings within each CHARACTER cluster.

    Returns LONG format:
        character | cluster | mean_rating
    """

    # -----------------------------------
    # Character → cluster mapping
    # -----------------------------------
    char_to_cluster = dict(
        zip(cluster_df["character"], cluster_df["character_cluster"])
    )

    # -----------------------------------
    # Wide → Long
    # -----------------------------------
    long_df = (
        matrix_raw
        .melt(
            var_name="character",
            value_name="rating",
        )
        .dropna(subset=["rating"])
    )

    long_df["character_cluster"] = long_df["character"].map(char_to_cluster)

    # -----------------------------------
    # Mean rating per character per cluster
    # -----------------------------------
    profile_df = (
        long_df
        .groupby(["character", "character_cluster"], as_index=False)["rating"]
        .mean()
        .rename(columns={"rating": "mean_rating"})
        .sort_values(["character_cluster", "character"])
    )

    # -----------------------------------
    # Cluster sizes (number of ratings)
    # -----------------------------------
    cluster_sizes = (
        long_df
        .groupby("character_cluster")["rating"]
        .count()
        .rename("n_ratings")
        .reset_index()
    )

    profile_df = profile_df.merge(
        cluster_sizes,
        on="character_cluster",
        how="left",
    )

    return profile_df


# ==========================================================
# PHASE 4 — CLUSTER MEAN PROFILES (AUDIENCE SEGMENTS)
# ==========================================================

def load_cluster_profiles(path: str | pd.PathLike) -> pd.DataFrame:
    """
    Load cluster mean profiles and validate schema.

    Expected columns:
        character | audience_cluster | mean_rating
    """

    df = pd.read_csv(path)

    required = {"character", "audience_cluster", "mean_rating"}
    missing = required - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    return df.sort_values(["audience_cluster", "character"]).reset_index(drop=True)


# ==========================================================
# Overall Mean Reference
# ==========================================================

def compute_overall_means(
    profile_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compute overall mean rating per character
    across all clusters.

    Returns:
        character | mean_rating_overall
    """

    overall_df = (
        profile_df
        .groupby("character", as_index=False)["mean_rating"]
        .mean()
        .rename(
            columns={"mean_rating": "mean_rating_overall"}
        )
        .sort_values("character")
    )

    return overall_df


# ==========================================================
# Cluster Extremeness Metric
# ==========================================================

def compute_cluster_extremeness(
    profile_df: pd.DataFrame,
    overall_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Measure how strongly each cluster deviates
    from overall audience taste.

    Extremeness =
        mean absolute deviation from global mean.
    """

    merged = profile_df.merge(
        overall_df,
        on="character",
        how="left",
    )

    merged["abs_deviation"] = (
        merged["mean_rating"]
        - merged["mean_rating_overall"]
    ).abs()

    extreme_df = (
        merged
        .groupby("audience_cluster", as_index=False)["abs_deviation"]
        .mean()
        .rename(
            columns={"abs_deviation": "extremeness_score"}
        )
        .sort_values("extremeness_score", ascending=False)
    )

    return extreme_df

# analysis/metrics/cluster_profiles.py

def compute_audience_cluster_profiles(
    matrix_raw: pd.DataFrame,
    respondent_clusters: pd.DataFrame,
) -> pd.DataFrame:
    """
    Phase 4:
    Compute mean character ratings within RESPONDENT clusters.

    Parameters
    ----------
    matrix_raw :
        Wide matrix
            index = respondent_id
            columns = characters

    respondent_clusters :
        DataFrame:
            respondent_id | audience_cluster

    Returns
    -------
    LONG format:
        character | character_cluster | mean_rating
    """

    # -----------------------------------
    # Attach cluster labels to respondents
    # -----------------------------------
    df = matrix_raw.copy()

    cluster_map = respondent_clusters.set_index(
        "respondent_id"
    )["audience_cluster"]

    df["audience_cluster"] = cluster_map

    # -----------------------------------
    # Wide → Long
    # -----------------------------------
    long_df = (
        df.reset_index()
        .melt(
            id_vars=["respondent_id", "audience_cluster"],
            var_name="character",
            value_name="rating",
        )
        .dropna(subset=["rating"])
    )

    # -----------------------------------
    # Mean rating per character per cluster
    # -----------------------------------
    profile_df = (
        long_df
        .groupby(["character", "audience_cluster"], as_index=False)["rating"]
        .mean()
        .rename(columns={"rating": "mean_rating"})
        .sort_values(["audience_cluster", "character"])
    )

    return profile_df