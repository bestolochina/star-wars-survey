# analysis/pipelines/phase3_pipeline.py

from __future__ import annotations

import pandas as pd

from src.paths import PHASE3_TABLES_DIR, PHASE3_FIGURES_DIR
from src.config import CHARACTER_RATING_COLUMNS

from analysis.metrics.character_audience_structure_validation import (
    compute_character_correlation,
    compute_character_pca,
    hierarchical_character_clustering,
    compute_silhouette,
    bootstrap_cluster_stability,
    compute_cluster_profiles,
    hierarchical_respondent_clustering,
    compute_audience_cluster_centroids,
)
from analysis.visualization.character_audience_structure_visualization import (
    plot_correlation_heatmap,
    plot_character_dendrogram,
    plot_scree,
    plot_cumulative_variance,
    plot_character_pca_clusters,
)

from analysis.transforms.matrix_builder import build_character_matrix
from analysis.transforms.imputation import knn_impute_matrix


# ==========================================================
# Utilities
# ==========================================================

def _ensure_dirs():
    PHASE3_TABLES_DIR.mkdir(parents=True, exist_ok=True)
    PHASE3_FIGURES_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================================
# 3.1.1 Character Correlation
# ==========================================================

def step_311_character_correlation(matrix: pd.DataFrame) -> pd.DataFrame:
    print("\n=== 3.1.1 Correlation Structure ===")

    table_path = PHASE3_TABLES_DIR / "correlation_matrix.csv"
    plot_path = PHASE3_FIGURES_DIR / "correlation_heatmap.png"

    corr = compute_character_correlation(matrix)

    corr.to_csv(PHASE3_TABLES_DIR / "correlation_matrix.csv")

    print(f"Saved → {table_path}")

    plot_correlation_heatmap(
        corr,
        save_path=plot_path,
    )

    print(f"Saved → {plot_path}")

    return corr


# ==========================================================
# 3.1.2 Character Clustering
# ==========================================================

def step_312_character_clustering(matrix: pd.DataFrame, n_clusters: int) -> pd.DataFrame:
    print("\n=== 3.1.2 Hierarchical Clustering ===")

    table_path = PHASE3_TABLES_DIR / "character_cluster_assignments.csv"
    plot_path = PHASE3_FIGURES_DIR / "character_dendrogram.png"

    Z, cluster_df, _ = hierarchical_character_clustering(
        matrix,
        linkage_method="average",
        n_clusters=n_clusters,
    )

    cluster_df.to_csv(
        table_path,
        index=False,
    )

    print(f"Saved → {table_path}")

    plot_character_dendrogram(
        Z,
        labels=matrix.columns.tolist(),
        save_path=plot_path,
    )

    print(f"Saved → {plot_path}")

    return cluster_df


# ==========================================================
# 3.1.3 PCA Structure
# ==========================================================

def step_313_character_pca(matrix: pd.DataFrame):

    print("\n=== 3.1.3 PCA Dimensionality Analysis ===")

    explained_path = PHASE3_TABLES_DIR / "pca_explained_variance.csv"
    loadings_path = PHASE3_TABLES_DIR / "pca_loadings.csv"

    scree_path = PHASE3_FIGURES_DIR / "pca_scree_plot.png"
    cumulative_path = PHASE3_FIGURES_DIR / "pca_cumulative_variance.png"

    pca, explained_df, loadings_df = compute_character_pca(matrix)

    explained_df.to_csv(
        explained_path,
        index=False,
    )

    print(f"Saved → {explained_path}")

    loadings_df.to_csv(
        loadings_path,
    )

    print(f"Saved → {loadings_path}")

    plot_scree(
        explained_df,
        scree_path,
    )

    print(f"Saved → {scree_path}")

    plot_cumulative_variance(
        explained_df,
        cumulative_path,
    )

    print(f"Saved → {cumulative_path}")

    return pca, explained_df, loadings_df


# ==========================================================
# 3.1.4 Character Cluster Profiles
# ==========================================================

