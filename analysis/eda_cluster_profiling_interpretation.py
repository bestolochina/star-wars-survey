# analysis/eda_cluster_profiling_interpretation.py

from __future__ import annotations

from analysis.phase4_pipeline import run_phase4_1
from analysis.phase4_2_pipeline import run_phase4_2
from src.io_utils import load_clean_star_wars
from src.paths import PHASE4_TABLES_DIR


def main() -> None:

    df = load_clean_star_wars()

    # ------------------------------------------------------
    # Respondent cluster assignments (input to Phase 4)
    # ------------------------------------------------------
    respondent_cluster_path = (
        PHASE4_TABLES_DIR
        / "respondent_cluster_assignments.csv"
    )

    # run_phase4_1(df)

    run_phase4_2(df)


if __name__ == "__main__":
    main()