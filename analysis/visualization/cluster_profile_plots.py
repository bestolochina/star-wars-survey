# analysis/visualization/cluster_profile_plots.py

from __future__ import annotations

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ==========================================================
# Cluster Profile Heatmap
# ==========================================================

def plot_cluster_profile_heatmap(
    profile_df: pd.DataFrame,
    save_path,
) -> None:
    """
    Plot heatmap of mean character ratings per respondent cluster.

    Parameters
    ----------
    profile_df :
        LONG format:
            character | cluster | mean_rating

    save_path :
        Output image path
    """

    # ------------------------------------------------------
    # Pivot to matrix form
    # ------------------------------------------------------
    heatmap_df = profile_df.pivot(
        index="character",
        columns="cluster",
        values="mean_rating",
    )

    # ------------------------------------------------------
    # Sort characters alphabetically (stable baseline)
    # ------------------------------------------------------
    heatmap_df = heatmap_df.sort_index()

    # ------------------------------------------------------
    # Plot
    # ------------------------------------------------------
    plt.figure(figsize=(8, 10))

    ax = sns.heatmap(
        heatmap_df,
        annot=True,
        fmt=".2f",
        linewidths=0.5,
        cmap="coolwarm",
        center=3.0,  # neutral rating midpoint
        cbar_kws={"label": "Mean Rating"},
    )

    # ------------------------------------------------------
    # Labels
    # ------------------------------------------------------
    ax.set_title(
        "Cluster Mean Character Ratings",
        fontsize=14,
        pad=12,
    )

    ax.set_xlabel("Audience Cluster")
    ax.set_ylabel("Character")

    plt.tight_layout()

    # ------------------------------------------------------
    # Save
    # ------------------------------------------------------
    plt.savefig(save_path, dpi=300)
    plt.close()

    print(f"Saved heatmap → {save_path}")