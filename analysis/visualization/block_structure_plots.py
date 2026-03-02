# analysis/visualization/block_structure_plots.py

from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def plot_audience_character_cluster_heatmap(
    block_means: pd.DataFrame,
    save_path: Path,
) -> None:

    matrix = block_means.pivot(
        index="cluster",
        columns="character_cluster",
        values="mean_rating",
    )

    # # ✅ Defensive numeric coercion (FIX)
    # matrix = matrix.apply(pd.to_numeric, errors="coerce")

    # IMPORTANT FIX
    matrix = matrix.astype(float)

    plt.figure(figsize=(8, 6))

    sns.heatmap(
        matrix,
        annot=True,
        fmt=".2f",
        linewidths=0.5,
    )

    plt.title("Audience × Character Cluster Mean Ratings")
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()

    print(f"Saved heatmap → {save_path}")


def plot_block_deviation_heatmap(
    deviation_df: pd.DataFrame,
    output_path: Path,
) -> None:
    """
    Plot audience × character-cluster deviation heatmap.
    """

    # -------------------------
    # Pivot
    # -------------------------
    heatmap_data = deviation_df.pivot(
        index="cluster",
        columns="character_cluster",
        values="deviation",
    )

    heatmap_data = heatmap_data.astype(float)

    # -------------------------
    # Plot
    # -------------------------
    plt.figure(figsize=(8, 6))

    sns.heatmap(
        heatmap_data,
        annot=True,
        fmt=".2f",
        center=0,          # IMPORTANT: zero baseline
        cmap="coolwarm",
        linewidths=0.5,
    )

    plt.title(
        "Audience Preference Deviations\n"
        "(Relative to Character-Cluster Average)"
    )

    plt.xlabel("Character Cluster")
    plt.ylabel("Audience Cluster")

    plt.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_block_zscore_heatmap(
    zscore_df: pd.DataFrame,
    output_path,
) -> None:

    pivot = zscore_df.pivot(
        index="cluster",
        columns="character_cluster",
        values="z_score",
    )

    pivot = pivot.astype(float)

    plt.figure(figsize=(8, 6))

    sns.heatmap(
        pivot,
        annot=True,
        fmt=".2f",
        center=0,
        cmap="coolwarm",
    )

    plt.title("Audience × Character Cluster Z-Scores")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_block_radar_profiles(
    deviation_df: pd.DataFrame,
    output_path,
) -> None:
    """
    Radar plot of signed structural bias profiles
    for each audience cluster.
    """

    pivot = deviation_df.pivot(
        index="cluster",
        columns="character_cluster",
        values="deviation",
    ).sort_index()

    labels = [f"Bloc {c}" for c in pivot.columns]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    angles = np.concatenate([angles, [angles[0]]])

    fig = plt.figure(figsize=(7, 7))
    ax = plt.subplot(111, polar=True)

    for cluster_id, row in pivot.iterrows():
        values = row.values
        values = np.concatenate([values, [values[0]]])

        ax.plot(angles, values, label=f"Audience {cluster_id}")
        ax.fill(angles, values, alpha=0.1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    ax.set_title("Signed Structural Bias Profiles")

    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved radar plot → {output_path}")