def step_314_character_cluster_profiles(
    matrix: pd.DataFrame,
    cluster_df: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 3.1.4 Cluster Mean Profiles ===")

    table_path = PHASE3_TABLES_DIR / "cluster_character_profiles.csv"

    cluster_profile_df = compute_cluster_profiles(
        matrix,
        cluster_df
    )

    cluster_profile_df.to_csv(
        table_path,
        index=False,
    )

    print(f"Saved → {table_path}")

    print(cluster_profile_df.to_string(index=False))

    return cluster_profile_df

# ==========================================================
# 3.2.1 Audience Clustering
# ==========================================================

def step_321_audience_clustering(
    matrix: pd.DataFrame,
    n_clusters: int,
) -> pd.DataFrame:

    print("\n=== 3.2.1 Audience Clustering ===")

    table_path = PHASE3_TABLES_DIR / "respondent_cluster_assignments.csv"

    Z, respondent_cluster_df, _ = (
        hierarchical_respondent_clustering(
            matrix,
            n_clusters=n_clusters,
        )
    )

    respondent_cluster_df.to_csv(
        table_path,
        index=False,
    )

    print(f"Saved → {table_path}")

    print(
        respondent_cluster_df["audience_cluster"]
        .value_counts()
        .sort_index()
    )

    return respondent_cluster_df


# ==========================================================
# 3.2.2 Audience Cluster Ideological Centroids
# ==========================================================

def step_322_audience_cluster_centroids(
        matrix: pd.DataFrame,
        pca,
        respondent_clusters: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 3.2.2 Audience Cluster Ideological Centroids ===")

    path = PHASE3_TABLES_DIR / "audience_cluster_centroids.csv"

    centroids = compute_audience_cluster_centroids(
        matrix,
        pca,
        respondent_clusters,
    )

    centroids.to_csv(
        path,
        index=False,
    )

    print(centroids.to_string(index=False))
    print(f"Saved → {path}")

    return centroids


# ==========================================================
# 3.3.1 Cluster Validation
# ==========================================================

def step_331_cluster_validation(
    matrix: pd.DataFrame,
    cluster_df: pd.DataFrame,
) -> None:

    print("\n=== 3.3.1 Cluster Validation ===")

    table_path = PHASE3_TABLES_DIR / "cluster_bootstrap_stability.csv"

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

    sil = compute_silhouette(
        matrix_for_validation,
        cluster_df
    )

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
        table_path,
        index=False,
    )

    print(f"Saved → {table_path}")

    print(
        f"Mean ARI: {stability_df['ARI'].mean():.3f}"
    )


# ==========================================================
# Pipeline Entry
# ==========================================================

def run_phase3(df: pd.DataFrame) -> None:

    print("=== PHASE 3: STRUCTURAL MODELING ===")

    _ensure_dirs()

    # ------------------------------------------------
    # Build matrices
    # ------------------------------------------------

    matrix_std = build_character_matrix(
        df,
        respondent_id="respondent_id",
        character_columns=CHARACTER_RATING_COLUMNS,
        standardize=True,
    )

    matrix_raw = build_character_matrix(
        df,
        respondent_id="respondent_id",
        character_columns=CHARACTER_RATING_COLUMNS,
        standardize=False,
    )

    print(f"Matrix shape: {matrix_std.shape}")

    # ------------------------------------------------
    # 3.1 Character structure
    # ------------------------------------------------

    corr = step_311_character_correlation(matrix_std)

    character_clusters = step_312_character_clustering(
        matrix_std,
        n_clusters=3,
    )

    pca, explained_df, loadings_df = step_313_character_pca(matrix_std)

    step_314_character_cluster_profiles(
        matrix_raw,
        character_clusters,
    )

    # ------------------------------------------------
    # 3.2 Audience segmentation
    # ------------------------------------------------

    audience_clusters = step_321_audience_clustering(
        matrix_std,
        n_clusters=3,
    )

    step_322_audience_cluster_centroids(
        matrix_std,
        pca,
        audience_clusters,
    )

    # ------------------------------------------------
    # 3.3 Structural validation
    # ------------------------------------------------

    step_331_cluster_validation(
        matrix_std,
        character_clusters,
    )

    # ------------------------------------------------
    # PCA visualisation
    # ------------------------------------------------

    plot_character_pca_clusters(
        loadings_df,
        character_clusters,
        save_path_2d=PHASE3_FIGURES_DIR / "pca_character_clusters_pc12.png",
        save_path_13=PHASE3_FIGURES_DIR / "pca_character_clusters_pc13.png",
    )