# analysis/phase4_2_pipeline.py

from __future__ import annotations

import pandas as pd

from src.paths import (
    PHASE4_TABLES_DIR,
    PHASE4_FIGURES_DIR,
)
from src.io_utils import (
    load_respondent_clusters,
    load_character_clusters,
)
from src.config import CHARACTER_RATING_COLUMNS
from analysis.transforms.matrix_builder import build_character_matrix
from analysis.interpretation.structural_archetypes import derive_structural_archetypes

from analysis.metrics.block_structure import (
    compute_audience_character_cluster_means,
    compute_block_deviations,
    compute_block_zscores,
    bootstrap_block_deviation_significance,
)

from analysis.visualization.block_structure_plots import (
    plot_audience_character_cluster_heatmap,
    plot_block_deviation_heatmap,
    plot_block_zscore_heatmap,
    plot_block_radar_profiles,
)


# ==========================================================
# Utilities
# ==========================================================

def _ensure_dirs() -> None:
    PHASE4_TABLES_DIR.mkdir(parents=True, exist_ok=True)
    PHASE4_FIGURES_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================================
# 4.2.0 Build Rating Matrix
# ==========================================================

def step_420_build_matrix(df: pd.DataFrame) -> pd.DataFrame:

    print("\n=== 4.2.0 Build Raw Rating Matrix ===")

    matrix_raw = build_character_matrix(
        df,
        respondent_id="respondent_id",
        character_columns=CHARACTER_RATING_COLUMNS,
        standardize=False,
    )

    print(f"Matrix shape: {matrix_raw.shape}")

    return matrix_raw


# ==========================================================
# 4.2.1 Load Character Cluster Mapping
# ==========================================================

def step_421_load_character_clusters() -> pd.DataFrame:

    print("\n=== 4.2.1 Character → Character Cluster Mapping ===")

    df = load_character_clusters()

    print(df.to_string())

    return df


# ==========================================================
# 4.2.2 Load Audience Cluster Mapping
# ==========================================================

def step_422_load_respondent_clusters() -> pd.DataFrame:

    print("\n=== 4.2.2 Respondent → Audience Cluster Mapping ===")

    df = load_respondent_clusters()

    print(df.head().to_string())

    return df


# ==========================================================
# 4.2.3 Audience × Character Cluster Means
# ==========================================================

