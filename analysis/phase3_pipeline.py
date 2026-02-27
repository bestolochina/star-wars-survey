# analysis/phase3_pipeline.py

from __future__ import annotations

import pandas as pd

from src.paths import PHASE3_TABLES_DIR, PHASE3_FIGURES_DIR
from src.config import CHARACTER_RATING_COLUMNS

from analysis.transforms.matrix_builder import build_character_matrix
from analysis.metrics.correlation_structure import compute_character_correlation
from analysis.metrics.hierarchical_clustering import hierarchical_character_clustering
from analysis.metrics.pca_structure import compute_character_pca
from analysis.metrics.cluster_profiles import compute_cluster_profiles

from analysis.visualization.structure_plots import plot_correlation_heatmap
from analysis.visualization.clustering_plots import plot_character_dendrogram
from analysis.visualization.pca_plots import (
    plot_scree,
    plot_cumulative_variance,
    plot_character_pca_clusters,
)
from analysis.metrics.cluster_validation import (
    compute_silhouette,
    bootstrap_cluster_stability,
)
from analysis.metrics.imputation import knn_impute_matrix


# ==========================================================
# Utilities
# ==========================================================

def _ensure_dirs():
    PHASE3_TABLES_DIR.mkdir(parents=True, exist_ok=True)
    PHASE3_FIGURES_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================================
# 3.1.1 Correlation Structure
# ==========================================================

def step_311_correlation(matrix: pd.DataFrame) -> pd.DataFrame:
    print("\n=== 3.1.1 Correlation Structure ===")

    corr = compute_character_correlation(matrix)

    corr.to_csv(PHASE3_TABLES_DIR / "correlation_matrix.csv")

    plot_correlation_heatmap(
        corr,
        save_path=PHASE3_FIGURES_DIR / "correlation_heatmap.png",
    )

    return corr


# ==========================================================
# 3.1.2 Hierarchical Clustering
# ==========================================================

def step_312_clustering(matrix: pd.DataFrame) -> pd.DataFrame:
    print("\n=== 3.1.2 Hierarchical Clustering ===")

    Z, cluster_df, _ = hierarchical_character_clustering(
        matrix,
        linkage_method="average",
        n_clusters=3,
    )

    cluster_df.to_csv(
        PHASE3_TABLES_DIR / "character_cluster_assignments.csv",
        index=False,
    )

    plot_character_dendrogram(
        Z,
        labels=matrix.columns.tolist(),
        save_path=PHASE3_FIGURES_DIR / "character_dendrogram.png",
    )

    return cluster_df


# ==========================================================
# 3.1.3 PCA Structure
# ==========================================================

def step_313_pca(matrix: pd.DataFrame):

    print("\n=== 3.1.3 PCA Dimensionality Analysis ===")

    pca, explained_df, loadings_df = compute_character_pca(matrix)

    explained_df.to_csv(
        PHASE3_TABLES_DIR / "pca_explained_variance.csv",
        index=False,
    )

    loadings_df.to_csv(
        PHASE3_TABLES_DIR / "pca_loadings.csv"
    )

    plot_scree(
        explained_df,
        PHASE3_FIGURES_DIR / "pca_scree_plot.png",
    )

    plot_cumulative_variance(
        explained_df,
        PHASE3_FIGURES_DIR / "pca_cumulative_variance.png",
    )

    return pca, explained_df, loadings_df


# ==========================================================
# 3.1.4 Cluster Profiles
# ==========================================================

def step_314_cluster_profiles(
    matrix: pd.DataFrame,
    cluster_df: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 3.1.4 Cluster Mean Profiles ===")

    cluster_profile_df = compute_cluster_profiles(
        matrix,
        cluster_df)

    cluster_profile_df.to_csv(
        PHASE3_TABLES_DIR / "cluster_character_profiles.csv",
        index=False,
    )

    print(cluster_profile_df.to_string(index=False))

    return cluster_profile_df

def step_315_cluster_validation(
    matrix: pd.DataFrame,
    cluster_df: pd.DataFrame,
) -> None:

    print("\n=== 3.1.5 Cluster Validation ===")

    # -------------------------
    # KNN Imputation
    # -------------------------
    print("Running KNN imputation...")

    matrix_for_validation = knn_impute_matrix(
        matrix,
        n_neighbors=5,
        weights="distance",
    )

    # -------------------------
    # Silhouette
    # -------------------------
    sil = compute_silhouette(matrix_for_validation, cluster_df)

    print(f"Silhouette score: {sil:.3f}")

    # -------------------------
    # Bootstrap stability
    # -------------------------
    stability_df = bootstrap_cluster_stability(
        matrix_for_validation,
        cluster_df,
        hierarchical_character_clustering,
        n_bootstrap=100,
    )

    stability_df.to_csv(
        PHASE3_TABLES_DIR / "cluster_bootstrap_stability.csv",
        index=False,
    )

    print(
        f"Mean ARI: {stability_df['ARI'].mean():.3f}"
    )


# ==========================================================
# Pipeline Entry
# ==========================================================

def run_phase3(df: pd.DataFrame) -> None:

    print("=== PHASE 3: STRUCTURAL MODELING ===")

    _ensure_dirs()

    # ------------------------------------------------------
    # Build matrix
    # ------------------------------------------------------

    # standardized → structure
    matrix_std = build_character_matrix(
        df,
        respondent_id="respondent_id",
        character_columns=CHARACTER_RATING_COLUMNS,
        standardize=True,
    )

    # raw → interpretation
    matrix_raw = build_character_matrix(
        df,
        respondent_id="respondent_id",
        character_columns=CHARACTER_RATING_COLUMNS,
        standardize=False,
    )

    print(f"Matrix shape: {matrix_std.shape}")

    n_missing = matrix_std.isna().sum().sum()
    print(f"PCA missing values filled: {n_missing}")

    # ------------------------------------------------------
    # 3.1.1 Correlation
    # ------------------------------------------------------

    step_311_correlation(matrix_std)

    # ------------------------------------------------------
    # 3.1.2 Clustering
    # ------------------------------------------------------

    cluster_df = step_312_clustering(matrix_std)

    # ------------------------------------------------------
    # 3.1.3 PCA
    # ------------------------------------------------------

    _, _, loadings_df = step_313_pca(matrix_std)

    plot_character_pca_clusters(
        loadings_df,
        cluster_df,
        save_path_2d=PHASE3_FIGURES_DIR / "pca_character_clusters_pc12.png",
        save_path_13=PHASE3_FIGURES_DIR / "pca_character_clusters_pc13.png",
    )

    # ------------------------------------------------------
    # 3.1.4 Cluster Profiles
    # ------------------------------------------------------

    print("\n=== 3.1.4 Cluster Character Profiles ===")

    profile_df = step_314_cluster_profiles(
        matrix_raw,
        cluster_df,
    )

    # ------------------------------------------------------
    # 3.1.5 Cluster validation
    #         • Silhouette score
    #         • Bootstrap stability
    # ------------------------------------------------------

    step_315_cluster_validation(matrix_std, cluster_df)
