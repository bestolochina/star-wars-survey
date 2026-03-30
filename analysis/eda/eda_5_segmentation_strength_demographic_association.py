# analysis/eda/eda_5_segmentation_strength_demographic_association.py

from __future__ import annotations

from src.io_utils import load_clean_star_wars
from analysis.pipelines.phase5_1_pipeline import run_phase5_1
from analysis.pipelines.phase5_2_pipeline import run_phase5_2
from analysis.pipelines.phase5_3_polarization_analysis_pipeline import run_phase5_3
from analysis.pipelines.phase5_4_pipeline import run_phase5_4
from analysis.pipelines.phase5_5_visualization_pipeline import run_phase5_5
from analysis.pipelines.phase5_6_interpretation_pipeline import run_phase5_6


# ==========================================================
# Phase 5 Controller
# ==========================================================

def main() -> None:

    print("=== PHASE 5: AUDIENCE–NARRATIVE INTERACTION AND IDEOLOGICAL INTERPRETATION ===")

    df = load_clean_star_wars()

    # run_phase5_1(df)

    # run_phase5_2()

    # run_phase5_3()

    # run_phase5_4()

    # run_phase5_5()

    run_phase5_6(df)


if __name__ == "__main__":
    main()
