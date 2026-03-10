# analysis/visualization/character_audience_structure_visualization.py

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
from scipy.cluster.hierarchy import dendrogram


def plot_correlation_heatmap(
    corr: pd.DataFrame,
    save_path,
) -> None:

    fig, ax = plt.subplots(figsize=(10, 8))

    im = ax.imshow(
        corr.values,
        vmin=-1,
        vmax=1,
        cmap="coolwarm",
    )

    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))

    ax.set_xticklabels(corr.columns, rotation=90)
    ax.set_yticklabels(corr.columns)

    fig.colorbar(im, ax=ax)

    ax.set_title("Character Rating Correlation")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()


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


def plot_scree(
    explained_df: pd.DataFrame,
    save_path,
) -> None:

    plt.figure(figsize=(8, 5))

    plt.plot(
        explained_df["component"],
        explained_df["eigenvalue"],
        marker="o",
    )

    plt.xlabel("Principal Component")
    plt.ylabel("Eigenvalue")
    plt.title("Scree Plot")

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()


def plot_cumulative_variance(
    explained_df: pd.DataFrame,
    save_path,
) -> None:

    plt.figure(figsize=(8, 5))

    plt.plot(
        explained_df["component"],
        explained_df["cumulative_variance"],
        marker="o",
    )

    plt.axhline(0.80, linestyle="--")
    plt.axhline(0.90, linestyle="--")

    plt.xlabel("Principal Component")
    plt.ylabel("Cumulative Variance Explained")
    plt.title("Cumulative Variance Explained")

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()


def plot_character_pca_clusters(
    loadings_df: pd.DataFrame,
    cluster_df: pd.DataFrame,
    *,
    save_path_2d,
    save_path_13=None,
) -> None:

    plot_df = (
        loadings_df
        .rename_axis("character")
        .reset_index()
        .merge(cluster_df, on="character")
    )

    def _plot(x, y, path, title):

        plt.figure(figsize=(8, 6))

        for cluster_id, group in plot_df.groupby("character_cluster"):
            plt.scatter(group[x], group[y], label=f"Cluster {cluster_id}")

            for _, row in group.iterrows():
                plt.text(row[x], row[y], row["character"], fontsize=9)

        plt.axhline(0)
        plt.axvline(0)

        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(title)
        plt.legend()

        plt.tight_layout()
        plt.savefig(path, dpi=150)
        plt.close()

    _plot("PC1", "PC2", save_path_2d, "Characters in PCA Space (PC1 vs PC2)")

    if save_path_13 is not None:
        _plot("PC1", "PC3", save_path_13, "Characters in PCA Space (PC1 vs PC3)")