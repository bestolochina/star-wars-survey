# analysis/pipelines/phase2_3_part2_pipeline.py

from __future__ import annotations

from pathlib import Path
import pandas as pd

from src.paths import PHASE2_FIGURES_DIR, PHASE2_TABLES_DIR
from src.config import EPISODE_RANK_COLUMNS, CHARACTER_RATING_COLUMNS

from analysis.transforms.reshaping import melt_variable

from analysis.metrics.segmentation_metrics import (
    compute_all_segmentation_metrics,
    build_comparison_table_from_metrics,
    build_all_variable_divergence_tables_from_metrics,
    extract_all_variable_drivers,
)

from analysis.visualization.phase2_3_part2_plots import (
    plot_segmentation_comparison,
    plot_variable_divergence_heatmap,
    plot_variable_drivers,
    plot_eta_squared_summary,
)

from analysis.metrics.anova_effects import (
    compute_variable_anova_table,
    build_eta_squared_table,
    build_axis_summary,
)

from analysis.metrics.variance_decomposition import (
    build_variance_decomposition_table
)

from analysis.metrics.bootstrap_effects import run_bootstrap_validation


# ==========================================================
# SEGMENTATION PIPELINE
# ==========================================================

def run_segmentation_phase(
    *,
    long_df: pd.DataFrame,
    variable_name: str,
    value_name: str,
    tables_dir: Path,
    figures_dir: Path,
) -> None:

    print(f"\n=== SEGMENTATION: {variable_name.upper()} ===")

    print(f"Rows: {len(long_df):,}")
    print(f"Unique {variable_name}s: {long_df[variable_name].nunique()}")

    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nTables → {tables_dir}")
    print(f"Figures → {figures_dir}")

    # --------------------------------------------------
    # Compute metrics
    # --------------------------------------------------

    metrics_store = compute_all_segmentation_metrics(
        long_df,
        variable_column=variable_name,
        value_column=value_name,
    )

    comparison_table = build_comparison_table_from_metrics(
        metrics_store
    )

    divergence_tables = build_all_variable_divergence_tables_from_metrics(
        metrics_store
    )

    drivers = extract_all_variable_drivers(
        metrics_store,
        top_n=2,
    )

    # --------------------------------------------------
    # Print results
    # --------------------------------------------------

    print("\n--- Segmentation Comparison ---")
    print(comparison_table.to_string())

    print("\n--- Divergence Tables ---")
    for demo, table in divergence_tables.items():
        print(f"\n[{demo}]")
        print(table.to_string())

    print("\n--- Drivers ---")
    for demo, table in drivers.items():
        print(f"\n[{demo}]")
        print(table.to_string())

    # --------------------------------------------------
    # Export tables
    # --------------------------------------------------

    path = tables_dir / "segmentation_strength.csv"
    comparison_table.to_csv(path)
    print(f"Saved → {path}\n")


    for demo, table in divergence_tables.items():
        path = tables_dir / f"divergence_{demo}.csv"
        table.to_csv(path)
        print(f"Saved → {path}\n")

    for demo, table in drivers.items():
        path = tables_dir / f"drivers_{demo}.csv"
        table.to_csv(path, index=False)
        print(f"Saved → {path}\n")

    print("\nTables exported.")

    # --------------------------------------------------
    # Plots
    # --------------------------------------------------

    plot_segmentation_comparison(
        comparison_table,
        save_dir=figures_dir,
    )

    plot_variable_divergence_heatmap(
        metrics_store,
        save_dir=figures_dir,
    )

    plot_variable_drivers(
        drivers,
        save_dir=figures_dir,
    )

    print("Plots generated.")
    print(f"\nSegmentation phase complete: {variable_name}\n")


# ==========================================================
# ANOVA PIPELINE
# ==========================================================

