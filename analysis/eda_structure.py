# analysis/eda_structure.py

from __future__ import annotations

import pandas as pd

from analysis.phase3_pipeline import run_phase3_correlation
from src.io_utils import load_clean_star_wars


def main() -> None:

    print("=== PHASE 3: STRUCTURAL MODELING ===")

    df = load_clean_star_wars()

    run_phase3_correlation(
        df,
        respondent_id="respondent_id",  # change if needed
    )

    print("\nPhase 3 step 3.1.1 complete.")


if __name__ == "__main__":
    main()
