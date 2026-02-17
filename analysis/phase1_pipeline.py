# analysis/phase1_pipeline.py

import pandas as pd
from typing import List, Literal

from analysis.transforms.reshaping import melt_variable
from src.paths import FIGURES_DIR
from src.config import DEMOGRAPHICS_COLUMNS, EPISODE_RANK_COLUMNS

from analysis.visualization.rank_histograms import (
    plot_rank_histograms_single_slice_horizontal_grid,
)
from analysis.metrics.distribution_metrics import (
    sanity_check_rank_percentages_multi,
)

DEMOGRAPHICS: List[str] = list(DEMOGRAPHICS_COLUMNS.keys())


def run_phase_1(df: pd.DataFrame) -> None:

    print("\n--- Phase 1: Distributional Structure ---\n")

    save_dir = FIGURES_DIR / "phase1"
    save_dir.mkdir(parents=True, exist_ok=True)

    variable_columns = EPISODE_RANK_COLUMNS
    variable_name = "episode ranking"
    value_name = "rank"
    better: Literal["low", "high"] = "low"

    df_long = melt_variable(
        df,
        variable_columns=variable_columns,
        variable_name=variable_name,
        value_name=value_name,
    )

    for demo in DEMOGRAPHICS:

        print(f"Generating histogram grid for {demo}...")

        save_path = save_dir / f"episode_ranking_{demo}.png"

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

    sanity_check_rank_percentages_multi(
        df_long,
        demographic_columns=DEMOGRAPHICS,
        episode_column=variable_name,
        rank_column=value_name,
    )

    print("\nPhase 1 complete.\n")
