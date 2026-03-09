# analysis/eda_cluster_profiling_interpretation.py

from __future__ import annotations

from analysis.phase4_1_pipeline import run_phase4_1
from analysis.phase4_2_pipeline import run_phase4_2
from src.io_utils import load_clean_star_wars


def main() -> None:

    df = load_clean_star_wars()

    # ------------------------------------------------------
    # Respondent cluster assignments (input to Phase 4)
    # ------------------------------------------------------

    # run_phase4_1(df)

    run_phase4_2(df)


if __name__ == "__main__":
    main()