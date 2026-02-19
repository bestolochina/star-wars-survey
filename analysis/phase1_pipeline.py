# analysis/phase1_pipeline.py

import pandas as pd
from typing import List, Literal

from analysis.transforms.reshaping import melt_variable
from analysis.metrics.distribution_metrics import (
    validate_rank_percentage_sums,
    build_all_rank_distribution_tables,
)
from analysis.visualization.rank_histograms import (
    plot_rank_histograms_single_slice_horizontal_grid,
)
from src.paths import FIGURES_DIR, PHASE1_TABLES_DIR
from src.config import (
    DEMOGRAPHICS_COLUMNS,
    EPISODE_RANK_COLUMNS,
)


DEMOGRAPHICS: List[str] = list(DEMOGRAPHICS_COLUMNS.keys())


# ==========================================================
# MASTER PIPELINE
# ==========================================================

def run_phase_1(df: pd.DataFrame) -> None:

    print("\n=== PHASE 1: DISTRIBUTIONAL STRUCTURE ===")

    save_dir = FIGURES_DIR / "phase1"
    save_dir.mkdir(parents=True, exist_ok=True)

    # 1️⃣ Melt episode rankings
    df_long = melt_variable(
        df,
        variable_columns=EPISODE_RANK_COLUMNS,
        variable_name="episode",
        value_name="rank",
    )

    # 2️⃣ Validate rank distributions
    validation = validate_rank_percentage_sums(
        df_long,
        demographic_columns=DEMOGRAPHICS,
        episode_column="episode",
        rank_column="rank",
    )

    print("\n--- Validation Summary ---")
    print(validation["valid"].value_counts().to_string())

    if not validation["valid"].all():
        raise ValueError("Rank percentage validation failed.")

    # 3️⃣ Build distribution tables (report-ready)
    distribution_tables = build_all_rank_distribution_tables(
        df_long,
        episode_column="episode",
        rank_column="rank",
        slice_config=DEMOGRAPHICS_COLUMNS,
    )

    tables_dir = PHASE1_TABLES_DIR
    tables_dir.mkdir(parents=True, exist_ok=True)

    print("\n--- Exporting Phase 1 Tables ---")

    for demo, table in distribution_tables.items():
        table.to_csv(
            tables_dir / f"rank_distribution_{demo}.csv"
        )

    print(f"Phase 1 tables saved to: {tables_dir}")

    # Print tables
    for demo, table in distribution_tables.items():
        print(f"\n--- Distribution Table: {demo} ---")
        print(table.to_string())

    # 4️⃣ Generate histogram grids
    print("\n--- Generating Distribution Plots ---")

    better: Literal["low", "high"] = "low"

    for demo in DEMOGRAPHICS:

        save_path = save_dir / f"episode_distribution_{demo}.png"

        plot_rank_histograms_single_slice_horizontal_grid(
            long_df=df_long,
            variable_name="episode",
            value_name="rank",
            slice_column=demo,
            slice_title=demo.replace("_", " ").title(),
            slice_config=DEMOGRAPHICS_COLUMNS,
            better=better,
            save_path=save_path,
        )

    print(f"\nPhase 1 plots saved to: {save_dir}")
    print("\nPhase 1 complete.\n")
