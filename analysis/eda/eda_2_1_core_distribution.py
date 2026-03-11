# analysis/eda/eda_2_1_core_distribution.py

from src.io_utils import load_clean_star_wars

from analysis.pipelines.phase2_1_pipeline import run_phase2_1


def main():

    df = load_clean_star_wars()

    run_phase2_1(df)


if __name__ == "__main__":
    main()
