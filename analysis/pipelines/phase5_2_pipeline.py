# analysis/pipelines/phase5_2_pipeline.py

from __future__ import annotations

import pandas as pd

from src.io_utils import load_clean_star_wars_with_audience_clusters
from src.paths import PHASE4_TABLES_DIR, PHASE5_TABLES_DIR, PHASE5_FIGURES_DIR, PHASE3_TABLES_DIR
from src.config import CHARACTER_RATING_COLUMNS

from analysis.visualization.phase5_plots import (
    plot_audience_character_bloc_affinity_heatmap,
    plot_cluster_character_preference_profiles,
    plot_audience_character_ideology_alignment_map,
)

from analysis.metrics.character_polarization import (
    compute_character_polarization_index,
    compute_character_ideological_blocs,
    compute_character_bloc_summary,
    compute_character_bloc_sizes,
    compute_character_cluster_polarization,
)

from analysis.metrics.audience_character_alignment import (
    build_audience_character_alignment_matrix,
    compute_audience_cluster_character_rankings,
    compute_character_evaluation_variance_across_audience_clusters,
    compute_character_divergence_across_audience_clusters,
    compute_audience_cluster_character_ideology_distance,
    compute_character_segmentation_strength_across_audience_clusters,
    compute_audience_cluster_character_affinity_profiles,
    compute_audience_bloc_affinity,
    compute_cluster_ideology_index,
    compute_audience_cluster_engagement_index,
    compute_audience_cluster_character_rating_positivity_bias,
    compute_audience_cluster_character_preference_distance,
)


# ==========================================================
# Utilities
# ==========================================================

