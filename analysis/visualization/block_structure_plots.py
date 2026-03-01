# analysis/visualization/block_structure_plots.py

from __future__ import annotations

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
