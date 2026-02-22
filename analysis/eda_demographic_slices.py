# analysis/eda_demographic_slices.py

from __future__ import annotations

import pandas as pd

from src.io_utils import load_clean_star_wars

from analysis.phase1_pipeline import run_phase_1
from analysis.phase2_pipeline import run_phase_2


# ==========================================================
# MAIN
# ==========================================================

def main() -> None:
    df: pd.DataFrame = load_clean_star_wars()

    # run_phase_1(df)

    run_phase_2(df)


if __name__ == "__main__":
    main()
