# analysis/phase2_pipeline.py

import pandas as pd
from dataclasses import dataclass
from src.paths import PHASE2_FIGURES_DIR
from analysis.transforms.reshaping import melt_variable
from analysis.metrics.segmentation_metrics import (
    compute_all_segmentation_metrics,
    build_comparison_table_from_metrics,
    build_all_episode_divergence_tables_from_metrics,
    extract_all_episode_drivers,
)
from analysis.visualization.segmentation_plots import (
    plot_segmentation_comparison,
    plot_episode_divergence_heatmap,
    plot_episode_drivers,
)
from src.config import (
    EPISODE_RANK_COLUMNS,
    CHARACTER_RATING_COLUMNS,
)


# ==========================================================
# DATA CONTAINER
# ==========================================================

@dataclass
class Phase2Data:
    df: pd.DataFrame
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
        df=df,
        episode_long=episode_long,
        character_long=character_long,
    )


# ==========================================================
# MASTER PIPELINE
# ==========================================================

def run_phase_2(df: pd.DataFrame) -> None:

    save_dir = PHASE2_FIGURES_DIR
    save_dir.mkdir(parents=True, exist_ok=True)

    print("\n=== PHASE 2: DEMOGRAPHIC SEGMENTATION ===")

    # 1️⃣ Melt once
    phase2_data = build_phase2_data(df)

    # 2️⃣ Compute segmentation metrics once
    metrics_store = compute_all_segmentation_metrics(
        phase2_data.episode_long
    )

    # 3️⃣ Comparison table
    comparison_table = build_comparison_table_from_metrics(
        metrics_store
    )

    print("\n--- Segmentation Comparison ---")
    print(comparison_table)

    # 4️⃣ Episode divergence tables
    episode_tables = build_all_episode_divergence_tables_from_metrics(
        metrics_store
    )

    print("\n--- Episode Divergence Tables ---")
    for demo, table in episode_tables.items():
        print(f"\n[{demo}]")
        print(table)

    # 5️⃣ Episode drivers
    drivers = extract_all_episode_drivers(
        metrics_store,
        top_n=2,
    )

    print("\n--- Episode Drivers ---")
    for demo, table in drivers.items():
        print(f"\n[{demo}]")
        print(table)

    # ======================================================
    # 6️⃣ VISUALIZATION LAYER
    # ======================================================

    print("\n--- Generating Plots ---")

    plot_segmentation_comparison(
        comparison_table,
        save_dir=save_dir,
    )

    plot_episode_divergence_heatmap(
        metrics_store,
        save_dir=save_dir,
    )

    plot_episode_drivers(
        drivers,
        save_dir=save_dir,
    )

    print(f"\nPlots saved to: {save_dir}")
