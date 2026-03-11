# analysis/pipelines/phase2_1_pipeline.py

from __future__ import annotations

import pandas as pd

from src.paths import PHASE2_TABLES_DIR, PHASE2_FIGURES_DIR
from src.config import DEMOGRAPHICS_COLUMNS, BOOLEAN_COLUMNS

from analysis.metrics.phase2_1_metrics import (
    summarize_boolean_columns,
    summarize_nominal_column,
    compute_episode_average_scores,
    melt_episode_ranks,
)

from analysis.visualization.phase2_1_visualization import (
    plot_boolean_summary,
    plot_nominal_distribution,
    plot_episode_average_scores,
    plot_episode_rank_histograms,
    overall_rating_behavior,
)


# ==========================================================
# BOOLEAN DISTRIBUTIONS
# ==========================================================

def run_boolean_distributions(df: pd.DataFrame) -> None:

    print("\n=== BOOLEAN DISTRIBUTIONS ===")

    tables_dir = PHASE2_TABLES_DIR / "boolean"
    figures_dir = PHASE2_FIGURES_DIR / "boolean"

    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    summary = summarize_boolean_columns(df, BOOLEAN_COLUMNS)

    print("\n--- Boolean Summary ---")
    print(summary)

    path = tables_dir / "boolean_summary.csv"
    summary.to_csv(path)

    print(f"Saved → {path}")

    plot_boolean_summary(
        summary,
        save_path=figures_dir / "boolean_summary.png",
    )

    print("Boolean plots generated.")


# ==========================================================
# NOMINAL DISTRIBUTIONS
# ==========================================================

def run_nominal_distributions(df: pd.DataFrame) -> None:

    print("\n=== NOMINAL DISTRIBUTIONS ===")

    tables_dir = PHASE2_TABLES_DIR / "nominal"
    figures_dir = PHASE2_FIGURES_DIR / "nominal"

    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    for column in DEMOGRAPHICS_COLUMNS:

        summary = summarize_nominal_column(df, column)

        print(f"\n--- {column} ---")
        print(summary)

        path = tables_dir / f"{column}.csv"
        summary.to_csv(path)

        print(f"Saved → {path}")

        plot_nominal_distribution(
            df,
            column,
            save_path=figures_dir / f"{column}.png",
        )

    print("Nominal distributions complete.")


# ==========================================================
# EPISODE PREFERENCES
# ==========================================================

def run_episode_analysis(df: pd.DataFrame) -> None:

    print("\n=== EPISODE PREFERENCE ANALYSIS ===")

    tables_dir = PHASE2_TABLES_DIR / "episodes"
    figures_dir = PHASE2_FIGURES_DIR / "episodes"

    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    avg_scores = compute_episode_average_scores(df)

    print("\n--- Average Episode Scores ---")
    print(avg_scores)

    path = tables_dir / "episode_average_scores.csv"
    avg_scores.to_csv(path)

    print(f"Saved → {path}")

    plot_episode_average_scores(
        avg_scores,
        save_path=figures_dir / "episode_average_scores.png",
    )

    long_df = melt_episode_ranks(df)

    plot_episode_rank_histograms(
        long_df,
        save_path=figures_dir / "episode_rank_histograms.png",
    )

    print("Episode analysis complete.")


# ==========================================================
# CHARACTER FAVORABILITY
# ==========================================================

def run_character_analysis(df: pd.DataFrame) -> None:

    print("\n=== CHARACTER FAVORABILITY ===")

    figures_dir = PHASE2_FIGURES_DIR / "characters"
    figures_dir.mkdir(parents=True, exist_ok=True)

    overall_rating_behavior(
        df,
        save_path=figures_dir / "character_rating_distributions.png",
    )

    print("Character favorability plots generated.")


# ==========================================================
# MASTER PIPELINE
# ==========================================================

def run_phase2_1(df: pd.DataFrame) -> None:

    print("\n=== PHASE 2.1: CORE DISTRIBUTIONS ===")

    run_boolean_distributions(df)
    run_nominal_distributions(df)
    run_episode_analysis(df)
    run_character_analysis(df)

    print("\nPhase 2.1 complete.\n")