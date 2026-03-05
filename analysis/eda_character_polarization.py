# analysis/eda_character_polarization.py

from __future__ import annotations

import pandas as pd

from src.io_utils import load_clean_star_wars
from analysis.phase4_3_pipeline import run_phase4_3


# ==========================================================
# Phase 4.3 Controller
# ==========================================================

def main() -> None:

    print("=== PHASE 4.3: CHARACTER POLARIZATION ANALYSIS ===")

    df = load_clean_star_wars()

    run_phase4_3(df)


if __name__ == "__main__":
    main()