# analysis/visualization/phase5_4_plots.py

from __future__ import annotations

import pandas as pd
import matplotlib.pyplot as plt


# ==========================================================
# Audience–Character Ideology Alignment Map
# ==========================================================

def plot_audience_character_ideology_alignment_map(
        character_coords: pd.DataFrame,
        cluster_coords: pd.DataFrame,
        save_path,
) -> None:

    fig, ax = plt.subplots(figsize=(10, 8))

    # Characters
    ax.scatter(
        character_coords["ideology_axis_1"],
        character_coords["ideology_axis_2"],
        s=120,
        alpha=0.9,
        label="Characters",
    )

    for _, row in character_coords.iterrows():
        ax.annotate(
            row["character"],
            (row["ideology_axis_1"], row["ideology_axis_2"]),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=9,
        )

    # Audience clusters
    ax.scatter(
        cluster_coords["PC1"],
        cluster_coords["PC2"],
        s=200,
        marker="X",
        label="Audience Clusters",
    )

    for _, row in cluster_coords.iterrows():
        ax.text(
            row["PC1"],
            row["PC2"],
            f"Cluster {int(row['audience_cluster'])}",
            fontsize=11,
            fontweight="bold",
        )

    ax.axhline(0)
    ax.axvline(0)

    ax.set_title("Audience–Character Ideological Alignment Map")
    ax.set_xlabel("Ideological Axis 1")
    ax.set_ylabel("Ideological Axis 2")

    ax.legend()

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
