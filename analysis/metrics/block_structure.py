# analysis/metrics/block_structure.py

from __future__ import annotations

import numpy as np
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
        audience_cluster | character_cluster | mean_rating
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
        character_clusters,
        on="character",
        how="inner",
    )

    # ----------------------------------
    # Aggregate (THE KEY STEP)
    # ----------------------------------
    block_means = (
        long_df
        .groupby(
            ["audience_cluster", "character_cluster"],
            as_index=False,
        )["rating"]
        .mean()
        .rename(columns={"rating": "mean_rating"})
        .sort_values(["audience_cluster", "character_cluster"])
    )

    return block_means


def compute_block_deviations(
    block_means: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compute deviation of audience-cluster ratings from
    global character-cluster averages.

    Parameters
    ----------
    block_means : pd.DataFrame
        Columns:
            - audience_cluster
            - character_cluster
            - mean_rating

    Returns
    -------
    pd.DataFrame
        Same structure with added column:
            - deviation
    """

    # -------------------------
    # Global baseline per character cluster
    # -------------------------
    global_means = (
        block_means
        .groupby("character_cluster")["mean_rating"]
        .mean()
        .rename("global_mean")
        .reset_index()
    )

    # -------------------------
    # Merge baseline
    # -------------------------
    merged = block_means.merge(
        global_means,
        on="character_cluster",
        how="left",
    )

    # -------------------------
    # Compute deviation
    # -------------------------
    merged["deviation"] = (
        merged["mean_rating"] - merged["global_mean"]
    )

    return merged


def compute_block_zscores(
    block_deviations: pd.DataFrame,
) -> pd.DataFrame:
    """
    Convert block deviations into z-scores.

    Z = (deviation - mean) / std
    """

    df = block_deviations.copy()

    mean_dev = df["deviation"].mean()
    std_dev = df["deviation"].std(ddof=0)

    df["z_score"] = (df["deviation"] - mean_dev) / std_dev

    return df


def bootstrap_block_deviation_significance(
    matrix_raw: pd.DataFrame,
    respondent_clusters: pd.DataFrame,
    character_clusters: pd.DataFrame,
    n_bootstrap: int = 500,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Bootstrap confidence intervals for block deviations.

    Resamples respondents within audience clusters.
    """

    rng = np.random.default_rng(random_state)

    # ----------------------------------
    # Attach cluster labels
    # ----------------------------------
    matrix = (
        matrix_raw
        .reset_index()
        .merge(respondent_clusters, on="respondent_id")
    )

    clusters = matrix["audience_cluster"].unique()

    bootstrap_results = []

    # ----------------------------------
    # Bootstrap loop
    # ----------------------------------
    for _ in range(n_bootstrap):

        sampled_frames = []

        for c in clusters:
            subset = matrix[matrix["audience_cluster"] == c]

            sampled = subset.sample(
                n=len(subset),
                replace=True,
                random_state=rng.integers(0, 1_000_000),
            )

            sampled_frames.append(sampled)

        sampled_matrix = pd.concat(sampled_frames)

        sampled_matrix = sampled_matrix.set_index("respondent_id")
        sampled_matrix = sampled_matrix.drop(columns="audience_cluster")

        means = compute_audience_character_cluster_means(
            sampled_matrix,
            respondent_clusters,
            character_clusters,
        )

        deviations = compute_block_deviations(means)

        bootstrap_results.append(deviations)

    boot_df = pd.concat(bootstrap_results, ignore_index=True)

    # ----------------------------------
    # Confidence intervals
    # ----------------------------------
    summary = (
        boot_df
        .groupby(["audience_cluster", "character_cluster"])["deviation"]
        .agg(
            ci_low=lambda x: np.percentile(x, 2.5),
            ci_high=lambda x: np.percentile(x, 97.5),
        )
        .reset_index()
    )

    return summary


# ==========================================================
# 4.2.12 Block Extremeness Index
# ==========================================================

def compute_block_extremeness(
    deviation_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Computes structural extremeness for each audience cluster.

    Extremeness = mean absolute deviation across character blocs.

    Parameters
    ----------
    deviation_df :
        Output of compute_block_deviations()

    Returns
    -------
    pd.DataFrame
        cluster | block_extremeness
    """

    extremeness = (
        deviation_df
        .assign(abs_dev=lambda df: df["deviation"].abs())
        .groupby("audience_cluster", as_index=False)["abs_dev"]
        .mean()
        .rename(columns={"abs_dev": "block_extremeness"})
        .sort_values("audience_cluster")
        .reset_index(drop=True)
    )

    return extremeness


def compute_narrative_selectivity(
    deviation_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Step 4.2.13 — Narrative Selectivity Index (NSI)

    Measures how concentrated each audience cluster's
    structural preferences are across character archetypes.

    High selectivity:
        → strong preference for few archetypes

    Low selectivity:
        → diffuse or general preference pattern
    """

    required_cols = {
        "audience_cluster",
        "character_cluster",
        "deviation",
    }

    missing = required_cols - set(deviation_df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    df = deviation_df.copy()

    # --------------------------------------------------
    # Absolute structural strength
    # --------------------------------------------------
    df["abs_dev"] = df["deviation"].abs()

    results = []

    # --------------------------------------------------
    # Compute concentration per audience cluster
    # --------------------------------------------------
    for cluster, g in df.groupby("audience_cluster"):

        total = g["abs_dev"].sum()

        if total == 0:
            selectivity = 0.0
        else:
            proportions = g["abs_dev"] / total

            # Herfindahl concentration index
            selectivity = float(np.sum(proportions**2))

        results.append(
            {
                "audience_cluster": cluster,
                "narrative_selectivity": selectivity,
            }
        )

    result_df = (
        pd.DataFrame(results)
        .sort_values("narrative_selectivity", ascending=False)
        .reset_index(drop=True)
    )

    return result_df


def compute_structural_tension(
    deviation_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Step 4.2.17 — Structural Narrative Tension

    Measures disagreement between audience clusters
    for each character cluster.
    """

    tension = (
        deviation_df
        .groupby("character_cluster")["deviation"]
        .agg(
            tension_variance="var",
            tension_std="std",
            mean_abs_deviation=lambda x: x.abs().mean(),
        )
        .reset_index()
        .sort_values("tension_variance", ascending=False)
    )

    return tension
