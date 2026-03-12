# analysis/metrics/block_structure.py

from __future__ import annotations

import pandas as pd
import numpy as np


# ==========================================================
# Audience × Character Cluster Means
# ==========================================================

def compute_audience_character_cluster_means(
    matrix_raw: pd.DataFrame,
    respondent_clusters: pd.DataFrame,
    character_clusters: pd.DataFrame,
) -> pd.DataFrame:

    df = matrix_raw.merge(
        respondent_clusters,
        on="respondent_id",
        how="left",
    )

    long = (
        df.drop(columns=["audience_cluster"])
        .melt(
            id_vars=["respondent_id"],
            var_name="character",
            value_name="rating",
        )
    )

    long = long.merge(respondent_clusters, on="respondent_id", how="left")
    long = long.merge(character_clusters, on="character", how="left")

    result = (
        long.groupby(
            ["audience_cluster", "character_cluster"],
            as_index=False,
        )["rating"]
        .mean()
        .rename(columns={"rating": "mean_rating"})
    )

    return result


# ==========================================================
# Rating Deviations Relative to Character Cluster Baseline
# ==========================================================

def compute_block_deviations(
    audience_character_cluster_mean_ratings: pd.DataFrame,
) -> pd.DataFrame:

    df = audience_character_cluster_mean_ratings.copy()

    # baseline per character cluster (across all audience clusters)
    character_cluster_baseline = (
        df.groupby("character_cluster")["mean_rating"]
        .mean()
        .reset_index()
        .rename(
            columns={
                "mean_rating": "character_cluster_mean_rating"
            }
        )
    )

    df = df.merge(
        character_cluster_baseline,
        on="character_cluster",
        how="left",
    )

    df["rating_deviation"] = (
        df["mean_rating"] - df["character_cluster_mean_rating"]
    )

    return df


# ==========================================================
# Z-Scores
# ==========================================================

def compute_block_zscores(
    audience_character_cluster_rating_deviations: pd.DataFrame,
) -> pd.DataFrame:

    df = audience_character_cluster_rating_deviations.copy()

    std = df["rating_deviation"].std()

    df["z_score"] = df["rating_deviation"] / std

    return df


# ==========================================================
# Bootstrap Significance
# ==========================================================

def bootstrap_block_deviation_significance(
    matrix_raw: pd.DataFrame,
    respondent_clusters: pd.DataFrame,
    character_clusters: pd.DataFrame,
    n_bootstrap: int = 500,
) -> pd.DataFrame:

    results = []

    for _ in range(n_bootstrap):

        sample = matrix_raw.sample(frac=1, replace=True)

        means = compute_audience_character_cluster_means(
            sample,
            respondent_clusters,
            character_clusters,
        )

        dev = compute_block_deviations(means)

        results.append(dev[["audience_cluster", "character_cluster", "rating_deviation"]])

    boot = pd.concat(results)

    ci = (
        boot.groupby(
            ["audience_cluster", "character_cluster"]
        )["rating_deviation"]
        .quantile([0.025, 0.975])
        .unstack()
        .reset_index()
        .rename(columns={0.025: "ci_low", 0.975: "ci_high"})
    )

    return ci


# ==========================================================
# Extremeness
# ==========================================================

def compute_block_extremeness(
    audience_character_cluster_rating_deviations: pd.DataFrame,
) -> pd.DataFrame:

    df = audience_character_cluster_rating_deviations.copy()

    result = (
        df.groupby("audience_cluster")["rating_deviation"]
        .apply(lambda x: np.mean(np.abs(x)))
        .reset_index()
        .rename(columns={"rating_deviation": "block_extremeness"})
    )

    return result


# ==========================================================
# Narrative Selectivity
# ==========================================================

def compute_narrative_selectivity(
    audience_character_cluster_rating_deviations: pd.DataFrame,
) -> pd.DataFrame:

    df = audience_character_cluster_rating_deviations.copy()

    result = (
        df.groupby("audience_cluster")["rating_deviation"]
        .std()
        .reset_index()
        .rename(columns={"rating_deviation": "narrative_selectivity"})
    )

    return result


# ==========================================================
# Structural Tension
# ==========================================================

def compute_structural_tension(
    audience_character_cluster_rating_deviations: pd.DataFrame,
) -> pd.DataFrame:

    df = audience_character_cluster_rating_deviations.copy()

    result = (
        df.groupby("character_cluster")["rating_deviation"]
        .agg(
            tension_variance="var",
            tension_std="std",
            mean_abs_deviation=lambda x: np.mean(np.abs(x)),
        )
        .reset_index()
    )

    return result