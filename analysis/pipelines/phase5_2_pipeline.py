# analysis/phase5_2_pipeline.py

from __future__ import annotations

import pandas as pd

from src.paths import PHASE4_TABLES_DIR, PHASE5_TABLES_DIR, PHASE5_FIGURES_DIR, PHASE3_TABLES_DIR
from analysis.metrics.audience_character_alignment import (
    build_audience_character_alignment_matrix,
    compute_cluster_character_rankings,
    compute_cluster_character_variance,
    compute_character_divergence,
    compute_cluster_character_ideology_distance,
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
# 5.2.1 Alignment Matrix
# ==========================================================

def step_521_alignment_matrix(
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
# 5.2.2 Cluster Character Rankings
# ==========================================================

def step_522_cluster_character_rankings(
    matrix: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.2.2 Cluster Character Rankings ===")

    rankings = compute_cluster_character_rankings(matrix)

    path = (
        PHASE5_TABLES_DIR
        / "alignment"
        / "cluster_character_rankings.csv"
    )

    rankings.to_csv(path)

    print(rankings.head().to_string())
    print(f"Saved → {path}")

    return rankings


# ==========================================================
# 5.2.3 Cluster Character Variance
# ==========================================================

def step_523_cluster_character_variance(
    matrix: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.2.3 Cluster Character Variance ===")

    variance = compute_cluster_character_variance(matrix)

    path = (
        PHASE5_TABLES_DIR
        / "alignment"
        / "cluster_character_variance.csv"
    )

    variance.to_csv(path, index=False)

    print(variance.head().to_string())
    print(f"Saved → {path}")

    return variance


# ==========================================================
# 5.2.4 Character Divergence
# ==========================================================

def step_524_character_divergence(
    matrix: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.2.4 Character Divergence ===")

    divergence = compute_character_divergence(matrix)

    path = (
        PHASE5_TABLES_DIR
        / "alignment"
        / "character_cluster_divergence.csv"
    )

    divergence.to_csv(path, index=False)

    print(divergence.head().to_string())
    print(f"Saved → {path}")

    return divergence


# ==========================================================
# 5.2.5 Ideological Distance
# ==========================================================

def step_525_ideology_distance(
    cluster_coords: pd.DataFrame,
    character_coords: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.2.5 Cluster–Character Ideological Distance ===")

    distance = compute_cluster_character_ideology_distance(
        cluster_coords,
        character_coords,
    )

    path = (
        PHASE5_TABLES_DIR
        / "alignment"
        / "cluster_character_ideology_distance.csv"
    )

    distance.to_csv(path, index=False)

    print(distance.head().to_string())
    print(f"Saved → {path}")

    return distance


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

    cluster_coords = pd.read_csv(
        polarization_dir / "cluster_ideology_coordinates.csv"
    )

    matrix = step_521_alignment_matrix(means)

    step_522_cluster_character_rankings(matrix)

    step_523_cluster_character_variance(matrix)

    step_524_character_divergence(matrix)

    step_525_ideology_distance(
        cluster_coords,
        character_coords,
    )