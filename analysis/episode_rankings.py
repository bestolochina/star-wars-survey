from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from src.io_utils import load_clean_star_wars


EPISODE_COLUMNS: list[str] = [
    "rank_ep1",
    "rank_ep2",
    "rank_ep3",
    "rank_ep4",
    "rank_ep5",
    "rank_ep6",
]

EPISODE_LABELS: list[str] = [
    "Ep I",
    "Ep II",
    "Ep III",
    "Ep IV",
    "Ep V",
    "Ep VI",
]


def compute_episode_scores(df: pd.DataFrame) -> pd.Series:
    """
    Compute average episode scores from ranking columns.
    Higher score = more preferred episode.
    """
    avg_scores: pd.Series = (7 - df[EPISODE_COLUMNS]).mean()
    avg_scores.index = EPISODE_LABELS
    return avg_scores


def plot_episode_scores(
    avg_scores: pd.Series,
    *,
    title: str = "Average Scores of Star Wars Episodes",
    save_path: Path | None = None,
) -> None:
    """
    Plot average episode scores as a bar chart.
    """
    plt.figure(figsize=(8, 5))
    ax = avg_scores.plot(kind="bar")

    ax.set_ylabel("Average Score (6 = best, 1 = worst)")
    ax.set_xlabel("Star Wars Episode")
    ax.set_title(title)

    plt.xticks(rotation=0, ha="center")

    for i, value in enumerate(avg_scores):
        ax.text(i, value + 0.05, f"{value:.2f}", ha="center", va="bottom")

    plt.tight_layout()

    if save_path is not None:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path)

    plt.show()


def run_episode_rankings_eda() -> None:
    df: pd.DataFrame = load_clean_star_wars()
    avg_scores: pd.Series = compute_episode_scores(df)

    plot_episode_scores(
        avg_scores,
        save_path=Path("analysis/figures/episode_scores.png"),
    )


def main() -> None:
    run_episode_rankings_eda()


if __name__ == "__main__":
    main()
