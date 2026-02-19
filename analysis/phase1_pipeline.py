# analysis/phase1_pipeline.py

from __future__ import annotations

import pandas as pd
from typing import List, Literal

from analysis.transforms.reshaping import melt_variable
from analysis.metrics.distribution_metrics import (
    validate_ordinal_percentage_sums,
    build_all_ordinal_distribution_tables,
)
from analysis.visualization.rank_histograms import (
    plot_rank_histograms_single_slice_horizontal_grid,
)
from src.paths import FIGURES_DIR, PHASE1_TABLES_DIR
from src.config import DEMOGRAPHICS_COLUMNS


# ==========================================================
# GENERIC DISTRIBUTION PIPELINE
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
    """
    Generic distribution analysis pipeline.

    Parameters
    ----------
    df : pd.DataFrame
        Clean survey dataframe.

    variable_columns : List[str]
        Columns representing ranking/rating variables.

    variable_name : str
        Name for melted variable column (e.g. "episode", "character").

    value_name : str
        Name for value column (e.g. "rank", "rating").

    better : Literal["low", "high"]
        Indicates whether lower or higher values are better.

    output_prefix : str
        Used for naming output files (e.g. "episode", "character").
    """

    print(f"\n=== DISTRIBUTION PHASE: {variable_name.upper()} ===")

    save_dir = FIGURES_DIR / "phase1" / output_prefix
    save_dir.mkdir(parents=True, exist_ok=True)

    tables_dir = PHASE1_TABLES_DIR / output_prefix
    tables_dir.mkdir(parents=True, exist_ok=True)

    demographics: List[str] = list(DEMOGRAPHICS_COLUMNS.keys())

    # 1️⃣ Melt variable
    df_long = melt_variable(
        df,
        variable_columns=variable_columns,
        variable_name=variable_name,
        value_name=value_name,
    )

    # 2️⃣ Validate percentage sums
    validation = validate_ordinal_percentage_sums(
        df_long,
        demographic_columns=demographics,
        episode_column=variable_name,
        rank_column=value_name,
    )

    print("\n--- Validation Summary ---")
    print(validation["valid"].value_counts().to_string())

    if not validation["valid"].all():
        raise ValueError(
            f"{variable_name} percentage validation failed."
        )

    # 3️⃣ Build distribution tables
    distribution_tables = build_all_ordinal_distribution_tables(
        df_long,
        episode_column=variable_name,
        rank_column=value_name,
        slice_config=DEMOGRAPHICS_COLUMNS,
    )

    print("\n--- Exporting Distribution Tables ---")

    for demo, table in distribution_tables.items():
        table.to_csv(
            tables_dir / f"{output_prefix}_distribution_{demo}.csv"
        )

    print(f"Tables saved to: {tables_dir}")

    # Print tables
    for demo, table in distribution_tables.items():
        print(f"\n--- Distribution Table: {demo} ---")
        print(table.to_string())

    # 4️⃣ Generate histogram grids
    print("\n--- Generating Distribution Plots ---")

    for demo in demographics:

        save_path = (
            save_dir / f"{output_prefix}_distribution_{demo}.png"
        )

        plot_rank_histograms_single_slice_horizontal_grid(
            long_df=df_long,
            variable_name=variable_name,
            value_name=value_name,
            slice_column=demo,
            slice_title=demo.replace("_", " ").title(),
            slice_config=DEMOGRAPHICS_COLUMNS,
            better=better,
            save_path=save_path,
        )

    print(f"\nPlots saved to: {save_dir}")
    print(f"\nDistribution phase for {variable_name} complete.\n")
