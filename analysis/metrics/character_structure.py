# analysis/metrics/character_structure.py

from __future__ import annotations

import pandas as pd
from sklearn.decomposition import PCA
from src.config import CHARACTER_IDEOLOGY_AXES
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities


# ==========================================================
# Helpers
# ==========================================================

def _pivot_character_cluster_means(
    means: pd.DataFrame,
) -> pd.DataFrame:
    """
    Convert long-format means table into:

        character × audience_cluster matrix

    Required columns:
        character
        cluster
        mean_rating
    """

    required = {"character", "cluster", "mean_rating"}

    missing = required - set(means.columns)

    if missing:
        raise ValueError(
            f"Missing columns in means table: {missing}"
        )

    matrix = (
        means
        .pivot(
            index="character",
            columns="cluster",
            values="mean_rating",
        )
        .sort_index()
    )

    return matrix


# ==========================================================
# Character Bridge Index
# ==========================================================

def compute_character_bridge_index(
    means: pd.DataFrame,
) -> pd.DataFrame:
    """
    Bridge Index measures how evenly a character is liked
    across audience clusters.

    Formula:

        bridge_index = 1 - (max - min)

    High value  → broadly liked across blocs
    Low value   → strongly polarized character
    """

    matrix = _pivot_character_cluster_means(means)

    max_scores = matrix.max(axis=1)
    min_scores = matrix.min(axis=1)

    bridge_index = 1 - (max_scores - min_scores)

    result = pd.DataFrame(
        {
            "character": matrix.index,
            "bridge_index": bridge_index.values,
        }
    )

    return result.sort_values(
        "bridge_index",
        ascending=False,
    ).reset_index(drop=True)


# ==========================================================
# Character Cluster Attachment
# ==========================================================

def compute_character_cluster_attachment(
    means: pd.DataFrame,
) -> pd.DataFrame:
    """
    Determine which audience cluster each character is most attached to.

    Attachment = cluster with highest mean rating.

    Returns
    -------
    DataFrame:
        character
        attached_cluster
        attachment_strength
    """

    pivot = means.pivot(
        index="character",
        columns="cluster",
        values="mean_rating",
    )

    rows = []

    for character, row in pivot.iterrows():

        attached_cluster = row.idxmax()
        strength = row.max()

        rows.append(
            {
                "character": character,
                "attached_cluster": attached_cluster,
                "attachment_strength": strength,
            }
        )

    result = pd.DataFrame(rows)

    return result

# ==========================================================
# Character Audience Variance
# ==========================================================

def compute_character_audience_variance(
    means: pd.DataFrame,
) -> pd.DataFrame:
    """
    Measures how much audiences disagree about a character.

    Metric:
        variance across audience cluster means
    """

    matrix = _pivot_character_cluster_means(means)

    variance = matrix.var(axis=1)

    result = pd.DataFrame(
        {
            "character": matrix.index,
            "audience_variance": variance.values,
        }
    )

    return result.sort_values(
        "audience_variance",
        ascending=False,
    ).reset_index(drop=True)


def compute_character_ideology_coordinates(
    alignment: pd.DataFrame,
) -> pd.DataFrame:

    pca = PCA(n_components=2)

    coords = pca.fit_transform(alignment)

    result = pd.DataFrame({
        "character": alignment.index,
        "ideology_axis_1": coords[:, 0],
        "ideology_axis_2": coords[:, 1],
    })

    return result


def build_character_structure_metrics(
    polarization: pd.DataFrame,
    bridge: pd.DataFrame,
    variance: pd.DataFrame,
    attachment: pd.DataFrame,
) -> pd.DataFrame:

    df = polarization.merge(
        bridge,
        on="character",
    )

    df = df.merge(
        variance,
        on="character",
    )

    df = df.merge(
        attachment,
        on="character",
    )

    return df


def compute_character_ideology_quadrants(
    coords: pd.DataFrame,
) -> pd.DataFrame:

    df = coords.copy()

    axis_cols = [
        f"ideology_axis_{axis}"
        for axis in CHARACTER_IDEOLOGY_AXES
    ]

    x_col, y_col = axis_cols

    def quadrant(row: pd.Series) -> str:

        x = row[x_col]
        y = row[y_col]

        if x >= 0 and y >= 0:
            return "Q1"
        if x >= 0 and y < 0:
            return "Q2"
        if x < 0 and y >= 0:
            return "Q3"
        return "Q4"

    df["ideology_quadrant"] = df.apply(quadrant, axis=1)

    return df


def compute_character_correlation_network(
    matrix: pd.DataFrame,
    threshold: float = 0.25,
):

    corr = matrix.corr()

    edges = []

    for c1 in corr.columns:
        for c2 in corr.columns:

            if c1 >= c2:
                continue

            value = corr.loc[c1, c2]

            if abs(value) >= threshold:

                edges.append(
                    {
                        "source": c1,
                        "target": c2,
                        "correlation": value,
                        "type": "positive" if value > 0 else "negative",
                    }
                )

    return pd.DataFrame(edges)


def compute_character_communities(edges: pd.DataFrame) -> pd.DataFrame:

    G = nx.Graph()

    for _, row in edges.iterrows():
        G.add_edge(
            row["source"],
            row["target"],
            weight=abs(row["correlation"]),
        )

    communities = list(greedy_modularity_communities(G))

    rows = []

    for i, community in enumerate(communities, start=1):

        for character in community:

            rows.append(
                {
                    "character": character,
                    "community": i,
                }
            )

    return pd.DataFrame(rows)


def build_character_structure_triangulation(
    profiles: pd.DataFrame,
    communities: pd.DataFrame,
) -> pd.DataFrame:

    df = profiles.merge(
        communities,
        on="character",
        how="left",
    )

    df = df[
        [
            "character",
            "attached_cluster_label",
            "ideology_quadrant",
            "community",
        ]
    ]

    # df = df.rename(
    #     columns={
    #         "attached_cluster_label": "archetype_bloc",
    #         "community": "network_community",
    #     }
    # )

    return df.sort_values(
        ["community", "attached_cluster_label"]
    )