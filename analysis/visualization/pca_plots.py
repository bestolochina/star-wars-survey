# analysis/visualization/pca_plots.py

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


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
    """
    Plot characters in PCA space colored by hierarchical cluster.
    """

    # ------------------------------------------
    # Merge PCA loadings + clusters
    # ------------------------------------------

    plot_df = (
        loadings_df
        .reset_index()
        .rename(columns={"index": "character"})
        .merge(cluster_df, on="character")
    )

    # ------------------------------------------
    # PC1 vs PC2
    # ------------------------------------------

    plt.figure(figsize=(8, 6))

    for cluster_id, group in plot_df.groupby("cluster"):
        plt.scatter(
            group["PC1"],
            group["PC2"],
            label=f"Cluster {cluster_id}",
        )

        # labels
        for _, row in group.iterrows():
            plt.text(
                row["PC1"],
                row["PC2"],
                row["character"],
                fontsize=9,
            )

    plt.axhline(0)
    plt.axvline(0)

    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("Characters in PCA Space (PC1 vs PC2)")
    plt.legend()
    plt.tight_layout()

    plt.savefig(save_path_2d, dpi=150)
    plt.close()

    # ------------------------------------------
    # Optional PC1 vs PC3
    # ------------------------------------------

    if save_path_13 is not None:

        plt.figure(figsize=(8, 6))

        for cluster_id, group in plot_df.groupby("cluster"):
            plt.scatter(
                group["PC1"],
                group["PC3"],
                label=f"Cluster {cluster_id}",
            )

            for _, row in group.iterrows():
                plt.text(
                    row["PC1"],
                    row["PC3"],
                    row["character"],
                    fontsize=9,
                )

        plt.axhline(0)
        plt.axvline(0)

        plt.xlabel("PC1")
        plt.ylabel("PC3")
        plt.title("Characters in PCA Space (PC1 vs PC3)")
        plt.legend()
        plt.tight_layout()

        plt.savefig(save_path_13, dpi=150)
        plt.close()