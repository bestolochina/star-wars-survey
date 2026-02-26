# analysis/phase3_pipeline.py

from __future__ import annotations

import pandas as pd

from src.paths import PHASE3_TABLES_DIR, PHASE3_FIGURES_DIR
from src.config import CHARACTER_RATING_COLUMNS

from analysis.transforms.matrix_builder import (
    build_character_matrix,
)
from analysis.metrics.correlation_structure import (
    compute_character_correlation,
)
from analysis.visualization.structure_plots import (
    plot_correlation_heatmap,
)
from analysis.metrics.hierarchical_clustering import (
    hierarchical_character_clustering,
)
from analysis.visualization.clustering_plots import (
    plot_character_dendrogram,
)
from analysis.metrics.pca_structure import (
    compute_character_pca,
)
from analysis.visualization.pca_plots import (
    plot_scree,
    plot_cumulative_variance,
    plot_character_pca_clusters,
)


# ==========================================================
# PHASE 3 — STEP 3.1.1
# ==========================================================

def run_phase3_correlation(
    matrix: pd.DataFrame,
    *,
    tables_dir,
    figures_dir,
) -> pd.DataFrame:

    # ------------------------------------------------------
    # Correlation
    # ------------------------------------------------------

    corr = compute_character_correlation(matrix)

    # save table
    corr.to_csv(
        tables_dir / "correlation_matrix.csv"
    )

    # plot
    plot_correlation_heatmap(
        corr,
        save_path=figures_dir / "correlation_heatmap.png",
    )

    print("Correlation structure saved.")

    return corr

# ==========================================================
# PHASE 3 — STEP 3.1.2
# ==========================================================

def run_character_hierarchical_clustering(
    matrix,
    *,
    tables_dir,
    figures_dir,
) -> pd.DataFrame:

    print("\n=== 3.1.2 Hierarchical Clustering ===")

    Z, cluster_df, distance_df = hierarchical_character_clustering(
        matrix,
        linkage_method="average",
        n_clusters=3,
    )

    # save assignments
    cluster_df.to_csv(
        tables_dir / "character_cluster_assignments.csv",
        index=False,
    )

    # plot dendrogram
    plot_character_dendrogram(
        Z,
        labels=matrix.columns.tolist(),
        save_path=figures_dir / "character_dendrogram.png",
    )

    print("Hierarchical clustering complete.")

    return cluster_df

# ==========================================================
# PHASE 3 — STEP 3.1.3
# ==========================================================

def run_character_pca(
    matrix,
    cluster_df,
    *,
    tables_dir,
    figures_dir,
) -> None:

    print("\n=== 3.1.3 PCA Dimensionality Analysis ===")

    n_missing = matrix.isna().sum().sum()
    print(f"PCA missing values filled: {n_missing}")

    pca, explained_df, loadings_df = compute_character_pca(matrix)

    # save tables
    explained_df.to_csv(
        tables_dir / "pca_explained_variance.csv",
        index=False,
    )

    loadings_df.to_csv(
        tables_dir / "pca_loadings.csv"
    )

    # plots
    plot_scree(
        explained_df,
        figures_dir / "pca_scree_plot.png",
    )

    plot_cumulative_variance(
        explained_df,
        figures_dir / "pca_cumulative_variance.png",
    )

    print("PCA analysis complete.")

    plot_character_pca_clusters(
        loadings_df,
        cluster_df,
        save_path_2d=figures_dir / "pca_character_clusters_pc12.png",
        save_path_13=figures_dir / "pca_character_clusters_pc13.png",
    )

    print("PCA cluster visualization saved.")


def run_phase3(df: pd.DataFrame) -> None:

    print("=== PHASE 3: STRUCTURAL MODELING ===")

    print("\n=== PHASE 3 — CHARACTER STRUCTURE ===")

    tables_dir = PHASE3_TABLES_DIR
    figures_dir = PHASE3_FIGURES_DIR

    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------
    # Build matrix
    # ------------------------------------------------------

    matrix = build_character_matrix(
        df,
        respondent_id="respondent_id",  # change if needed
        character_columns=CHARACTER_RATING_COLUMNS,
        standardize=True,
    )

    print(f"Matrix shape: {matrix.shape}")

    corr = run_phase3_correlation(matrix, tables_dir=tables_dir, figures_dir=figures_dir)

    print("\nPhase 3 step 3.1.1 complete.\n")

    cluster_df = run_character_hierarchical_clustering(
        matrix,
        tables_dir=tables_dir,
        figures_dir=figures_dir,
    )

    run_character_pca(
        matrix,
        cluster_df,
        tables_dir=tables_dir,
        figures_dir=figures_dir,
    )
