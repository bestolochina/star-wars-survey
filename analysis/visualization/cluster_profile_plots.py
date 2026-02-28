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

    import matplotlib.pyplot as plt
    import seaborn as sns

    # -----------------------------------
    # LONG → WIDE (required for heatmap)
    # -----------------------------------
    heatmap_df = profile_df.pivot(
        index="character",
        columns="cluster",
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

    plt.title("Audience Cluster Mean Ratings")
    plt.tight_layout()

    plt.savefig(save_path, dpi=300)
    plt.close()

    print(f"Saved heatmap → {save_path}")