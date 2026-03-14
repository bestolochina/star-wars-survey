# analysis/metrics/polarization_analysis.py

from __future__ import annotations

import pandas as pd
import numpy as np
from itertools import combinations


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
