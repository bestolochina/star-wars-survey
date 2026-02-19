# analysis/eda_demographic_slices.py

from __future__ import annotations

import pandas as pd

from src.io_utils import load_clean_star_wars
from src.config import (
    EPISODE_RANK_COLUMNS,
    CHARACTER_RATING_COLUMNS,
)

from analysis.phase1_pipeline import run_distribution_phase
from analysis.phase2_pipeline import run_phase_2


# ==========================================================
# MAIN
# ==========================================================

def main() -> None:
    df: pd.DataFrame = load_clean_star_wars()

    # ======================================================
    # PHASE 1 — DISTRIBUTIONAL STRUCTURE
    # ======================================================

    # 🎬 Episode Ranking Distribution
    run_distribution_phase(
        df,
        variable_columns=EPISODE_RANK_COLUMNS,
        variable_name="episode",
        value_name="rank",
        better="low",          # lower rank = better
        output_prefix="episode",
    )

    # ⭐ Character Rating Distribution
    run_distribution_phase(
        df,
        variable_columns=CHARACTER_RATING_COLUMNS,
        variable_name="character",
        value_name="rating",
        better="high",         # higher rating = better
        output_prefix="character",
    )

    # ======================================================
    # PHASE 2 — SEGMENTATION
    # (still episode-only for now)
    # ======================================================

    run_phase_2(df)


if __name__ == "__main__":
    main()