def step_423_block_means(
    matrix_raw: pd.DataFrame,
    respondent_clusters: pd.DataFrame,
    character_clusters: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 4.2.3 Audience × Character Cluster Means ===")

    print(matrix_raw.head().to_string())

    block_means = compute_audience_character_cluster_means(
        matrix_raw,
        respondent_clusters,
        character_clusters,
    )

    block_means.to_csv(
        PHASE4_TABLES_DIR
        / "audience_character_cluster_means.csv",
        index=False,
    )

    print(block_means.to_string(index=False))

    return block_means


# ==========================================================
# 4.2.4 Audience Character Cluster Heatmap
# ==========================================================

def step_424_block_heatmap(
    block_means: pd.DataFrame,
) -> None:

    print("\n=== 4.2.4 Audience × Character Cluster Heatmap ===")

    output_path = PHASE4_FIGURES_DIR / "audience_character_cluster_heatmap.png"

    plot_audience_character_cluster_heatmap(
        block_means,
        save_path=output_path,
    )

    print(f"Saved → {output_path}")


# ==========================================================
# 4.2.5 Compute block deviations
# ==========================================================

def step_425_compute_block_deviations(
    block_means: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 4.2.5 Block Deviations ===")

    block_deviations = compute_block_deviations(block_means)

    print("Computed deviations:")
    print(block_deviations.to_string(index=False))

    block_deviations.to_csv(
        PHASE4_TABLES_DIR
        / "block_deviations.csv",
        index=False,
    )

    return block_deviations


# ==========================================================
# 4.2.6 Plot block deviation heatmap
# ==========================================================

def step_426_deviation_heatmap(
    block_deviations: pd.DataFrame,
) -> None:

    print("\n=== 4.2.6 Deviation Heatmap ===")

    output_path = PHASE4_FIGURES_DIR / "audience_character_cluster_deviation_heatmap.png"

    plot_block_deviation_heatmap(
        deviation_df=block_deviations,
        output_path=output_path,
    )

    print(f"Saved → {output_path}")


# ==========================================================
# 4.2.7 Compute Z-score Strength
# ==========================================================

def step_427_block_zscores(
    block_deviations: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 4.2.7 Block Z-Scores ===")

    z_scores = compute_block_zscores(block_deviations)

    z_scores.to_csv(
        PHASE4_TABLES_DIR / "block_zscores.csv",
        index=False,
    )

    print(z_scores.to_string(index=False))

    return z_scores


# ==========================================================
# 4.2.8 Plot Z-score heatmap
# ==========================================================

def step_428_zscore_heatmap(
    zscores: pd.DataFrame,
) -> None:

    print("\n=== 4.2.8 Z-Score Heatmap ===")

    output_path = PHASE4_FIGURES_DIR / "block_zscore_heatmap.png"

    plot_block_zscore_heatmap(
        zscore_df=zscores,
        output_path=output_path,
    )

    print(f"Saved → {output_path}")


# ==========================================================
# 4.2.9 Bootstrap Structural Significance
# ==========================================================

def step_429_bootstrap_significance(
    matrix_raw: pd.DataFrame,
    respondent_clusters: pd.DataFrame,
    character_clusters: pd.DataFrame,
    deviations: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 4.2.9 Bootstrap Structural Significance ===")

    ci_df = bootstrap_block_deviation_significance(
        matrix_raw=matrix_raw,
        respondent_clusters=respondent_clusters,
        character_clusters=character_clusters,
        n_bootstrap=500,
    )

    result = deviations.merge(
        ci_df,
        on=["cluster", "character_cluster"],
        how="left",
    )

    result["significant"] = ~(
        (result["ci_low"] <= 0) & (result["ci_high"] >= 0)
    )

    output_path = PHASE4_TABLES_DIR / "bootstrap_block_significance.csv"

    result.to_csv(output_path, index=False)

    print(result.to_string(index=False))
    print(f"Saved → {output_path}")

    return result


# ==========================================================
# 4.2.10 Signed Structural Bias Profiles
# ==========================================================

def step_4210_block_radar_profiles(
    deviation_df: pd.DataFrame,
) -> None:

    print("\n=== 4.2.10 Signed Structural Bias Profiles ===")

    output_path = PHASE4_FIGURES_DIR / "block_radar_plot.png"

    plot_block_radar_profiles(
        deviation_df=deviation_df,
        output_path=output_path,
    )


def step_4211_structural_archetypes(
    deviations: pd.DataFrame,
    zscores: pd.DataFrame,
    significance: pd.DataFrame,
) -> pd.DataFrame:

    print("\n=== 4.2.11 Structural Archetype Extraction ===")

    structural_archetypes_df = derive_structural_archetypes(
        deviations,
        zscores,
        significance,
    )

    output_path = (
        PHASE4_TABLES_DIR
        / "structural_archetypes.csv"
    )

    structural_archetypes_df.to_csv(output_path, index=False)

    print(structural_archetypes_df.to_string(index=False))
    print(f"Saved → {output_path}")

    return structural_archetypes_df

# ==========================================================
# Pipeline Entry
# ==========================================================

def run_phase4_2(
    df: pd.DataFrame,
) -> None:

    print("=== PHASE 4.2: STRUCTURAL INTERACTION ANALYSIS ===")

    _ensure_dirs()

    matrix_raw = step_420_build_matrix(df)

    character_clusters = step_421_load_character_clusters()

    respondent_clusters = step_422_load_respondent_clusters()

    block_means = step_423_block_means(
        matrix_raw,
        respondent_clusters,
        character_clusters,
    )

    step_424_block_heatmap(block_means)

    block_deviations = step_425_compute_block_deviations(block_means)

    step_426_deviation_heatmap(block_deviations)

    zscores = step_427_block_zscores(block_deviations)

    step_428_zscore_heatmap(zscores)

    significance = step_429_bootstrap_significance(
        matrix_raw,
        respondent_clusters,
        character_clusters,
        block_deviations,
    )

    step_4210_block_radar_profiles(block_deviations)

    step_4211_structural_archetypes(
        block_deviations,
        zscores,
        significance,
    )
