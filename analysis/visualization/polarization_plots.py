# analysis/visualization/polarization_plots.py

from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from src.config import AUDIENCE_CLUSTER_LABELS


# ==========================================================
# Audience Cluster Ideological Distance Heatmap
# ==========================================================

def plot_cluster_ideological_distance_heatmap(
    distance_df: pd.DataFrame,
    path: Path
) -> pd.DataFrame:

    pivot = distance_df.pivot(
        index="audience_cluster_1",
        columns="audience_cluster_2",
        values="cluster_ideological_distance",
    )

    heatmap_df = pivot.combine_first(pivot.T)

    # Replace numeric labels with readable cluster names
    heatmap_df.index = [
        AUDIENCE_CLUSTER_LABELS.get(i, f"Cluster {i}")
        for i in heatmap_df.index
    ]

    heatmap_df.columns = [
        AUDIENCE_CLUSTER_LABELS.get(i, f"Cluster {i}")
        for i in heatmap_df.columns
    ]

    plt.figure(figsize=(6, 4))

    sns.heatmap(
        heatmap_df,
        annot=True,
        cmap="RdYlBu_r",
        linewidths=0.5,
        fmt=".2f",
    )

    plt.xlabel("Audience Cluster")
    plt.ylabel("Audience Cluster")

    plt.title("Audience Cluster Ideological Distance")

    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()

    return heatmap_df


# ==========================================================
# Character Polarization Ranking
# ==========================================================

def plot_character_polarization_ranking(
    character_polarization: pd.DataFrame,
    path: Path
) -> pd.DataFrame:

    df = character_polarization.sort_values(
        "character_rating_range_across_clusters",
        ascending=False,
    )

    plt.figure(figsize=(8, 6))

    sns.barplot(
        data=df,
        y="character",
        x="character_rating_range_across_clusters",
        color="steelblue",
    )

    plt.xlabel("Rating Range Across Audience Clusters")
    plt.ylabel("Character")

    plt.title("Character Polarization Across Audience Clusters")

    plt.tight_layout()

    plt.savefig(path, dpi=300)
    plt.close()

    return df


# ==========================================================
# Cluster Character Preference Polarization
# ==========================================================

def plot_cluster_character_preference_polarization(
    cluster_distance: pd.DataFrame,
    path: Path
) -> pd.DataFrame:

    df = cluster_distance.sort_values(
        "character_preference_distance_between_clusters",
        ascending=False,
    )

    df["cluster_pair"] = (
        df["audience_cluster_1"].astype(str)
        + " vs "
        + df["audience_cluster_2"].astype(str)
    )

    plt.figure(figsize=(6, 4))

    sns.barplot(
        data=df,
        x="cluster_pair",
        y="character_preference_distance_between_clusters",
        color="darkred",
    )

    plt.xlabel("Audience Cluster Pair")
    plt.ylabel("Character Preference Distance")

    plt.title("Audience Cluster Character Preference Polarization")

    plt.tight_layout()

    plt.savefig(path, dpi=300)
    plt.close()

    return df