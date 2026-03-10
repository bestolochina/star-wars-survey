# analysis/eda/eda_2_3_demographic_slices.py

from __future__ import annotations

import pandas as pd

from src.io_utils import load_clean_star_wars

from analysis.pipelines.phase2_3_pipeline import run_phase_2_3


# ==========================================================
# MAIN
# ==========================================================

def main() -> None:
    df: pd.DataFrame = load_clean_star_wars()

    run_phase_2_3(df)


if __name__ == "__main__":
    main()
