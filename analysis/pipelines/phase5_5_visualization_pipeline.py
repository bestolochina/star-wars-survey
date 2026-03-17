# analysis/pipelines/phase5_5_visualization_pipeline.py

from __future__ import annotations

import pandas as pd

from src.paths import (
    PHASE5_TABLES_DIR,
    PHASE5_FIGURES_DIR,
    PHASE4_TABLES_DIR,
    PHASE3_TABLES_DIR,
)

from analysis.visualization.phase5_plots import (
    plot_cluster_character_heatmap,
    plot_cluster_character_divergence,
    plot_polarization_driver_ranking,
    plot_cluster_archetype_profiles,
    plot_audience_character_ideology_alignment_map,
    plot_character_ideology_force_field,
)


# ==========================================================
# Utilities
# ==========================================================

def _ensure_dirs() -> None:

    (PHASE5_FIGURES_DIR / "visualizations").mkdir(
        parents=True,
        exist_ok=True,
    )


# ==========================================================
# 5.5.1 Cluster Character Heatmap
# ==========================================================

def step_551_cluster_character_heatmap(
    alignment_matrix: pd.DataFrame,
) -> None:

    print("\n=== 5.5.1 Cluster Character Heatmap ===")

    path = (
        PHASE5_FIGURES_DIR
        / "visualizations"
        / "cluster_character_heatmap.png"
    )

    plot_cluster_character_heatmap(
        alignment_matrix,
        path,
    )

    print(f"Saved → {path}")


# ==========================================================
# 5.5.2 Cluster Character Divergence
# ==========================================================

def step_552_cluster_character_divergence(
    variance_table: pd.DataFrame,
) -> None:

    print("\n=== 5.5.2 Cluster Character Divergence ===")

    path = (
        PHASE5_FIGURES_DIR
        / "visualizations"
        / "cluster_character_divergence.png"
    )

    plot_cluster_character_divergence(
        variance_table,
        path,
    )

    print(f"Saved → {path}")


# ==========================================================
# 5.5.3 Polarization Driver Ranking
# ==========================================================

def step_553_polarization_driver_ranking(
    polarization_table: pd.DataFrame,
) -> None:

    print("\n=== 5.5.3 Polarization Driver Ranking ===")

    path = (
        PHASE5_FIGURES_DIR
        / "visualizations"
        / "polarization_driver_ranking.png"
    )

    plot_polarization_driver_ranking(
        polarization_table,
        path,
    )

    print(f"Saved → {path}")


# ==========================================================
# 5.5.4 Cluster Archetype Profiles
# ==========================================================

def step_554_cluster_archetype_profiles(
    archetype_table: pd.DataFrame,
) -> None:

    print("\n=== 5.5.4 Cluster Archetype Profiles ===")

    path = (
        PHASE5_FIGURES_DIR
        / "visualizations"
        / "cluster_archetype_profiles.png"
    )

    plot_cluster_archetype_profiles(
        archetype_table,
        path,
    )

    print(f"Saved → {path}")


# ==========================================================
# 5.5.5 Fandom Ideology Map
# ==========================================================

def step_555_fandom_ideology_map(
    character_coords: pd.DataFrame,
    cluster_coords: pd.DataFrame,
) -> None:

    print("\n=== 5.5.5 Fandom Ideology Map ===")

    path = (
        PHASE5_FIGURES_DIR
        / "visualizations"
        / "fandom_ideology_map.png"
    )

    plot_audience_character_ideology_alignment_map(
        character_coords,
        cluster_coords,
        path,
    )

    print(f"Saved → {path}")


# ==========================================================
# 5.5.6 Fandom Ideological Force Field
# ==========================================================

def step_556_fandom_ideological_force_field(
    character_coords,
    cluster_coords,
    archetype_table,
):
    print("\n=== 5.5.6 Fandom Ideological Force Field ===")

    path = (
            PHASE5_FIGURES_DIR
            / "visualizations"
            / "fandom_ideological_force_field.png"
    )

    plot_character_ideology_force_field(
        character_coords,
        cluster_coords,
        archetype_table,
        output_path=path,
    )



# ==========================================================
# Pipeline Entry
# ==========================================================

def run_phase5_5() -> None:

    print("=== PHASE 5.5: VISUALIZATION LAYER ===")

    _ensure_dirs()

    alignment_dir = PHASE5_TABLES_DIR / "alignment"
    polarization_dir = PHASE5_TABLES_DIR / "polarization"
    narrative_dir = PHASE5_TABLES_DIR / "narrative_structure"

    # ------------------------------------------------------
    # Load Tables
    # ------------------------------------------------------

    alignment_matrix = pd.read_csv(
        alignment_dir / "cluster_character_preference_profiles.csv",
        index_col=0,
    )

    variance_table = pd.read_csv(
        alignment_dir
        / "character_evaluation_variance_across_audience_clusters.csv"
    )

    polarization_table = pd.read_csv(
        alignment_dir / "character_polarization_index.csv"
    )

    archetype_table = pd.read_csv(
        narrative_dir / "audience_cluster_narrative_archetypes.csv"
    )

    character_coords = pd.read_csv(
        PHASE4_TABLES_DIR
        / "polarization"
        / "character_ideology_coordinates.csv"
    )

    cluster_coords = pd.read_csv(
        PHASE3_TABLES_DIR
        / "audience_cluster_centroids.csv"
    )

    # ------------------------------------------------------
    # Run Visualizations
    # ------------------------------------------------------

    step_551_cluster_character_heatmap(alignment_matrix)

    step_552_cluster_character_divergence(variance_table)

    step_553_polarization_driver_ranking(polarization_table)

    step_554_cluster_archetype_profiles(archetype_table)

    step_555_fandom_ideology_map(
        character_coords,
        cluster_coords,
    )

    step_556_fandom_ideological_force_field(
        character_coords,
        cluster_coords,
        archetype_table,
    )



