# analysis/metrics/audience_character_alignment.py

from __future__ import annotations

import pandas as pd
import numpy as np


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
        index="cluster",
        columns="character",
        values="mean_rating",
    )

    return matrix.sort_index()


# ==========================================================
# Cluster Character Rankings
# ==========================================================

def compute_cluster_character_rankings(
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

def compute_cluster_character_variance(
    matrix: pd.DataFrame,
) -> pd.DataFrame:

    variance = matrix.var(axis=0)

    return pd.DataFrame(
        {
            "character": variance.index,
            "cluster_variance": variance.values,
        }
    ).sort_values(
        "cluster_variance",
        ascending=False,
    )


# ==========================================================
# Character Divergence
# ==========================================================

def compute_character_divergence(
    matrix: pd.DataFrame,
) -> pd.DataFrame:
    """
    Measures disagreement between clusters.
    """

    divergence = matrix.max(axis=0) - matrix.min(axis=0)

    return pd.DataFrame(
        {
            "character": divergence.index,
            "cluster_divergence": divergence.values,
        }
    ).sort_values(
        "cluster_divergence",
        ascending=False,
    )


# ==========================================================
# Ideological Distance
# ==========================================================

def compute_cluster_character_ideology_distance(
    cluster_coords: pd.DataFrame,
    character_coords: pd.DataFrame,
) -> pd.DataFrame:

    rows = []

    for _, c_row in cluster_coords.iterrows():

        cluster = c_row["cluster"]

        cx = c_row["axis_1"]
        cy = c_row["axis_2"]

        for _, char_row in character_coords.iterrows():

            char = char_row["character"]

            x = char_row["ideology_axis_1"]
            y = char_row["ideology_axis_2"]

            dist = np.sqrt((cx - x) ** 2 + (cy - y) ** 2)

            rows.append(
                {
                    "cluster": cluster,
                    "character": char,
                    "ideology_distance": dist,
                }
            )

    return pd.DataFrame(rows)