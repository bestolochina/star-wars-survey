# analysis/phase4_2_pipeline.py

from __future__ import annotations

import pandas as pd

from src.paths import (
    PHASE3_TABLES_DIR,
    PHASE4_TABLES_DIR,
    PHASE4_FIGURES_DIR,
)
from src.io_utils import (
    load_respondent_clusters,
    load_character_clusters,
)
from src.config import CHARACTER_RATING_COLUMNS
from analysis.transforms.matrix_builder import build_character_matrix

from analysis.metrics.block_structure import (
    compute_audience_character_cluster_means,
)

from analysis.visualization.block_structure_plots import (
    plot_audience_character_cluster_heatmap,
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

    print(df.head().to_string())

    return df


def step_422_load_respondent_clusters() -> pd.DataFrame:

    print("\n=== 4.2.2 Respondent → Audience Cluster Mapping ===")

    df = load_respondent_clusters()

    print(df.head().to_string())

    return df


# ==========================================================
# 4.2.2 Audience × Character Cluster Means
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
# 4.2.3 Audience Character Cluster Heatmap
# ==========================================================

def step_424_block_heatmap(
    block_means: pd.DataFrame,
) -> None:

    print("\n=== 4.2.4 Audience × Character Cluster Heatmap ===")

    plot_audience_character_cluster_heatmap(
        block_means,
        save_path=(
            PHASE4_FIGURES_DIR
            / "audience_character_cluster_heatmap.png"
        ),
    )


# ==========================================================
# Pipeline Entry
# ==========================================================

def run_phase4_2(
    df: pd.DataFrame,
) -> None:

    print("=== PHASE 4.2: STRUCTURAL INTERACTION ANALYSIS ===")

    _ensure_dirs()

    # -----------------------------------------
    # Character blocs
    # -----------------------------------------
    character_clusters = step_421_load_character_clusters()
    respondent_clusters = step_422_load_respondent_clusters()

    # -----------------------------------------
    # Block aggregation
    # -----------------------------------------
    matrix_raw = step_420_build_matrix(df)

    block_means = step_423_block_means(
        matrix_raw,
        respondent_clusters,
        character_clusters,
    )

    # -----------------------------------------
    # Visualization
    # -----------------------------------------
    step_424_block_heatmap(block_means)
