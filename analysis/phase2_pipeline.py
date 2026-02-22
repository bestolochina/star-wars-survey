# analysis/phase2_pipeline.py

from __future__ import annotations

import pandas as pd
from dataclasses import dataclass

from src.paths import PHASE2_FIGURES_DIR, PHASE2_TABLES_DIR
from src.config import EPISODE_RANK_COLUMNS, CHARACTER_RATING_COLUMNS

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
from analysis.metrics.anova_effects import (
    compute_variable_anova_table,
    build_eta_squared_table,
    build_axis_summary,
)
from analysis.visualization.anova_plots import plot_eta_squared_summary
from analysis.metrics.variance_decomposition import build_variance_decomposition_table
from analysis.metrics.bootstrap_effects import run_bootstrap_validation


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
# ANOVA EFFECT ANALYSIS
# ==========================================================

def run_anova_phase(
    *,
    long_df: pd.DataFrame,
    variable_name: str,
    value_name: str,
    output_prefix: str,
) -> None:

    print(f"\n=== ANOVA EFFECT ANALYSIS: {variable_name.upper()} ===")

    tables_dir = PHASE2_TABLES_DIR / output_prefix
    tables_dir.mkdir(parents=True, exist_ok=True)

    figures_dir = PHASE2_FIGURES_DIR / output_prefix
    figures_dir.mkdir(parents=True, exist_ok=True)

    # 1️⃣ Compute ANOVA
    anova_results = compute_variable_anova_table(
        long_df,
        variable_column=variable_name,
        value_column=value_name,
    )

    # 2️⃣ Tables
    eta_table = build_eta_squared_table(anova_results)
    axis_summary = build_axis_summary(anova_results)

    # 3️⃣ Variance decomposition
    variance_table = build_variance_decomposition_table(
        anova_results,
        entity_col="variable",
    )

    print("\n--- Variance Decomposition ---")
    print(variance_table.to_string())

    variance_table.to_csv(
        tables_dir / "variance_decomposition.csv",
        index=False,
    )

    print("\n--- Eta Squared Table ---")
    print(eta_table.to_string())

    print("\n--- Axis Summary ---")
    print(axis_summary.to_string())

    eta_table.to_csv(
        tables_dir / "eta_squared.csv",
        index=False,
    )

    axis_summary.to_csv(
        tables_dir / "axis_summary.csv",
    )

    # 4️⃣ Plot
    plot_eta_squared_summary(
        anova_results,
        save_path=figures_dir / "eta_squared_summary.png",
    )

    print(f"\nANOVA results saved to: {tables_dir}")


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

    # Episode ANOVA
    run_anova_phase(
        long_df=phase2_data.episode_long,
        variable_name="episode",
        value_name="rank",
        output_prefix="anova_episode",
    )

    # Character ANOVA
    run_anova_phase(
        long_df=phase2_data.character_long,
        variable_name="character",
        value_name="rating",
        output_prefix="anova_character",
    )

    run_bootstrap_validation(
        df=phase2_data.episode_long,
        entity_col="episode",
        value_col="rank",
        axes=["age_group", "gender"],
        top_entities=[
            "Episode I",
            "Episode IV",
            "Episode III",
        ],
        save_path=PHASE2_TABLES_DIR
                  / "anova_episode"
                  / "bootstrap_eta_squared.csv",
    )

    run_bootstrap_validation(
        df=phase2_data.character_long,
        entity_col="character",
        value_col="rating",
        axes=["age_group", "gender"],
        top_entities=[
            "Anakin Skywalker",
            "Luke Skywalker",
            "Jar-Jar Binks",
        ],
        save_path=PHASE2_TABLES_DIR
                  / "anova_character"
                  / "bootstrap_eta_squared.csv"
    )

