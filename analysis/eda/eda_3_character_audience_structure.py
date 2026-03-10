# analysis/eda/eda_3_character_audience_structure.py

from __future__ import annotations

from analysis.pipelines.phase3_pipeline import run_phase3
from src.io_utils import load_clean_star_wars


def main() -> None:

    df = load_clean_star_wars()

    run_phase3(df)


if __name__ == "__main__":
    main()