def run_anova_phase(
    *,
    long_df: pd.DataFrame,
    variable_name: str,
    value_name: str,
    tables_dir: Path,
    figures_dir: Path,
) -> None:

    print(f"\n=== ANOVA ANALYSIS: {variable_name.upper()} ===")

    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nTables → {tables_dir}")
    print(f"Figures → {figures_dir}")

    # --------------------------------------------------
    # Compute ANOVA
    # --------------------------------------------------

    anova_results = compute_variable_anova_table(
        long_df,
        variable_column=variable_name,
        value_column=value_name,
    )

    eta_table = build_eta_squared_table(anova_results)

    axis_summary = build_axis_summary(anova_results)

    variance_table = build_variance_decomposition_table(
        anova_results,
        entity_col="variable",
    )

    # --------------------------------------------------
    # Print results
    # --------------------------------------------------

    print("\n--- Variance Decomposition ---")
    print(variance_table.to_string())

    print("\n--- Eta Squared Table ---")
    print(eta_table.to_string())

    print("\n--- Axis Summary ---")
    print(axis_summary.to_string())

    # --------------------------------------------------
    # Export tables
    # --------------------------------------------------

    path_var = tables_dir / "variance_decomposition.csv"
    path_eta = tables_dir / "eta_squared.csv"
    path_axis = tables_dir / "axis_summary.csv"

    variance_table.to_csv(path_var, index=False)
    eta_table.to_csv(path_eta, index=False)
    axis_summary.to_csv(path_axis)

    print(
        f"Saved → {path_var}\n"
        f"        {path_eta}\n"
        f"        {path_axis}\n"
    )

    # --------------------------------------------------
    # Plot
    # --------------------------------------------------

    path = figures_dir / "eta_squared_summary.png"

    plot_eta_squared_summary(
        anova_results,
        save_path=path,
    )

    print(f"Saved → {path}")
    print(f"\nANOVA phase complete: {variable_name}\n")


# ==========================================================
# MASTER PHASE 2 RUNNER
# ==========================================================

def run_phase_2_3_part2(df: pd.DataFrame) -> None:

    print("\n=== PHASE 2: SEGMENTATION & DEMOGRAPHIC EFFECTS ===")

    # --------------------------------------------------
    # Build long data
    # --------------------------------------------------

    print("\nBuilding long-format datasets...")

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

    print(f"Episode rows: {len(episode_long):,}")
    print(f"Character rows: {len(character_long):,}")

    # --------------------------------------------------
    # Segmentation analysis
    # --------------------------------------------------

    run_segmentation_phase(
        long_df=episode_long,
        variable_name="episode",
        value_name="rank",
        tables_dir=PHASE2_TABLES_DIR / "episode",
        figures_dir=PHASE2_FIGURES_DIR / "episode",
    )

    run_segmentation_phase(
        long_df=character_long,
        variable_name="character",
        value_name="rating",
        tables_dir=PHASE2_TABLES_DIR / "character",
        figures_dir=PHASE2_FIGURES_DIR / "character",
    )

    # --------------------------------------------------
    # ANOVA analysis
    # --------------------------------------------------

    run_anova_phase(
        long_df=episode_long,
        variable_name="episode",
        value_name="rank",
        tables_dir=PHASE2_TABLES_DIR / "anova_episode",
        figures_dir=PHASE2_FIGURES_DIR / "anova_episode",
    )

    run_anova_phase(
        long_df=character_long,
        variable_name="character",
        value_name="rating",
        tables_dir=PHASE2_TABLES_DIR / "anova_character",
        figures_dir=PHASE2_FIGURES_DIR / "anova_character",
    )

    # --------------------------------------------------
    # Bootstrap validation
    # --------------------------------------------------

    print("\n=== BOOTSTRAP VALIDATION ===")

    run_bootstrap_validation(
        df=episode_long,
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
    print(
        "Saved →",
        PHASE2_TABLES_DIR / "anova_episode" / "bootstrap_eta_squared.csv"
    )

    run_bootstrap_validation(
        df=character_long,
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
        / "bootstrap_eta_squared.csv",
    )
    print(
        "Saved →",
        PHASE2_TABLES_DIR / "anova_character" / "bootstrap_eta_squared.csv"
    )

    print("\nPhase 2 complete.\n")