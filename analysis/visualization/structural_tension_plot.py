# analysis/visualization/structural_tension_plot.py

from __future__ import annotations
import matplotlib.pyplot as plt
import pandas as pd


def plot_structural_tension(
    tension_df: pd.DataFrame,
    output_path,
) -> None:
    """
    Bar plot of narrative tension by character cluster.
    """

    fig, ax = plt.subplots(figsize=(7, 5))

    ax.bar(
        tension_df["character_cluster"].astype(str),
        tension_df["tension_variance"],
    )

    ax.set_xlabel("Character Cluster")
    ax.set_ylabel("Narrative Tension (Variance)")
    ax.set_title("Structural Narrative Tension")

    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved tension plot → {output_path}")