def _ensure_dirs() -> None:

    (PHASE5_TABLES_DIR / "alignment").mkdir(
        parents=True,
        exist_ok=True,
    )

    (PHASE5_TABLES_DIR / "segmentation").mkdir(
        parents=True,
        exist_ok=True,
    )

    (PHASE5_FIGURES_DIR / "alignment").mkdir(
        parents=True,
        exist_ok=True,
    )

    (PHASE5_FIGURES_DIR / "segmentation").mkdir(
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
    character_ideology_coordinates: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.2.5 Audience Cluster–Character Ideological Distance ===")

    distance = compute_audience_cluster_character_ideology_distance(
        audience_cluster_coords,
        character_ideology_coordinates,
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
# 5.2.7 Character Polarization Index
# ==========================================================

def step_527_character_polarization_index(
    character_cluster_means: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.2.7 Character Polarization Index ===")

    df = compute_character_polarization_index(
        character_cluster_means
    )

    path = (
        PHASE5_TABLES_DIR
        / "alignment"
        / "character_polarization_index.csv"
    )

    df.to_csv(path, index=False)

    print(df.to_string())
    print(f"Saved → {path}")

    return df


# ==========================================================
# 5.2.8 Audience Cluster Character Affinity Profiles
# ==========================================================

def step_528_audience_cluster_character_affinity_profiles(
    means: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.2.8 Audience Cluster Character Affinity Profiles ===")

    df = compute_audience_cluster_character_affinity_profiles(
        means
    )

    path = (
        PHASE5_TABLES_DIR
        / "alignment"
        / "audience_cluster_character_affinity_profiles.csv"
    )

    df.to_csv(path, index=False)

    print(df.to_string())
    print(f"Saved → {path}")

    return df


# ==========================================================
# 5.2.9 Character Ideological Blocs
# ==========================================================

def step_529_character_ideological_blocs(
    means: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.2.9 Character Ideological Blocs ===")

    df = compute_character_ideological_blocs(means)

    path = (
        PHASE5_TABLES_DIR
        / "alignment"
        / "character_ideological_blocs.csv"
    )

    df.to_csv(path, index=False)

    print(df.to_string())
    print(f"Saved → {path}")

    return df


# ==========================================================
# 5.2.10 Character Block Summary
# ==========================================================

def step_5210_character_bloc_summary(
    blocs: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.2.10 Character Bloc Summary ===")

    df = compute_character_bloc_summary(blocs)

    path = (
        PHASE5_TABLES_DIR
        / "alignment"
        / "character_bloc_summary.csv"
    )

    df.to_csv(path, index=False)

    print(df.to_string())
    print(f"Saved → {path}")

    return df


# ==========================================================
# 5.2.11 Audience × Character Bloc Affinity
# ==========================================================

def step_5211_audience_bloc_affinity(
    means: pd.DataFrame,
    blocs: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.2.11 Audience × Character Bloc Affinity ===")

    df = compute_audience_bloc_affinity(
        means,
        blocs,
    )

    path = (
        PHASE5_TABLES_DIR
        / "alignment"
        / "audience_bloc_affinity_matrix.csv"
    )

    df.to_csv(path, index=False)

    print(df.to_string())
    print(f"Saved → {path}")

    return df


# ==========================================================
# 5.2.12 Audience × Character Bloc Affinity
# ==========================================================

def step_5212_character_bloc_sizes(
    blocs: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.2.12 Character Bloc Sizes ===")

    df = compute_character_bloc_sizes(blocs)

    path = (
        PHASE5_TABLES_DIR
        / "alignment"
        / "character_bloc_sizes.csv"
    )

    df.to_csv(path, index=False)

    print(df.to_string())
    print(f"Saved → {path}")

    return df


# ==========================================================
# 5.2.13 Cluster Ideology Index
# ==========================================================

def step_5213_cluster_ideology_index(
    affinity: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.2.13 Cluster Ideology Index ===")

    df = compute_cluster_ideology_index(affinity)

    path = (
        PHASE5_TABLES_DIR
        / "alignment"
        / "cluster_ideology_index.csv"
    )

    df.to_csv(path, index=False)

    print(df.to_string())
    print(f"Saved → {path}")

    return df


# ==========================================================
# 5.2.14 Audience Engagement Index
# ==========================================================

def step_5214_audience_cluster_engagement_index(
    respondents: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.2.14 Audience Engagement Index ===")

    df = compute_audience_cluster_engagement_index(
        respondents
    )

    path = (
        PHASE5_TABLES_DIR
        / "alignment"
        / "audience_cluster_engagement_index.csv"
    )

    df.to_csv(path, index=False)

    print(df.to_string())
    print(f"Saved → {path}")

    return df


# ==========================================================
# 5.2.15 Audience × Character Bloc Affinity Heatmap
# ==========================================================

def step_5215_audience_character_bloc_affinity_heatmap(
    affinity: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.2.15 Audience × Character Bloc Affinity Heatmap ===")

    path = (
        PHASE5_FIGURES_DIR
        / "alignment"
        / "audience_character_bloc_affinity_heatmap.png"
    )

    heatmap_df = plot_audience_character_bloc_affinity_heatmap(
        affinity,
        path,
    )

    print(f"Saved → {path}")

    path = (
            PHASE5_TABLES_DIR
            / "alignment"
            / "audience_character_bloc_affinity_heatmap.csv"
    )

    heatmap_df.to_csv(path, index=False)
    print(heatmap_df.to_string())
    print(f"Saved → {path}")

    return heatmap_df


# ==========================================================
# 5.2.16 Audience Cluster Character Rating Positivity Bias
# ==========================================================

def step_5216_cluster_positivity_bias(
    respondents: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.2.16 Audience Cluster Character Rating Positivity Bias ===")

    df = compute_audience_cluster_character_rating_positivity_bias(respondents)

    path = (
        PHASE5_TABLES_DIR
        / "alignment"
        / "cluster_positivity_bias.csv"
    )

    df.to_csv(path, index=False)

    print(df.to_string())
    print(f"Saved → {path}")

    return df


# ==========================================================
# 5.2.17 Audience Cluster Character Preference Distance
# ==========================================================

def step_5217_audience_cluster_character_preference_distance(
    means: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.2.17 Audience Cluster Character Preference Distance ===")

    df = compute_audience_cluster_character_preference_distance(means)

    path = (
        PHASE5_TABLES_DIR
        / "alignment"
        / "audience_cluster_character_preference_distance.csv"
    )

    df.to_csv(path, index=False)

    print(df.to_string())
    print(f"Saved → {path}")

    return df


# ==========================================================
# 5.2.18 Audience × Character Ideology Alignment Map
# ==========================================================

def step_5218_audience_character_ideology_alignment_map(
        character_ideology_coordinates: pd.DataFrame,
        audience_cluster_centroids: pd.DataFrame,
) -> None:

    print("\n=== 5.2.18 Audience × Character Ideology Alignment Map ===")

    path = (
        PHASE5_FIGURES_DIR
        / "alignment"
        / "audience_character_ideology_alignment_map"
    )

    plot_audience_character_ideology_alignment_map(
        character_ideology_coordinates,
        audience_cluster_centroids,
        path,
    )

    print(f"Saved → {path}")


# ==========================================================
# 5.2.19 Cluster Character Preference Profiles
# ==========================================================

def step_5219_cluster_character_preference_profiles(
    respondents: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.2.19 Cluster Character Preference Profiles ===")

    path = (
        PHASE5_FIGURES_DIR
        / "alignment"
        / "cluster_character_preference_profiles.png"
    )

    profile_df = plot_cluster_character_preference_profiles(
        respondents,
        path,
    )

    print(f"Saved → {path}")

    path = (
        PHASE5_TABLES_DIR
        / "alignment"
        / "cluster_character_preference_profiles.csv"
    )

    profile_df.to_csv(path)
    print(profile_df.to_string())
    print(f"Saved → {path}")

    return profile_df


# ==========================================================
# 5.2.20 Character Polarization Index
# ==========================================================

def step_5220_character_cluster_polarization(
    respondents: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 5.2.20 Character Polarization Index ===")

    df = compute_character_cluster_polarization(respondents)

    path = (
        PHASE5_TABLES_DIR
        / "alignment"
        / "character_cluster_polarization.csv"
    )

    df.to_csv(path, index=False)

    print(df.to_string())
    print(f"Saved → {path}")

    return df


# ==========================================================
# Pipeline Entry
# ==========================================================

def run_phase5_2() -> None:

    print("=== PHASE 5.2: AUDIENCE–CHARACTER INTERACTION ===")

    _ensure_dirs()

    respondents = load_clean_star_wars_with_audience_clusters()

    polarization_dir = PHASE4_TABLES_DIR / "polarization"

    means = pd.read_csv(
        polarization_dir / "character_cluster_means.csv"
    )

    character_ideology_coordinates = pd.read_csv(
        PHASE4_TABLES_DIR / "polarization" / "character_ideology_coordinates.csv"
    )

    audience_cluster_centroids = pd.read_csv(
        PHASE3_TABLES_DIR / "audience_cluster_centroids.csv"
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
        character_ideology_coordinates,
    )

    step_526_character_segmentation_strength_across_audience_clusters()

    step_527_character_polarization_index(means)

    step_528_audience_cluster_character_affinity_profiles(means)

    blocs = step_529_character_ideological_blocs(means)

    step_5210_character_bloc_summary(blocs)

    affinity = step_5211_audience_bloc_affinity(means, blocs)

    step_5212_character_bloc_sizes(blocs)

    step_5213_cluster_ideology_index(affinity)

    engagement = step_5214_audience_cluster_engagement_index(respondents)

    heatmap = step_5215_audience_character_bloc_affinity_heatmap(affinity)

    step_5216_cluster_positivity_bias(respondents)

    step_5217_audience_cluster_character_preference_distance(means)

    step_5218_audience_character_ideology_alignment_map(
        character_ideology_coordinates,
        audience_cluster_centroids
    )

    step_5219_cluster_character_preference_profiles(respondents)

    step_5220_character_cluster_polarization(respondents)

