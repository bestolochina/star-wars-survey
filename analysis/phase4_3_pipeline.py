# analysis/phase4_3_pipeline.py

from __future__ import annotations

import pandas as pd

from analysis.utils.labels import attach_all_labels
from src.paths import PHASE4_TABLES_DIR, PHASE4_FIGURES_DIR
from src.io_utils import load_respondent_clusters
from src.config import CHARACTER_RATING_COLUMNS

from analysis.transforms.matrix_builder import build_character_matrix

from analysis.metrics.character_polarization import (
    compute_character_cluster_means,
    compute_character_polarization_index,
    compute_character_alignment_matrix,
)

from analysis.metrics.narrative_alignment import (
    compute_audience_bloc_dominance,
    compute_audience_preference_gap,
    compute_narrative_alignment_index,
)
from analysis.metrics.character_structure import (
    compute_character_bridge_index,
    compute_character_cluster_attachment,
    compute_character_audience_variance,
    compute_character_ideology_coordinates,
    build_character_structure_metrics,
)
from analysis.visualization.character_structure import (
    plot_character_polarization_map,
    plot_character_polarization_triangle,
    plot_character_ideology_gradient_map,
    plot_character_audience_ideology_field,
)


# ==========================================================
# Utilities
# ==========================================================

def _ensure_dirs() -> None:

    (PHASE4_TABLES_DIR / "polarization").mkdir(
        parents=True,
        exist_ok=True,
    )

    (PHASE4_FIGURES_DIR / "polarization").mkdir(
        parents=True,
        exist_ok=True,
    )


# ==========================================================
# 4.3.0 Build Character Matrix
# ==========================================================

