# analysis/visualization/character_structure.py

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
from src.config import AUDIENCE_CLUSTER_LABELS, CHARACTER_IDEOLOGY_AXES_READABLE, CHARACTER_CLUSTER_LABELS
from sklearn.decomposition import PCA
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities



def plot_character_polarization_map(
    bridge: pd.DataFrame,
    polarization: pd.DataFrame,
    save_path: str | None = None,
) -> None:
    """
    Character Polarization Map

    X-axis:
        polarization (audience_rating_range)

    Y-axis:
        character_bridge_index

    Each point = character
    """

    df = bridge.merge(
        polarization,
        on="character",
        how="inner",
    )

    fig, ax = plt.subplots(figsize=(10, 8))

    ax.scatter(
        df["audience_rating_range"],
        df["character_bridge_index"],
    )

    for _, row in df.iterrows():
        ax.text(
            row["audience_rating_range"],
            row["character_bridge_index"],
            row["character"],
            fontsize=9,
        )

    ax.set_xlabel("Character Polarization (Rating Range)")
    ax.set_ylabel("Bridge Index (Cross-Audience Appeal)")
    ax.set_title("Character Polarization Map")

    ax.axhline(
        df["character_bridge_index"].median(),
        linestyle="--",
        linewidth=1,
    )

    ax.axvline(
        df["audience_rating_range"].median(),
        linestyle="--",
        linewidth=1,
    )

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")

    plt.close()


def plot_character_polarization_triangle(
    means: pd.DataFrame,
    save_path: str | None = None,
) -> None:

    pivot = (
        means
        .pivot(
            index="character",
            columns="audience_cluster",
            values="mean_rating",
        )
    )

    x = pivot[1]
    y = pivot[2]
    color = pivot[3]

    plt.figure(figsize=(8, 6))

    scatter = plt.scatter(
        x,
        y,
        c=color,
        s=120,
    )

    for character in pivot.index:
        plt.text(
            pivot.loc[character, 1],
            pivot.loc[character, 2],
            character,
            fontsize=8,
        )

    plt.xlabel(f"{AUDIENCE_CLUSTER_LABELS[1]} Rating")
    plt.ylabel(f"{AUDIENCE_CLUSTER_LABELS[2]} Rating")

    cbar = plt.colorbar(scatter)
    cbar.set_label(f"{AUDIENCE_CLUSTER_LABELS[3]} Rating")

    plt.title("Character Polarization Structure")

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")

    plt.close()

def plot_character_ideology_gradient_map(
    variance: pd.DataFrame,
    attachment: pd.DataFrame,
    save_path: str | None = None,
) -> None:
    """
    Character Ideology Gradient Map

    X-axis:
        audience_variance (ideological disagreement)

    Y-axis:
        attachment_strength (identity anchor strength)
    """

    df = variance.merge(
        attachment,
        on="character",
        how="inner",
    )

    x = df["audience_variance"]
    y = df["attachment_strength"]

    plt.figure(figsize=(8, 8))

    plt.scatter(x, y, alpha=0.8)

    for _, row in df.iterrows():
        plt.text(
            row["audience_variance"],
            row["attachment_strength"],
            row["character"],
            fontsize=9,
        )

    plt.axhline(y=y.mean(), linestyle="--")
    plt.axvline(x=x.mean(), linestyle="--")

    plt.xlabel("Audience Variance (Ideological Disagreement)")
    plt.ylabel("Cluster Attachment Strength")

    plt.title("Character Ideology Gradient Map")

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")

    plt.close()


