# analysis/metrics/audience_character_alignment.py

from __future__ import annotations

import pandas as pd
import numpy as np
from scipy.stats import f_oneway

from analysis.metrics.character_polarization import compute_character_alignment_matrix


# ==========================================================
# Audience–Character Alignment Matrix
# ==========================================================

def build_audience_character_alignment_matrix(
    means: pd.DataFrame,
) -> pd.DataFrame:
    """
    Convert cluster-character mean ratings into matrix form.

    Rows:
        audience clusters

    Columns:
        characters
    """

    matrix = means.pivot(
        index="audience_cluster",
        columns="character",
        values="mean_rating",
    )

    return matrix.sort_index()


# ==========================================================
# Cluster Character Rankings
# ==========================================================

def compute_audience_cluster_character_rankings(
    matrix: pd.DataFrame,
) -> pd.DataFrame:

    rankings = matrix.rank(
        axis=1,
        ascending=False,
        method="min",
    )

    return rankings


# ==========================================================
# Cluster Character Variance
# ==========================================================

def compute_character_evaluation_variance_across_audience_clusters(
    matrix: pd.DataFrame,
) -> pd.DataFrame:

    variance = matrix.var(axis=0)

    return pd.DataFrame(
        {
            "character": variance.index,
            "character_evaluation_variance_across_audience_clusters": variance.values,
        }
    ).sort_values(
        "character_evaluation_variance_across_audience_clusters",
        ascending=False,
    )


# ==========================================================
# Character Divergence
# ==========================================================

def compute_character_divergence_across_audience_clusters(
    matrix: pd.DataFrame,
) -> pd.DataFrame:
    """
    Measures disagreement between clusters.
    """

    divergence = matrix.max(axis=0) - matrix.min(axis=0)

    return pd.DataFrame(
        {
            "character": divergence.index,
            "character_evaluation_divergence_across_audience_clusters": divergence.values,
        }
    ).sort_values(
        "character_evaluation_divergence_across_audience_clusters",
        ascending=False,
    )


# ==========================================================
# Ideological Distance
# ==========================================================

def compute_audience_cluster_character_ideology_distance(
    cluster_coords: pd.DataFrame,
    character_coords: pd.DataFrame,
) -> pd.DataFrame:

    rows = []

    for _, c_row in cluster_coords.iterrows():

        cluster = c_row["audience_cluster"]

        cx = c_row["ideology_axis_1"]
        cy = c_row["ideology_axis_2"]

        for _, char_row in character_coords.iterrows():

            char = char_row["character"]

            x = char_row["ideology_axis_1"]
            y = char_row["ideology_axis_2"]

            dist = np.sqrt((cx - x) ** 2 + (cy - y) ** 2)

            rows.append(
                {
                    "audience_cluster": cluster,
                    "character": char,
                    "audience_character_ideological_distance": dist,
                }
            )

    return pd.DataFrame(rows)


def compute_character_segmentation_strength_across_audience_clusters(
    respondent_cluster_df: pd.DataFrame,
    character_rating_columns: dict[str, str],
) -> pd.DataFrame:

    results = []

    for character_column, character_name in character_rating_columns.items():

        cluster_groups = []

        for audience_cluster in sorted(
            respondent_cluster_df["audience_cluster"].dropna().unique()
        ):

            ratings = respondent_cluster_df.loc[
                respondent_cluster_df["audience_cluster"] == audience_cluster,
                character_column,
            ].dropna()

            if len(ratings) > 0:
                cluster_groups.append(ratings)

        if len(cluster_groups) >= 2:

            f_statistic, p_value = f_oneway(*cluster_groups)

            results.append(
                {
                    "character": character_name,
                    "character_segmentation_strength_f_statistic": f_statistic,
                    "character_segmentation_strength_p_value": p_value,
                }
            )

    segmentation_df = (
        pd.DataFrame(results)
        .sort_values(
            "character_segmentation_strength_f_statistic",
            ascending=False,
        )
    )

    return segmentation_df


def compute_audience_cluster_character_affinity_profiles(
    means: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build audience cluster character affinity profiles.

    For each audience cluster:
    - rank characters by mean rating
    """

    matrix = compute_character_alignment_matrix(means)

    rows = []

    for audience_cluster in matrix.columns:

        cluster_ratings = matrix[audience_cluster].sort_values(
            ascending=False
        )

        for rank, (character, mean_rating) in enumerate(
            cluster_ratings.items(),
            start=1,
        ):

            rows.append(
                {
                    "audience_cluster": audience_cluster,
                    "character_rank": rank,
                    "character": character,
                    "character_mean_rating": mean_rating,
                }
            )

    return pd.DataFrame(rows)


def compute_audience_bloc_affinity(
    means: pd.DataFrame,
    blocs: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compute mean character ratings for each
    audience cluster × ideological character bloc.
    """

    matrix = compute_character_alignment_matrix(means)

    df = matrix.reset_index().rename(columns={"index": "character"})

    df = df.merge(
        blocs,
        on="character",
        how="left",
    )

    # Detect cluster columns (numeric)
    value_cols = [
        c for c in df.columns
        if isinstance(c, (int, float))
    ]

    affinity = (
        df
        .groupby("character_ideological_bloc")[value_cols]
        .mean()
        .T
    )

    affinity.index.name = "audience_cluster"

    affinity = affinity.reset_index()

    return affinity.sort_values("audience_cluster")