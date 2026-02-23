# analysis/phase3_pipeline.py

from __future__ import annotations

import pandas as pd

from src.paths import PHASE3_TABLES_DIR, PHASE3_FIGURES_DIR
from src.config import CHARACTER_RATING_COLUMNS

from analysis.transforms.matrix_builder import (
    build_character_matrix,
)
from analysis.metrics.correlation_structure import (
    compute_character_correlation,
)
from analysis.visualization.structure_plots import (
    plot_correlation_heatmap,
)


# ==========================================================
# PHASE 3 — STEP 3.1.1
# ==========================================================

def run_phase3_correlation(
    df: pd.DataFrame,
    *,
    respondent_id: str,
) -> pd.DataFrame:

    print("\n=== PHASE 3 — CHARACTER STRUCTURE ===")

    tables_dir = PHASE3_TABLES_DIR
    figures_dir = PHASE3_FIGURES_DIR

    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------
    # Build matrix
    # ------------------------------------------------------

    matrix = build_character_matrix(
        df,
        respondent_id=respondent_id,
        character_columns=CHARACTER_RATING_COLUMNS,
        standardize=True,
    )

    print(f"Matrix shape: {matrix.shape}")

    # ------------------------------------------------------
    # Correlation
    # ------------------------------------------------------

    corr = compute_character_correlation(matrix)

    # save table
    corr.to_csv(
        tables_dir / "correlation_matrix.csv"
    )

    # plot
    plot_correlation_heatmap(
        corr,
        save_path=figures_dir / "correlation_heatmap.png",
    )

    print("Correlation structure saved.")

    return corr