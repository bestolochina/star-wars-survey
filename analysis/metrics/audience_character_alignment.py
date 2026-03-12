# analysis/metrics/audience_character_alignment.py

from __future__ import annotations

import pandas as pd
import numpy as np
from scipy.stats import f_oneway


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