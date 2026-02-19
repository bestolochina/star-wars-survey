# analysis/phase2_pipeline.py

from __future__ import annotations

import pandas as pd
from dataclasses import dataclass

from src.paths import PHASE2_FIGURES_DIR, PHASE2_TABLES_DIR
from src.config import (
    EPISODE_RANK_COLUMNS,
    CHARACTER_RATING_COLUMNS,
)

from analysis.transforms.reshaping import melt_variable
from analysis.metrics.segmentation_metrics import (
    compute_all_segmentation_metrics,
    build_comparison_table_from_metrics,
    build_all_variable_divergence_tables_from_metrics,
    extract_all_variable_drivers,
)
from analysis.visualization.segmentation_plots import (
    plot_segmentation_comparison,
    plot_variable_divergence_heatmap,
    plot_variable_drivers,
)


# ==========================================================
# DATA CONTAINER
# ==========================================================

@dataclass
class Phase2Data:
    episode_long: pd.DataFrame
    character_long: pd.DataFrame


# ==========================================================
# BUILD LONG DATA ONCE
# ==========================================================

def build_phase2_data(df: pd.DataFrame) -> Phase2Data:

    episode_long = melt_variable(
        df,
        variable_columns=EPISODE_RANK_COLUMNS,
        variable_name="episode",
        value_name="rank",
    )

    character_long = melt_variable(
        df,
        variable_columns=CHARACTER_RATING_COLUMNS,
        variable_name="character",
        value_name="rating",
    )

    return Phase2Data(
        episode_long=episode_long,
        character_long=character_long,
    )


# ==========================================================
# GENERIC SEGMENTATION PIPELINE
# ==========================================================

def run_segmentation_phase(
    *,
    long_df: pd.DataFrame,
    variable_name: str,
    value_name: str,
    output_prefix: str,
) -> None:

    print(f"\n=== SEGMENTATION PHASE: {variable_name.upper()} ===")

    save_dir = PHASE2_FIGURES_DIR / output_prefix
    save_dir.mkdir(parents=True, exist_ok=True)

    tables_dir = PHASE2_TABLES_DIR / output_prefix
    tables_dir.mkdir(parents=True, exist_ok=True)

    # 1️⃣ Compute segmentation metrics
    metrics_store = compute_all_segmentation_metrics(
        long_df,
        variable_column=variable_name,
        value_column=value_name,
    )

    # 2️⃣ Segmentation comparison
    comparison_table = build_comparison_table_from_metrics(
        metrics_store
    )

    print("\n--- Segmentation Comparison ---")
    print(comparison_table.to_string())

    # 3️⃣ Divergence tables
    divergence_tables = build_all_variable_divergence_tables_from_metrics(
        metrics_store
    )

    print("\n--- Divergence Tables ---")
    for demo, table in divergence_tables.items():
        print(f"\n[{demo}]")
        print(table.to_string())

    # 4️⃣ Drivers
    drivers = extract_all_variable_drivers(
        metrics_store,
        top_n=2,
    )

    print("\n--- Drivers ---")
    for demo, table in drivers.items():
        print(f"\n[{demo}]")
        print(table.to_string())

    # ======================================================
    # EXPORT TABLES
    # ======================================================

    print("\n--- Exporting Tables ---")

    comparison_table.to_csv(
        tables_dir / f"{output_prefix}_segmentation_strength.csv"
    )

    for demo, table in divergence_tables.items():
        table.to_csv(
            tables_dir / f"{output_prefix}_divergence_{demo}.csv"
        )

    for demo, table in drivers.items():
        table.to_csv(
            tables_dir / f"{output_prefix}_drivers_{demo}.csv",
            index=False,
        )

    print(f"Tables saved to: {tables_dir}")

    # ======================================================
    # VISUALIZATION
    # ======================================================

    print("\n--- Generating Plots ---")

    plot_segmentation_comparison(
        comparison_table,
        save_dir=save_dir,
    )

    plot_variable_divergence_heatmap(
        metrics_store,
        save_dir=save_dir,
    )

    plot_variable_drivers(
        drivers,
        save_dir=save_dir,
    )

    print(f"Plots saved to: {save_dir}")
    print(f"\nSegmentation phase for {variable_name} complete.\n")


# ==========================================================
# MASTER PHASE 2 RUNNER
# ==========================================================

def run_phase_2(df: pd.DataFrame) -> None:

    phase2_data = build_phase2_data(df)

    # Episode segmentation
    run_segmentation_phase(
        long_df=phase2_data.episode_long,
        variable_name="episode",
        value_name="rank",
        output_prefix="episode",
    )

    # Character segmentation
    run_segmentation_phase(
        long_df=phase2_data.character_long,
        variable_name="character",
        value_name="rating",
        output_prefix="character",
    )
