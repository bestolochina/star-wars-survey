# analysis/interpretation/character_polarization.py

from __future__ import annotations

import pandas as pd
import numpy as np
from src.config import AUDIENCE_CLUSTER_LABELS
from analysis.utils.labels import add_audience_labels


# ==========================================================
# Character Means by Audience Cluster
# ==========================================================

def compute_character_cluster_means(
    matrix: pd.DataFrame,
    respondent_clusters: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compute mean rating for each character within each audience cluster.

    Parameters
    ----------
    matrix :
        Respondent × Character rating matrix.
        Index = respondent_id
        Columns = character names

    respondent_clusters :
        DataFrame with columns:
        - respondent_id
        - audience_cluster

    Returns
    -------
    DataFrame with columns:
        character
        audience_cluster
        mean_rating
    """

    df = matrix.reset_index()

    df = df.merge(
        respondent_clusters,
        on="respondent_id",
        how="left",
    )

    character_columns = [
        c for c in df.columns
        if c not in {"respondent_id", "audience_cluster", "cluster_label"}
    ]

    results: list[dict] = []

    for character in character_columns:

        grouped = (
            df.groupby("audience_cluster")[character]
            .mean()
            .reset_index()
        )

        for _, row in grouped.iterrows():

            results.append(
                {
                    "character": character,
                    "audience_cluster": int(row["audience_cluster"]),
                    "mean_rating": float(row[character]),
                }
            )

    result_df = pd.DataFrame(results)

    result_df = result_df.sort_values(
        ["character", "audience_cluster"]
    ).reset_index(drop=True)

    return result_df


# ==========================================================
# Character Alignment Matrix
# ==========================================================

def compute_character_alignment_matrix(
    means: pd.DataFrame,
) -> pd.DataFrame:
    """
    Pivot character cluster means into matrix form.

    Output format:

    character | 1 | 2 | 3
    """

    matrix = means.pivot(
        index="character",
        columns="audience_cluster",
        values="mean_rating",
    )

    # enforce cluster order
    matrix = matrix.reindex(
        columns=sorted(AUDIENCE_CLUSTER_LABELS)
    )

    matrix = matrix.sort_index()

    return matrix

# ==========================================================
# Character Polarization Index
# ==========================================================

def compute_character_polarization_index(
    means: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compute polarization of each character across audience clusters.

    Polarization metrics:
    - audience_rating_range
    - audience_rating_std
    """

    matrix = compute_character_alignment_matrix(means)

    result = pd.DataFrame(
        {
            "character": matrix.index,
            "audience_rating_range": matrix.max(axis=1)
            - matrix.min(axis=1),
            "audience_rating_std": matrix.std(axis=1),
        }
    )

    result = result.reset_index(drop=True)

    result = result.sort_values(
        "audience_rating_range",
        ascending=False,
    )

    return result