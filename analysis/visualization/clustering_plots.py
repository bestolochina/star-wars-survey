# analysis/visualization/clustering_plots.py

from __future__ import annotations

import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram


def plot_character_dendrogram(
    linkage_matrix,
    labels,
    *,
    save_path,
) -> None:

    plt.figure(figsize=(12, 6))

    dendrogram(
        linkage_matrix,
        labels=labels,
        leaf_rotation=90,
        leaf_font_size=9,
    )

    plt.title("Character Hierarchical Clustering")
    plt.ylabel("Correlation Distance (1 − r)")

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()