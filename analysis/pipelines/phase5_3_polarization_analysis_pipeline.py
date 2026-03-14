# analysis/pipelines/phase5_3_polarization_analysis_pipeline.py

from __future__ import annotations

import pandas as pd

from src.paths import PHASE5_TABLES_DIR, PHASE5_FIGURES_DIR

from analysis.metrics.polarization_analysis import (
    compute_cluster_ideological_distance_matrix,
    compute_cluster_ideological_polarization_metrics,
    compute_character_polarization_summary,
    compute_narrative_polarization_index,
    compute_character_polarization_driver_decomposition,
)

from analysis.visualization.polarization_plots import (
    plot_cluster_ideological_distance_heatmap,
    plot_character_polarization_ranking,
)


# ==========================================================
# Utilities
# ==========================================================

def _ensure_dirs() -> None:

    (PHASE5_TABLES_DIR / "polarization").mkdir(
        parents=True,
        exist_ok=True,
    )

    (PHASE5_FIGURES_DIR / "polarization").mkdir(
        parents=True,
        exist_ok=True,
    )


# ==========================================================
# 5.3.1 Cluster Ideological Distance Matrix
# ==========================================================

def step_531_cluster_ideological_distance_matrix(
    cluster_ideology_index: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.3.1 Cluster Ideological Distance Matrix ===")

    df = compute_cluster_ideological_distance_matrix(
        cluster_ideology_index
    )

    path = (
        PHASE5_TABLES_DIR
        / "polarization"
        / "cluster_ideological_distance_matrix.csv"
    )

    df.to_csv(path, index=False)

    print(df.to_string())
    print(f"Saved → {path}")

    return df


# ==========================================================
# 5.3.2 Cluster Ideological Polarization Metrics
# ==========================================================

def step_532_cluster_ideological_polarization_metrics(
    cluster_ideology_index: pd.DataFrame,
    engagement_index: pd.DataFrame,
    positivity_bias: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.3.2 Cluster Ideological Polarization Metrics ===")

    df = compute_cluster_ideological_polarization_metrics(
        cluster_ideology_index,
        engagement_index,
        positivity_bias,
    )

    path = (
        PHASE5_TABLES_DIR
        / "polarization"
        / "cluster_ideological_polarization_metrics.csv"
    )

    df.to_csv(path, index=False)

    print(df.to_string())
    print(f"Saved → {path}")

    return df


# ==========================================================
# 5.3.3 Character Polarization Summary
# ==========================================================

def step_533_character_polarization_summary(
    alignment_matrix: pd.DataFrame,
) -> pd.DataFrame:


    print("\n=== 5.3.3 Character Polarization Summary ===")

    df = compute_character_polarization_summary(
        alignment_matrix
    )

    path = (
        PHASE5_TABLES_DIR
        / "polarization"
        / "character_polarization_summary.csv"
    )

    df.to_csv(path, index=False)

    print(df.to_string())
    print(f"Saved → {path}")

    return df


# ==========================================================
# 5.3.4 Narrative Polarization Index
# ==========================================================

def step_534_narrative_polarization_index(
    character_summary: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.3.4 Narrative Polarization Index ===")

    df = compute_narrative_polarization_index(
        character_summary
    )

    path = (
        PHASE5_TABLES_DIR
        / "polarization"
        / "narrative_polarization_index.csv"
    )

    df.to_csv(path, index=False)

    print(df.to_string())
    print(f"Saved → {path}")

    return df


# ==========================================================
# 5.3.5 Cluster Ideological Distance Heatmap
# ==========================================================

def step_535_cluster_ideological_distance_heatmap(
    distance_df: pd.DataFrame,
) -> None:

    print("\n=== 5.3.5 Cluster Ideological Distance Heatmap ===")

    path = (
        PHASE5_FIGURES_DIR
        / "polarization"
        / "cluster_ideological_distance_heatmap.png"
    )

    plot_cluster_ideological_distance_heatmap(
        distance_df,
        path,
    )

    print(f"Saved → {path}")


# ==========================================================
# 5.3.6 Character Polarization Ranking Plot
# ==========================================================

def step_536_character_polarization_ranking_plot(
    character_summary: pd.DataFrame,
) -> None:

    print("\n=== 5.3.6 Character Polarization Ranking Plot ===")

    path = (
        PHASE5_FIGURES_DIR
        / "polarization"
        / "character_polarization_ranking.png"
    )

    plot_character_polarization_ranking(
        character_summary,
        path,
    )

    print(f"Saved → {path}")


# ==========================================================
# 5.3.7 Character Polarization Driver Decomposition
# ==========================================================

def step_537_character_polarization_driver_decomposition(
    alignment_matrix: pd.DataFrame,
    cluster_ideology_index: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.3.7 Character Polarization Driver Decomposition ===")

    df = compute_character_polarization_driver_decomposition(
        alignment_matrix=alignment_matrix,
        cluster_ideology_index=cluster_ideology_index,
    )

    path = (
        PHASE5_TABLES_DIR
        / "polarization"
        / "character_polarization_driver_decomposition.csv"
    )

    df.to_csv(path, index=False)

    print(df.to_string())
    print(f"Saved → {path}")

    return df


# ==========================================================
# Pipeline Entry
# ==========================================================

def run_phase5_3() -> None:

    print("=== PHASE 5.3: POLARIZATION ANALYSIS ===")

    _ensure_dirs()

    alignment_dir = PHASE5_TABLES_DIR / "alignment"

    alignment_matrix = pd.read_csv(
        alignment_dir
        / "audience_character_alignment_matrix.csv",
        index_col=0,
    )

    cluster_ideology_index = pd.read_csv(
        alignment_dir / "cluster_ideology_index.csv"
    )

    engagement_index = pd.read_csv(
        alignment_dir / "audience_cluster_engagement_index.csv"
    )

    positivity_bias = pd.read_csv(
        alignment_dir / "cluster_positivity_bias.csv"
    )

    cluster_distance_matrix = step_531_cluster_ideological_distance_matrix(
        cluster_ideology_index
    )

    step_532_cluster_ideological_polarization_metrics(
        cluster_ideology_index,
        engagement_index,
        positivity_bias,
    )

    character_summary = step_533_character_polarization_summary(
        alignment_matrix
    )

    step_534_narrative_polarization_index(
        character_summary
    )

    step_535_cluster_ideological_distance_heatmap(
        cluster_distance_matrix
    )

    step_536_character_polarization_ranking_plot(
        character_summary
    )

    step_537_character_polarization_driver_decomposition(
        alignment_matrix=alignment_matrix,
        cluster_ideology_index=cluster_ideology_index,
    )
