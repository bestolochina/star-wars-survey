# analysis/pipelines/phase2_3_part1_pipeline.py

from __future__ import annotations

from pathlib import Path
import pandas as pd
from typing import List, Literal

from analysis.transforms.reshaping import melt_variable

from analysis.metrics.distribution_metrics import (
    validate_ordinal_percentage_sums,
    build_all_ordinal_distribution_tables,
)

from analysis.visualization.phase2_3_part1_plots import (
    plot_rank_histograms_single_slice_horizontal_grid,
)

from src.paths import PHASE2_FIGURES_DIR, PHASE2_TABLES_DIR
from src.config import (
    DEMOGRAPHICS_COLUMNS,
    EPISODE_RANK_COLUMNS,
    CHARACTER_RATING_COLUMNS,
)


# ==========================================================
# DISTRIBUTION PIPELINE
# ==========================================================

def run_distribution_phase(
    df: pd.DataFrame,
    *,
    variable_columns: dict[str, str],
    variable_name: str,
    value_name: str,
    better: Literal["low", "high"],
    output_prefix: str,
) -> None:

    print(f"\n=== DISTRIBUTION PHASE: {variable_name.upper()} ===")

    tables_dir = PHASE2_TABLES_DIR / (output_prefix + "_distribution")
    figures_dir = PHASE2_FIGURES_DIR / (output_prefix + "_distribution")

    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nTables → {tables_dir}")
    print(f"Figures → {figures_dir}")

    demographics: List[str] = list(DEMOGRAPHICS_COLUMNS.keys())

    # --------------------------------------------------
    # Melt variable
    # --------------------------------------------------

    df_long = melt_variable(
        df,
        variable_columns=variable_columns,
        variable_name=variable_name,
        value_name=value_name,
    )

    print(f"\nRows: {len(df_long):,}")
    print(f"Unique {variable_name}s: {df_long[variable_name].nunique()}")

    # --------------------------------------------------
    # Validate percentage sums
    # --------------------------------------------------

    print("\n--- Validating Percentage Sums ---")

    validation = validate_ordinal_percentage_sums(
        df_long,
        demographic_columns=demographics,
        variable_column=variable_name,
        rank_column=value_name,
    )

    print(validation["valid"].value_counts().to_string())

    if not validation["valid"].all():
        raise ValueError(
            f"{variable_name} percentage validation failed."
        )

    print("Validation passed.\n")

    # --------------------------------------------------
    # Build distribution tables
    # --------------------------------------------------

    print("--- Building Distribution Tables ---")

    distribution_tables = build_all_ordinal_distribution_tables(
        df_long,
        variable_column=variable_name,
        rank_column=value_name,
        slice_config=DEMOGRAPHICS_COLUMNS,
    )

    # --------------------------------------------------
    # Export tables
    # --------------------------------------------------

    print("\n--- Exporting Distribution Tables ---")

    for demo, table in distribution_tables.items():

        path = tables_dir / f"{output_prefix}_distribution_{demo}.csv"

        table.to_csv(path)

        print(f"Saved → {path}")

    print("\nTables exported.")

    # --------------------------------------------------
    # Print tables (optional but useful for debugging)
    # --------------------------------------------------

    for demo, table in distribution_tables.items():
        print(f"\n--- Distribution Table: {demo} ---")
        print(table.to_string())

    # --------------------------------------------------
    # Generate plots
    # --------------------------------------------------

    print("\n--- Generating Distribution Plots ---")

    for demo in demographics:

        path = figures_dir / f"{output_prefix}_distribution_{demo}.png"

        plot_rank_histograms_single_slice_horizontal_grid(
            long_df=df_long,
            variable_name=variable_name,
            value_name=value_name,
            slice_column=demo,
            slice_title=demo.replace("_", " ").title(),
            slice_config=DEMOGRAPHICS_COLUMNS,
            better=better,
            save_path=path,
        )

        print(f"Saved → {path}")

    print("\nPlots generated.")
    print(f"\nDistribution phase complete: {variable_name}\n")


# ==========================================================
# MASTER PHASE RUNNER
# ==========================================================

def run_phase_2_3_part1(df: pd.DataFrame) -> None:

    print("\n=== PHASE 2.3 PART 1: DISTRIBUTIONS ===")

    # Episode ranking distributions
    run_distribution_phase(
        df,
        variable_columns=EPISODE_RANK_COLUMNS,
        variable_name="episode",
        value_name="rank",
        better="low",
        output_prefix="episode",
    )

    # Character rating distributions
    run_distribution_phase(
        df,
        variable_columns=CHARACTER_RATING_COLUMNS,
        variable_name="character",
        value_name="rating",
        better="high",
        output_prefix="character",
    )

    print("\nPhase 2.3 Part 1 complete.\n")