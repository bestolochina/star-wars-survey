# analysis/eda/eda_2_2_cross_metrics.py

from src.io_utils import load_clean_star_wars

from analysis.pipelines.phase2_2_pipeline import run_phase2_2


def main():

    df = load_clean_star_wars()

    run_phase2_2(df)


if __name__ == "__main__":
    main()
