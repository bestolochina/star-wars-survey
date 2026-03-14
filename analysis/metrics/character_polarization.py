# analysis/interpretation/character_polarization.py

from __future__ import annotations

import pandas as pd
import numpy as np
from src.config import AUDIENCE_CLUSTER_LABELS
from analysis.utils.labels import add_audience_labels
from sklearn.cluster import AgglomerativeClustering


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
    - most_liked_audience_cluster
    - least_liked_audience_cluster
    """

    matrix = compute_character_alignment_matrix(means)

    rows = []

    for character in matrix.index:

        cluster_ratings = matrix.loc[character]

        max_cluster = cluster_ratings.idxmax()
        min_cluster = cluster_ratings.idxmin()

        rows.append(
            {
                "character": character,
                "audience_rating_range": cluster_ratings.max()
                - cluster_ratings.min(),
                "audience_rating_std": cluster_ratings.std(),
                "most_liked_audience_cluster": max_cluster,
                "least_liked_audience_cluster": min_cluster,
            }
        )

    result = pd.DataFrame(rows)

    result = result.sort_values(
        "audience_rating_range",
        ascending=False,
    )

    return result.reset_index(drop=True)


def compute_character_ideological_blocs(
    means: pd.DataFrame,
    n_blocs: int = 3,
) -> pd.DataFrame:
    """
    Detect ideological blocs of characters based on
    audience cluster rating patterns.
    """

    matrix = compute_character_alignment_matrix(means)

    model = AgglomerativeClustering(
        n_clusters=n_blocs,
        metric="euclidean",
        linkage="ward",
    )

    labels = model.fit_predict(matrix)

    df = pd.DataFrame(
        {
            "character": matrix.index,
            "character_ideological_bloc": labels + 1,
        }
    )

    return df.sort_values(
        "character_ideological_bloc"
    ).reset_index(drop=True)


def compute_character_bloc_summary(
    blocs: pd.DataFrame,
) -> pd.DataFrame:
    """
    Summarize characters belonging to each ideological bloc.
    """

    summary = (
        blocs
        .groupby("character_ideological_bloc")["character"]
        .apply(lambda x: ", ".join(sorted(x)))
        .reset_index()
        .rename(
            columns={
                "character_ideological_bloc": "character_ideological_bloc",
                "character": "characters",
            }
        )
    )

    return summary.sort_values("character_ideological_bloc")


def compute_character_bloc_sizes(
    blocs: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compute number of characters in each ideological bloc.
    """

    sizes = (
        blocs
        .groupby("character_ideological_bloc")
        .size()
        .reset_index(name="character_count")
        .sort_values("character_ideological_bloc")
    )

    return sizes
