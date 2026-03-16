# analysis/metrics/polarization_analysis.py

from __future__ import annotations

import pandas as pd
import numpy as np
from itertools import combinations

from src.config import CHARACTER_RATING_COLUMNS


# ==========================================================
# Cluster Ideological Distance Matrix
# ==========================================================

def compute_cluster_ideological_distance_matrix(
    cluster_ideology_index: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compute pairwise ideological distance between audience clusters.

    Parameters
    ----------
    cluster_ideology_index : pd.DataFrame
        Columns:
        - audience_cluster
        - cluster_ideology_index

    Returns
    -------
    pd.DataFrame
        Columns:
        - audience_cluster_1
        - audience_cluster_2
        - cluster_ideological_distance
    """

    rows = []

    clusters = cluster_ideology_index["audience_cluster"].tolist()

    ideology_map = dict(
        zip(
            cluster_ideology_index["audience_cluster"],
            cluster_ideology_index["cluster_ideology_index"],
        )
    )

    for c1, c2 in combinations(clusters, 2):

        distance = abs(
            ideology_map[c1] - ideology_map[c2]
        )

        rows.append(
            {
                "audience_cluster_1": c1,
                "audience_cluster_2": c2,
                "cluster_ideological_distance": distance,
            }
        )

    return pd.DataFrame(rows)


# ==========================================================
# Cluster Ideological Polarization Metrics
# ==========================================================

def compute_cluster_ideological_polarization_metrics(
    cluster_ideology_index: pd.DataFrame,
    engagement_index: pd.DataFrame,
    positivity_bias: pd.DataFrame,
) -> pd.DataFrame:
    """
    Combine ideological position, engagement, and positivity bias
    for each audience cluster.

    Returns
    -------
    pd.DataFrame
        Columns:
        - audience_cluster
        - cluster_ideology_position
        - cluster_audience_engagement_index
        - cluster_character_rating_bias
    """

    df = (
        cluster_ideology_index
        .merge(
            engagement_index,
            on="audience_cluster",
        )
        .merge(
            positivity_bias,
            on="audience_cluster",
        )
    )

    df = df.rename(
        columns={
            "cluster_ideology_index": "cluster_ideology_position",
            "engagement_index": "cluster_audience_engagement_index",
            "audience_cluster_character_rating_positivity_bias":
                "cluster_character_rating_bias",
        }
    )

    return df


# ==========================================================
# Character Polarization Summary
# ==========================================================

def compute_character_polarization_summary(
    alignment_matrix: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compute character polarization metrics across audience clusters.
    """

    results = []

    clusters = alignment_matrix.index.tolist()

    for character in alignment_matrix.columns:

        ratings = alignment_matrix[character]

        # Range polarization
        rating_range = ratings.max() - ratings.min()

        # Pairwise divergence
        diffs = []

        for c1, c2 in combinations(clusters, 2):

            diff = abs(
                alignment_matrix.loc[c1, character]
                - alignment_matrix.loc[c2, character]
            )

            diffs.append(diff)

        mean_divergence = np.mean(diffs)

        results.append(
            {
                "character": character,
                "character_rating_range_across_clusters": rating_range,
                "character_mean_rating_divergence_across_clusters": mean_divergence,
            }
        )

    df = pd.DataFrame(results)

    df = df.sort_values(
        "character_rating_range_across_clusters",
        ascending=False,
    )

    return df


# ==========================================================
# Narrative Polarization Index
# ==========================================================

def compute_narrative_polarization_index(
    character_summary: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compute overall narrative polarization level.

    Returns
    -------
    pd.DataFrame
        Columns:
        - narrative_polarization_index
        - character_count
    """

    index_value = character_summary[
        "character_rating_range_across_clusters"
    ].mean()

    df = pd.DataFrame(
        {
            "narrative_polarization_index": [index_value],
            "character_count": [len(character_summary)],
        }
    )

    return df


# ==========================================================
# Character Polarization Driver Decomposition
# ==========================================================

def compute_character_polarization_driver_decomposition(
    alignment_matrix: pd.DataFrame,
    cluster_ideology_index: pd.DataFrame,
) -> pd.DataFrame:
    """
    Decompose character polarization into ideological vs taste-driven components.

    For each character, we measure how strongly rating differences between
    audience clusters align with ideological distance.

    Returns
    -------
    pd.DataFrame
        Columns
        - character
        - ideology_alignment_correlation
        - polarization_driver
    """

    ideology_map = dict(
        zip(
            cluster_ideology_index["audience_cluster"],
            cluster_ideology_index["cluster_ideology_index"],
        )
    )

    clusters = alignment_matrix.index.tolist()

    results = []

    for character in alignment_matrix.columns:

        rating_differences = []
        ideology_distances = []

        for c1, c2 in combinations(clusters, 2):

            rating1 = alignment_matrix.loc[c1, character]
            rating2 = alignment_matrix.loc[c2, character]

            rating_diff = abs(rating1 - rating2)

            ideology_diff = abs(
                ideology_map[c1] - ideology_map[c2]
            )

            rating_differences.append(rating_diff)
            ideology_distances.append(ideology_diff)

        if len(rating_differences) > 1:

            corr = np.corrcoef(
                ideology_distances,
                rating_differences,
            )[0, 1]

        else:
            corr = np.nan

        abs_corr = abs(corr)

        if abs_corr >= 0.5:
            driver = "ideology-driven"
        elif abs_corr <= 0.2:
            driver = "taste-driven"
        else:
            driver = "mixed"

        results.append(
            {
                "character": character,
                "ideology_alignment_correlation": corr,
                "polarization_driver": driver,
            }
        )

    df = pd.DataFrame(results)

    df = df.sort_values(
        "ideology_alignment_correlation",
        ascending=False,
    )

    return df


def compute_ideological_sorting_strength(
    driver_df: pd.DataFrame,
) -> pd.DataFrame:

    df = driver_df.copy()

    strength = df["ideology_alignment_correlation"].abs().mean()

    result = pd.DataFrame(
        {
            "ideological_sorting_strength": [strength],
            "character_count": [len(df)],
        }
    )

    return result


def compute_ideological_polarization_asymmetry(
    polarization_summary: pd.DataFrame,
    driver_df: pd.DataFrame,
) -> pd.DataFrame:

    df = polarization_summary.merge(
        driver_df[["character", "ideology_alignment_correlation"]],
        on="character",
        how="left",
    )

    pos = df[
        df["ideology_alignment_correlation"] > 0
    ]["character_rating_range_across_clusters"]

    neg = df[
        df["ideology_alignment_correlation"] < 0
    ]["character_rating_range_across_clusters"]

    mean_pos = pos.mean()
    mean_neg = neg.mean()

    asymmetry_index = mean_pos - mean_neg

    result = pd.DataFrame(
        {
            "mean_polarization_positive_alignment": [mean_pos],
            "mean_polarization_negative_alignment": [mean_neg],
            "ideological_polarization_asymmetry_index": [asymmetry_index],
        }
    )

    return result


def compute_cluster_narrative_profiles(
    alignment_matrix: pd.DataFrame,
    cluster_polarization_metrics: pd.DataFrame,
) -> pd.DataFrame:

    # ==========================================================
    # Character columns (readable names used in analysis)
    # ==========================================================

    character_columns = list(CHARACTER_RATING_COLUMNS.values())

    # ==========================================================
    # Favorite / least liked characters
    # ==========================================================

    cluster_character_means = (
        alignment_matrix
        .groupby("audience_cluster")[character_columns]
        .mean()
    )

    favorite_character = cluster_character_means.idxmax(axis=1)
    least_liked_character = cluster_character_means.idxmin(axis=1)

    # ==========================================================
    # Base metrics
    # ==========================================================

    df = cluster_polarization_metrics.copy()

    df["favorite_character"] = df["audience_cluster"].map(favorite_character)
    df["least_liked_character"] = df["audience_cluster"].map(least_liked_character)

    # ==========================================================
    # Narrative classification
    # ==========================================================

    def classify_profile(row: pd.Series) -> str:

        ideology = row["cluster_ideology_position"]
        bias = row["cluster_character_rating_bias"]
        engagement = row["cluster_audience_engagement_index"]

        if engagement < 0.5:
            return "low_engagement_audience"

        # strong ideological alignment
        if ideology >= 2:
            return "dark_side_oriented_audience"

        if ideology <= 0.8:
            return "hero_oriented_audience"

        # highly engaged but ideologically moderate
        if engagement >= 0.8 and abs(bias) <= 0.05:
            return "balanced_high_engagement_audience"

        # everything else
        return "mixed_narrative_audience"

    df["narrative_profile"] = df.apply(classify_profile, axis=1)

    return df


# ==========================================================
# 5.3.1 Audience Cluster Character Mean Scores
# ==========================================================

def compute_audience_cluster_character_mean_scores(
    alignment_matrix: pd.DataFrame,
) -> pd.DataFrame:

    """
    Returns the audience cluster-character mean rating matrix.

    Rows:
        audience clusters

    Columns:
        characters

    Values:
        mean evaluation score
    """

    mean_scores = alignment_matrix.copy()

    mean_scores.index.name = "audience_cluster"

    return mean_scores