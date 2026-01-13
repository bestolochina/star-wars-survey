from src.io_utils import load_clean_star_wars
import matplotlib.pyplot as plt
import pandas as pd


def compute_episode_scores(df: pd.DataFrame) -> pd.Series:
    EPISODE_ORDER: list[str] = [
        "rank_ep1",
        "rank_ep2",
        "rank_ep3",
        "rank_ep4",
        "rank_ep5",
        "rank_ep6",
    ]

    avg_scores: pd.Series = (7 - df[EPISODE_ORDER]).mean()
    avg_scores.index = ["Ep I", "Ep II", "Ep III", "Ep IV", "Ep V", "Ep VI"]
    return avg_scores


def plot_episode_scores_bar(avg_scores: pd.Series) -> None:
    plt.figure(figsize=(8, 5))
    ax = avg_scores.plot(kind="bar")

    plt.ylabel("Average Score (6 = best, 1 = worst)")
    plt.xlabel("Star Wars Episode")
    plt.title("Average Scores of Star Wars Episodes")

    plt.xticks(rotation=0, ha="center")

    # Add value labels on top of bars
    for i, value in enumerate(avg_scores):
        ax.text(i, value + 0.05, f"{value:.2f}", ha="center", va="bottom")

    plt.tight_layout()
    plt.show()

def episode_scores(df: pd.DataFrame) -> None:
    avg_scores: pd.Series = compute_episode_scores(df)
    plot_episode_scores_bar(avg_scores)


def main() -> None:
    df: pd.DataFrame = load_clean_star_wars()
    episode_scores(df)


if __name__ == "__main__":
    main()
