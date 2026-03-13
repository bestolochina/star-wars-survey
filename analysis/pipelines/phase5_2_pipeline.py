# analysis/pipelines/phase5_2_pipeline.py

from __future__ import annotations

import pandas as pd

from src.io_utils import load_clean_star_wars_with_audience_clusters
from src.paths import PHASE4_TABLES_DIR, PHASE5_TABLES_DIR
from src.config import CHARACTER_RATING_COLUMNS

from analysis.metrics.audience_character_alignment import (
    build_audience_character_alignment_matrix,
    compute_audience_cluster_character_rankings,
    compute_character_evaluation_variance_across_audience_clusters,
    compute_character_divergence_across_audience_clusters,
    compute_audience_cluster_character_ideology_distance,
    compute_character_segmentation_strength_across_audience_clusters,
)


# ==========================================================
# Utilities
# ==========================================================

def _ensure_dirs() -> None:

    (PHASE5_TABLES_DIR / "alignment").mkdir(
        parents=True,
        exist_ok=True,
    )


# ==========================================================
# 5.2.1 Audience–Character Alignment Matrix
# ==========================================================

def step_521_audience_character_alignment_matrix(
    means: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.2.1 Audience–Character Alignment Matrix ===")

    matrix = build_audience_character_alignment_matrix(means)

    path = (
        PHASE5_TABLES_DIR
        / "alignment"
        / "audience_character_alignment_matrix.csv"
    )

    matrix.to_csv(path)

    print(matrix.to_string())
    print(f"Saved → {path}")

    return matrix


# ==========================================================
# 5.2.2 Audience Cluster Character Rankings
# ==========================================================

def step_522_audience_cluster_character_rankings(
    matrix: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.2.2 Audience Cluster Character Rankings ===")

    rankings = compute_audience_cluster_character_rankings(matrix)

    path = (
        PHASE5_TABLES_DIR
        / "alignment"
        / "audience_cluster_character_rankings.csv"
    )

    rankings.to_csv(path)

    print(rankings.head().to_string())
    print(f"Saved → {path}")

    return rankings


# ==========================================================
# 5.2.3 Character Evaluation Variance Across Audience Clusters
# ==========================================================

def step_523_character_evaluation_variance_across_audience_clusters(
    matrix: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.2.3 Character Evaluation Variance Across Audience Clusters ===")

    variance = compute_character_evaluation_variance_across_audience_clusters(matrix)

    path = (
        PHASE5_TABLES_DIR
        / "alignment"
        / "character_evaluation_variance_across_audience_clusters.csv"
    )

    variance.to_csv(path, index=False)

    print(variance.head().to_string())
    print(f"Saved → {path}")

    return variance


# ==========================================================
# 5.2.4 Character Divergence Across Audience Clusters
# ==========================================================

def step_524_character_divergence_across_audience_clusters(
    matrix: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.2.4 Character Divergence Across Audience Clusters ===")

    divergence = compute_character_divergence_across_audience_clusters(matrix)

    path = (
        PHASE5_TABLES_DIR
        / "alignment"
        / "character_divergence_across_audience_clusters.csv"
    )

    divergence.to_csv(path, index=False)

    print(divergence.head().to_string())
    print(f"Saved → {path}")

    return divergence


# ==========================================================
# 5.2.5 Audience Cluster–Character Ideological Distance
# ==========================================================

def step_525_audience_cluster_character_ideology_distance(
    audience_cluster_coords: pd.DataFrame,
    character_coords: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.2.5 Audience Cluster–Character Ideological Distance ===")

    distance = compute_audience_cluster_character_ideology_distance(
        audience_cluster_coords,
        character_coords,
    )

    path = (
        PHASE5_TABLES_DIR
        / "alignment"
        / "audience_cluster_character_ideology_distance.csv"
    )

    distance.to_csv(path, index=False)

    print(distance.head().to_string())
    print(f"Saved → {path}")

    return distance


# ==========================================================
# 5.2.6 Character Segmentation Strength Across Audience Clusters
# ==========================================================

def step_526_character_segmentation_strength_across_audience_clusters() -> pd.DataFrame:

    print("\n=== 5.2.6 Character Segmentation Strength Across Audience Clusters ===")

    respondent_cluster_df = load_clean_star_wars_with_audience_clusters()

    segmentation = compute_character_segmentation_strength_across_audience_clusters(
        respondent_cluster_df,
        CHARACTER_RATING_COLUMNS,
    )

    path = (
        PHASE5_TABLES_DIR
        / "alignment"
        / "character_segmentation_strength_across_audience_clusters.csv"
    )

    segmentation.to_csv(path, index=False)

    print(segmentation.head().to_string())
    print(f"Saved → {path}")

    return segmentation


# ==========================================================
# Pipeline Entry
# ==========================================================

def run_phase5_2() -> None:

    print("=== PHASE 5.2: AUDIENCE–CHARACTER INTERACTION ===")

    _ensure_dirs()

    polarization_dir = PHASE4_TABLES_DIR / "polarization"

    means = pd.read_csv(
        polarization_dir / "character_cluster_means.csv"
    )

    character_coords = pd.read_csv(
        polarization_dir / "character_ideology_coordinates.csv"
    )

    audience_cluster_coords = pd.read_csv(
        polarization_dir / "audience_cluster_ideology_coordinates.csv"
    )

    matrix = step_521_audience_character_alignment_matrix(means)

    step_522_audience_cluster_character_rankings(matrix)

    step_523_character_evaluation_variance_across_audience_clusters(matrix)

    step_524_character_divergence_across_audience_clusters(matrix)

    step_525_audience_cluster_character_ideology_distance(
        audience_cluster_coords,
        character_coords,
    )

    step_526_character_segmentation_strength_across_audience_clusters()