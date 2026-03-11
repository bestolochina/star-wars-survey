# analysis/pipelines/phase2_2_pipeline.py

from __future__ import annotations

import pandas as pd

from src.paths import PHASE2_FIGURES_DIR, PHASE2_TABLES_DIR

from analysis.metrics.phase2_2_metrics import (
    contingency_table,
    row_percentages,
    nominal_binary_crosstab,
)

from analysis.visualization.phase2_2_visualization import (
    plot_heatmap,
    plot_nominal_binary,
)

from src.config import DEMOGRAPHICS_COLUMNS


# ==========================================================
# BINARY × BINARY
# ==========================================================

def run_binary_binary_analysis(df: pd.DataFrame) -> None:

    print("\n=== BINARY × BINARY ANALYSIS ===")

    figures_dir = PHASE2_FIGURES_DIR / "binary_binary"
    tables_dir = PHASE2_TABLES_DIR / "binary_binary"

    figures_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nTables → {tables_dir}")
    print(f"Figures → {figures_dir}")

    binary_pairs = [
        ("seen_star_wars", "fan_star_wars"),
        ("fan_star_wars", "fan_star_trek"),
        ("seen_star_wars", "fan_star_trek"),
    ]

    for col_a, col_b in binary_pairs:

        print(f"\n--- {col_a} × {col_b} ---")

        counts = contingency_table(df, col_a, col_b)
        percents = row_percentages(counts)

        print("\nCounts:")
        print(counts)

        print("\nRow %:")
        print(percents.round(1))

        counts_path = tables_dir / f"{col_a}_vs_{col_b}_counts.csv"
        perc_path = tables_dir / f"{col_a}_vs_{col_b}_percent.csv"

        counts.to_csv(counts_path)
        percents.to_csv(perc_path)

        print(f"Saved → {counts_path}")
        print(f"Saved → {perc_path}")

        fig_path = figures_dir / f"{col_a}_vs_{col_b}.png"

        plot_heatmap(
            percents,
            title=f"{col_a} × {col_b}",
            save_path=fig_path,
        )

        print(f"Saved → {fig_path}")


# ==========================================================
# NOMINAL × BINARY
# ==========================================================

def run_nominal_binary_analysis(df: pd.DataFrame) -> None:

    print("\n=== NOMINAL × BINARY ANALYSIS ===")

    figures_dir = PHASE2_FIGURES_DIR / "nominal_binary"
    tables_dir = PHASE2_TABLES_DIR / "nominal_binary"

    figures_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nTables → {tables_dir}")
    print(f"Figures → {figures_dir}")

    binary_columns = [
        ("fan_star_wars", "Star Wars Fandom"),
        ("fan_star_trek", "Star Trek Fandom"),
    ]

    nominal_columns = list(DEMOGRAPHICS_COLUMNS.keys())

    for bin_col, bin_title in binary_columns:
        for nom_col in nominal_columns:

            print(f"\n--- {nom_col} × {bin_col} ---")

            counts, pct = nominal_binary_crosstab(
                df,
                nominal_col=nom_col,
                binary_col=bin_col,
            )

            print("\nCounts:")
            print(counts)

            print("\nRow %:")
            print(pct.round(1))

            counts_path = tables_dir / f"{nom_col}_vs_{bin_col}_counts.csv"
            pct_path = tables_dir / f"{nom_col}_vs_{bin_col}_percent.csv"

            counts.to_csv(counts_path)
            pct.to_csv(pct_path)

            print(f"Saved → {counts_path}")
            print(f"Saved → {pct_path}")

            fig_path = figures_dir / f"{nom_col}_vs_{bin_col}.png"

            plot_nominal_binary(
                pct,
                title=f"{bin_title} by {nom_col}",
                save_path=fig_path,
            )

            print(f"Saved → {fig_path}")


# ==========================================================
# MASTER PIPELINE
# ==========================================================

def run_phase2_2(df: pd.DataFrame) -> None:

    print("\n======================================")
    print("PHASE 2.2 — CROSS METRICS")
    print("======================================")

    run_binary_binary_analysis(df)
    run_nominal_binary_analysis(df)

    print("\nPhase 2.2 complete.\n")