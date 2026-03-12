# analysis/visualization/cluster_profile_plots.py

from __future__ import annotations

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from src.config import AUDIENCE_CLUSTER_LABELS


# ==========================================================
# Cluster Profile Heatmap
# ==========================================================

def plot_cluster_profile_heatmap(
    profile_df: pd.DataFrame,
    save_path,
) -> None:

    # -----------------------------------
    # LONG → WIDE (required for heatmap)
    # -----------------------------------
    heatmap_df = profile_df.pivot(
        index="character",
        columns="audience_cluster",
        values="mean_rating",
    )

    # ensure numeric dtype
    heatmap_df = heatmap_df.astype(float)

    # optional: sort clusters left→right
    heatmap_df = heatmap_df.sort_index(axis=1)

    # -----------------------------------
    # Plot
    # -----------------------------------
    plt.figure(figsize=(10, 8))

    ax = sns.heatmap(
        heatmap_df,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        vmin=1,
        vmax=5,
        linewidths=0.5,
    )

    plt.title("Character Ratings by Audience Segment")
    plt.tight_layout()

    plt.savefig(save_path, dpi=300)
    plt.close()

    print(f"Saved heatmap → {save_path}")


# ----------------------------------------------------------
# Deviation Heatmap
# ----------------------------------------------------------

def plot_deviation_heatmap(
    deviations: pd.DataFrame,
    save_path,
) -> None:
    """
    Heatmap of cluster deviations from overall mean.

    Expected columns:
        character
        audience_cluster
        character_deviation
    """

    pivot = deviations.pivot(
        index="character",
        columns="audience_cluster",
        values="character_deviation",
    )

    # ensure numeric dtype (prevents seaborn crash)
    pivot = pivot.astype(float)

    plt.figure(figsize=(8, 10))

    ax = sns.heatmap(
        pivot,
        center=0,
        cmap="coolwarm",
        annot=True,
        fmt=".2f",
        linewidths=0.5,
        cbar_kws={"label": "Deviation from Overall Mean"},
    )

    ax.set_title("Audience Character Preference Deviations")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()

    print(f"Saved deviation heatmap → {save_path}")


# ----------------------------------------------------------
# Cluster Radar Plots
# ----------------------------------------------------------

def plot_cluster_radar_plots(
    deviations: pd.DataFrame,
    save_path,
) -> None:
    """
    Radar chart comparing audience_clusters using deviations.
    """

    pivot = deviations.pivot(
        index="character",
        columns="audience_cluster",
        values="character_deviation",
    ).astype(float)

    characters = pivot.index.tolist()
    clusters = pivot.columns.tolist()

    num_vars = len(characters)

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)
    angles = np.concatenate([angles, [angles[0]]])

    fig, ax = plt.subplots(
        figsize=(8, 8),
        subplot_kw=dict(polar=True),
    )

    for audience_cluster in clusters:
        values = pivot[audience_cluster].values
        values = np.concatenate([values, [values[0]]])

        ax.plot(angles, values, label=AUDIENCE_CLUSTER_LABELS.get(
            audience_cluster,
            f"Cluster {audience_cluster}"
            ))
        ax.fill(angles, values, alpha=0.1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(characters, fontsize=8)

    ax.set_title("Audience Preference Signatures (Character Deviation Radar)")
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()

    print(f"Saved radar plots → {save_path}")