def plot_character_audience_ideology_field(
    alignment_matrix: pd.DataFrame,
    save_path: str | None = None,
) -> None:
    """
    Character–Audience Ideology Field

    PCA projection of character ratings across audience clusters.

    Characters → points
    Audience clusters → vectors
    """

    # -------------------------
    # PCA on character matrix
    # -------------------------

    pca = PCA(n_components=2)

    coords = pca.fit_transform(alignment_matrix)

    characters = alignment_matrix.index

    fig, ax = plt.subplots(figsize=(9, 9))

    # -------------------------
    # Plot characters
    # -------------------------

    ax.scatter(
        coords[:, 0],
        coords[:, 1],
    )

    for i, character in enumerate(characters):

        ax.text(
            coords[i, 0],
            coords[i, 1],
            character,
            fontsize=9,
        )

    # -------------------------
    # Plot audience vectors
    # -------------------------

    loadings = pca.components_.T

    for i, column in enumerate(alignment_matrix.columns):

        ax.arrow(
            0,
            0,
            loadings[i, 0] * 3,
            loadings[i, 1] * 3,
            head_width=0.05,
            length_includes_head=True,
        )

        ax.text(
            loadings[i, 0] * 3.2,
            loadings[i, 1] * 3.2,
            column,
            fontsize=10,
        )

    ax.axhline(0, linestyle="--")
    ax.axvline(0, linestyle="--")

    ax.set_xlabel(CHARACTER_IDEOLOGY_AXES_READABLE[1])
    ax.set_ylabel(CHARACTER_IDEOLOGY_AXES_READABLE[2])

    ax.set_title("Character–Audience Ideology Field")

    if save_path:
        plt.savefig(save_path, bbox_inches="tight")

    plt.close()


def plot_character_ideology_map(
        coords: pd.DataFrame,
        save_path: str,
) -> None:

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.scatter(
        coords["ideology_axis_1"],
        coords["ideology_axis_2"],
        alpha=0.8,
    )

    for _, row in coords.iterrows():
        ax.text(
            row["ideology_axis_1"],
            row["ideology_axis_2"],
            row["character"],
            fontsize=8,
        )

    ax.set_xlabel(CHARACTER_IDEOLOGY_AXES_READABLE[1])
    ax.set_ylabel(CHARACTER_IDEOLOGY_AXES_READABLE[2])
    ax.set_title("Character Ideology Map")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()


def plot_character_archetype_map(
    df,
    save_path=None,
):

    axis_x = "ideology_axis_1"
    axis_y = "ideology_axis_2"

    axis_x_label = CHARACTER_IDEOLOGY_AXES_READABLE[1]
    axis_y_label = CHARACTER_IDEOLOGY_AXES_READABLE[2]

    fig, ax = plt.subplots(figsize=(10, 8))

    colors = {
        1: "#e63946",  # Power & Ambiguity
        2: "#457b9d",  # Heroic Core
        3: "#2a9d8f",  # Prequel Identity
    }

    for cluster, group in df.groupby("attached_audience_cluster"):

        ax.scatter(
            group[axis_x],
            group[axis_y],
            label=CHARACTER_CLUSTER_LABELS[cluster],
            s=120,
            alpha=0.8,
            color=colors.get(cluster, "gray"),
        )

        for _, row in group.iterrows():
            ax.text(
                row[axis_x],
                row[axis_y],
                row["character"],
                fontsize=9,
                ha="center",
                va="bottom",
            )

    ax.axhline(0, linestyle="--", linewidth=1)
    ax.axvline(0, linestyle="--", linewidth=1)

    ax.set_xlabel(axis_x_label)
    ax.set_ylabel(axis_y_label)

    ax.set_title("Character Ideology Archetype Map")

    ax.legend()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.close()

def plot_character_polarization_network(
    edges,
    save_path=None,
):

    G = nx.Graph()

    for _, row in edges.iterrows():

        G.add_edge(
            row["source"],
            row["target"],
            weight=abs(row["correlation"]),
            sign=row["type"],
        )

    pos = nx.spring_layout(G, seed=42)

    # Detect communities
    communities = list(greedy_modularity_communities(G))

    community_map = {}

    for i, comm in enumerate(communities):
        for node in comm:
            community_map[node] = i

    colors = [community_map[n] for n in G.nodes()]

    plt.figure(figsize=(10, 8))

    positive_edges = [
        (u, v)
        for u, v, d in G.edges(data=True)
        if d["sign"] == "positive"
    ]

    negative_edges = [
        (u, v)
        for u, v, d in G.edges(data=True)
        if d["sign"] == "negative"
    ]

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=900,
        node_color=colors,
        cmap=plt.cm.Set2,
    )

    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=positive_edges,
        width=2,
    )

    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=negative_edges,
        style="dashed",
        width=2,
    )

    nx.draw_networkx_labels(
        G,
        pos,
        font_size=9,
    )

    plt.title("Character Polarization Network (character_network_community Structure)")

    plt.axis("off")

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.close()