def step_430_build_matrix(
    df: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 4.3.0 Build Character Rating Matrix ===")

    matrix = build_character_matrix(
        df,
        respondent_id="respondent_id",
        character_columns=CHARACTER_RATING_COLUMNS,
        standardize=False,
    )

    print(f"Matrix shape: {matrix.shape}")

    return matrix


# ==========================================================
# 4.3.1 Load Respondent Clusters
# ==========================================================

def step_431_load_clusters() -> pd.DataFrame:

    print("\n=== 4.3.1 Load Respondent Clusters ===")

    clusters = load_respondent_clusters()

    clusters = attach_all_labels(clusters)

    print(clusters.head().to_string())

    return clusters


# ==========================================================
# 4.3.2 Character Means by Audience Cluster
# ==========================================================

def step_432_character_cluster_means(
    matrix: pd.DataFrame,
    respondent_clusters: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 4.3.2 Character Means by Audience Cluster ===")

    means = compute_character_cluster_means(
        matrix,
        respondent_clusters,
    )

    path = (
        PHASE4_TABLES_DIR
        / "polarization"
        / "character_cluster_means.csv"
    )

    means = attach_all_labels(means)

    means.to_csv(path, index=False)

    print(means.head().to_string())
    print(f"Saved → {path}")

    return means


# ==========================================================
# 4.3.3 Character Alignment Matrix
# ==========================================================

def step_433_alignment_matrix(
    means: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 4.3.3 Character Alignment Matrix ===")

    alignment = compute_character_alignment_matrix(
        means
    )

    path = (
        PHASE4_TABLES_DIR
        / "polarization"
        / "character_alignment_matrix.csv"
    )

    alignment.to_csv(path)

    print(alignment.head().to_string())
    print(f"Saved → {path}")

    return alignment


# ==========================================================
# 4.3.4 Character Polarization Index
# ==========================================================

def step_434_character_polarization(
    means: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 4.3.4 Character Polarization Index ===")

    polarization = compute_character_polarization_index(
        means
    )

    path = (
        PHASE4_TABLES_DIR
        / "polarization"
        / "character_polarization_index.csv"
    )

    polarization.to_csv(path, index=False)

    print(polarization.head().to_string())
    print(f"Saved → {path}")

    return polarization


# ==========================================================
# 4.3.5 Audience Bloc Dominance
# ==========================================================

def step_435_bloc_dominance(
    block_means: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 4.3.5 Audience Bloc Dominance ===")

    dominance = compute_audience_bloc_dominance(
        block_means
    )

    path = (
        PHASE4_TABLES_DIR
        / "polarization"
        / "audience_bloc_dominance.csv"
    )

    dominance = attach_all_labels(dominance)

    dominance.to_csv(path, index=False)

    print(dominance.to_string(index=False))
    print(f"Saved → {path}")

    return dominance


# ==========================================================
# 4.3.6 Audience Preference Gap
# ==========================================================

def step_436_preference_gap(
    block_means: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 4.3.6 Audience Preference Gap ===")

    gap = compute_audience_preference_gap(
        block_means
    )

    path = (
        PHASE4_TABLES_DIR
        / "polarization"
        / "audience_preference_gap.csv"
    )

    gap = attach_all_labels(gap)

    gap.to_csv(path, index=False)

    print(gap.to_string(index=False))
    print(f"Saved → {path}")

    return gap


# ==========================================================
# 4.3.7 Narrative Alignment Index
# ==========================================================

def step_437_alignment_index(
    block_means: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 4.3.7 Narrative Alignment Index ===")

    index = compute_narrative_alignment_index(
        block_means
    )

    path = (
        PHASE4_TABLES_DIR
        / "polarization"
        / "narrative_alignment_index.csv"
    )

    index = attach_all_labels(index)

    index.to_csv(path, index=False)

    print(index.to_string(index=False))
    print(f"Saved → {path}")

    return index


# ==========================================================
# 4.3.8 Character Bridge Index
# ==========================================================

def step_438_bridge_index(
    means: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 4.3.8 Character Bridge Index ===")

    bridge = compute_character_bridge_index(means)

    path = (
        PHASE4_TABLES_DIR
        / "polarization"
        / "character_bridge_index.csv"
    )

    bridge = attach_all_labels(bridge)

    bridge.to_csv(path, index=False)

    print(bridge.head().to_string())
    print(f"Saved → {path}")

    return bridge


# ==========================================================
# 4.3.9 Character Cluster Attachment
# ==========================================================

def step_439_cluster_attachment(
    means: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 4.3.9 Character Cluster Attachment ===")

    attachment = compute_character_cluster_attachment(
        means
    )

    path = (
        PHASE4_TABLES_DIR
        / "polarization"
        / "character_cluster_attachment.csv"
    )

    attachment = attach_all_labels(attachment)

    attachment.to_csv(path, index=False)

    print(attachment.head().to_string())
    print(f"Saved → {path}")

    return attachment


# ==========================================================
# 4.3.10 Character Audience Variance
# ==========================================================

def step_4310_audience_variance(
    means: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 4.3.10 Character Audience Variance ===")

    variance = compute_character_audience_variance(
        means
    )

    path = (
        PHASE4_TABLES_DIR
        / "polarization"
        / "character_audience_variance.csv"
    )

    variance = attach_all_labels(variance)

    variance.to_csv(path, index=False)

    print(variance.head().to_string())
    print(f"Saved → {path}")

    return variance


# ==========================================================
# 4.3.11 Character Polarization Map
# ==========================================================

def step_4311_character_map(
    bridge: pd.DataFrame,
    polarization: pd.DataFrame,
) -> None:

    print("\n=== 4.3.11 Character Polarization Map ===")

    save_path = (
        PHASE4_FIGURES_DIR
        / "polarization"
        / "character_polarization_map.png"
    )

    plot_character_polarization_map(
        bridge,
        polarization,
        save_path=str(save_path),
    )

    print(f"Saved → {save_path}")


# ==========================================================
# 4.3.12 Character Polarization Triangle
# ==========================================================

def step_4312_character_polarization_triangle(
    means: pd.DataFrame,
) -> None:

    print("\n=== 4.3.12 Character Polarization Triangle ===")

    save_path = (
            PHASE4_FIGURES_DIR
            / "polarization"
            / "character_polarization_triangle.png"
    )

    plot_character_polarization_triangle(
        means,
        save_path=str(save_path),
    )

    print(f"Saved → {save_path}")


# ==========================================================
# 4.3.13 Character Ideology Gradient Map
# ==========================================================

def step_4313_character_ideology_gradient_map(
    variance: pd.DataFrame,
    attachment: pd.DataFrame,
) -> None:

    print("\n=== 4.3.13 Character Ideology Gradient Map ===")

    save_path = (
        PHASE4_FIGURES_DIR
        / "polarization"
        / "character_ideology_gradient_map.png"
    )

    plot_character_ideology_gradient_map(
        variance,
        attachment,
        save_path=str(save_path),
    )

    print(f"Saved → {save_path}")


# ==========================================================
# 4.3.14 Character–Audience Ideology Field
# ==========================================================

def step_4314_character_audience_ideology_field(
        alignment: pd.DataFrame,
) -> None:
    print("\n=== 4.3.14 Character–Audience Ideology Field ===")

    save_path = (
            PHASE4_FIGURES_DIR
            / "polarization"
            / "character_audience_ideology_field.png"
    )

    plot_character_audience_ideology_field(
        alignment,
        save_path=str(save_path),
    )

    print(f"Saved → {save_path}")


# ==========================================================
# 4.3.15 Character Ideology Coordinates
# ==========================================================

def step_4315_character_ideology_coordinates(
    alignment: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 4.3.15 Character Ideology Coordinates ===")

    coords = compute_character_ideology_coordinates(alignment)

    path = (
        PHASE4_TABLES_DIR
        / "polarization"
        / "character_ideology_coordinates.csv"
    )

    coords.to_csv(path, index=False)

    print(coords.head().to_string())
    print(f"Saved → {path}")

    return coords


# ==========================================================
# 4.3.16 Character Structure Metrics
# ==========================================================

def step_4316_character_structure_metrics(
    polarization: pd.DataFrame,
    bridge: pd.DataFrame,
    variance: pd.DataFrame,
    attachment: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 4.3.16 Character Structure Metrics ===")

    metrics = build_character_structure_metrics(
        polarization,
        bridge,
        variance,
        attachment,
    )

    path = (
        PHASE4_TABLES_DIR
        / "polarization"
        / "character_structure_metrics.csv"
    )

    metrics.to_csv(path, index=False)

    print(metrics.head().to_string())
    print(f"Saved → {path}")

    return metrics


# ==========================================================
# Pipeline Entry
# ==========================================================

def run_phase4_3(
    df: pd.DataFrame,
) -> None:

    print("=== PHASE 4.3: CHARACTER POLARIZATION ===")

    _ensure_dirs()

    matrix = step_430_build_matrix(df)

    respondent_clusters = step_431_load_clusters()

    means = step_432_character_cluster_means(
        matrix,
        respondent_clusters,
    )

    alignment = step_433_alignment_matrix(means)

    polarization = step_434_character_polarization(means)

    block_means = pd.read_csv(
        PHASE4_TABLES_DIR
        / "audience_character_cluster_means.csv"
    )

    step_435_bloc_dominance(block_means)

    step_436_preference_gap(block_means)

    step_437_alignment_index(block_means)

    bridge = step_438_bridge_index(means)

    attachment = step_439_cluster_attachment(means)

    variance = step_4310_audience_variance(means)

    step_4311_character_map(
        bridge,
        polarization,
    )

    step_4312_character_polarization_triangle(
        means
    )

    step_4313_character_ideology_gradient_map(
        variance,
        attachment,
    )

    step_4314_character_audience_ideology_field(alignment)

    step_4315_character_ideology_coordinates(alignment)

    metrics = step_4316_character_structure_metrics(
        polarization,
        bridge,
        variance,
        attachment,
        )
