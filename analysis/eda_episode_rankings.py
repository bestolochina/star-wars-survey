from __future__ import annotations
from pathlib import Path
from src.paths import FIGURES_DIR
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D

from src.io_utils import load_clean_star_wars


EPISODE_RANK_COLUMNS: dict[str, str] = {
    "rank_ep1": "Episode I",
    "rank_ep2": "Episode II",
    "rank_ep3": "Episode III",
    "rank_ep4": "Episode IV",
    "rank_ep5": "Episode V",
    "rank_ep6": "Episode VI",
}

def compute_episode_average_scores(df: pd.DataFrame) -> pd.Series:
    ranks = df[list(EPISODE_RANK_COLUMNS.keys())]
    scores = 7 - ranks  # higher = better
    avg_scores = scores.mean()
    avg_scores.index = EPISODE_RANK_COLUMNS.values()
    return avg_scores

def plot_episode_average_scores(
    avg_scores: pd.Series,
    *,
    save_path: Path,
) -> None:
    ax = avg_scores.plot(kind="bar", figsize=(8, 5))

    ax.set_ylabel("Average score (6 = best)")
    ax.set_xlabel("")
    ax.set_title("Average Star Wars Episode Rankings")

    plt.xticks(rotation=0, ha="center")

    for i, value in enumerate(avg_scores):
        ax.text(i, value + 0.05, f"{value:.2f}", ha="center")

    plt.tight_layout()
    save_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path)
    plt.show()

def melt_episode_ranks(df: pd.DataFrame) -> pd.DataFrame:
    long_df = df.melt(
        value_vars=EPISODE_RANK_COLUMNS.keys(),
        var_name="episode",
        value_name="rank",
    )
    long_df["episode"] = long_df["episode"].map(EPISODE_RANK_COLUMNS)

    # IMPORTANT: drop missing rankings
    long_df = long_df.dropna(subset=["rank"])

    return long_df

def plot_episode_rank_violin(
    long_df: pd.DataFrame,
    *,
    save_path: Path,
) -> None:
    ax = plt.figure(figsize=(8, 5)).add_subplot(111)

    data = [
        long_df[long_df["episode"] == ep]["rank"]
        for ep in EPISODE_RANK_COLUMNS.values()
    ]

    parts = ax.violinplot(
        data,
        showmeans=True,
        showmedians=True,
        showextrema=False,
        bw_method=0.1,  # smaller = less smoothing
    )
    parts["cmeans"].set_color("blue")
    parts["cmeans"].set_linewidth(2)

    parts["cmedians"].set_color("red")
    parts["cmedians"].set_linewidth(2)

    ax.set_xticks(range(1, len(EPISODE_RANK_COLUMNS) + 1))
    ax.set_xticklabels(EPISODE_RANK_COLUMNS.values())
    ax.set_ylabel("Rank (1 = best)")
    ax.set_title("Distribution of Episode Rankings")

    legend_elements = [
        Line2D([0], [0], color="red", lw=2, label="Median"),
        Line2D([0], [0], color="blue", lw=2, label="Mean"),
    ]

    ax.legend(
        handles=legend_elements,
        loc="lower right",
        bbox_to_anchor=(1.0, 1.05),
        ncol=1,
        # frameon=False,
    )

    ax.invert_yaxis()  # rank 1 at top → intuitive

    plt.tight_layout()
    save_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path)
    plt.show()

def plot_episode_rank_boxplot(
    long_df: pd.DataFrame,
    *,
    save_path: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))

    long_df.boxplot(
        column="rank",
        by="episode",
        grid=False,
        showfliers=False,
        showmeans=True,
        meanprops=dict(
            marker="^",
            markerfacecolor="blue",
            markeredgecolor="blue",
            markersize=8,
        ),
        medianprops=dict(
            color="red",
            linewidth=2,
        ),
        ax=ax,
    )

    ax.set_ylabel("Rank (1 = best)")
    ax.set_xlabel("")
    ax.set_title("Distribution of Episode Rankings")
    fig.suptitle("")  # remove pandas auto-title

    legend_elements = [
        Line2D([0], [0], color="red", lw=2, label="Median"),
        Line2D(
            [0], [0],
            marker="^",
            color="blue",
            linestyle="None",
            markersize=8,
            label="Mean",
        ),
    ]

    ax.legend(
        handles=legend_elements,
        loc="lower right",
        bbox_to_anchor=(1.0, 1.05),
        ncol=1,
        # frameon=False,
    )

    ax.invert_yaxis()  # rank 1 at top

    plt.tight_layout(rect=(0, 0, 1, 0.95))
    save_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path)
    plt.show()


def compute_rank_frequencies(long_df: pd.DataFrame) -> pd.DataFrame:
    freq = pd.crosstab(
        long_df["episode"],
        long_df["rank"],
        normalize="index",
    ) * 100

    return freq.sort_index(axis=1)

def plot_episode_rank_stacked(
    freq: pd.DataFrame,
    *,
    save_path: Path,
) -> None:
    ax = freq.plot(
        kind="bar",
        stacked=True,
        figsize=(10, 5),
    )

    ax.set_ylabel("Percentage of respondents")
    ax.set_xlabel("")
    ax.set_title("Rank Distribution by Episode")
    plt.xticks(rotation=0, ha="center")

    ax.legend(
        title="Rank",
        loc="lower right",
        bbox_to_anchor=(1.0, 1.05),
        ncol=3,
        # frameon=False,
    )

    for container in ax.containers:
        for bar in container:
            height = bar.get_height()
            if height < 3:  # skip tiny segments
                continue

            x = bar.get_x() + bar.get_width()
            y = bar.get_y() + height / 2

            ax.text(
                x + 0.01,  # slight offset to the right
                y,
                f"{height:.1f}%",
                va="center",
                ha="left",
                fontsize=8,
            )

    plt.tight_layout(rect=(0, 0, 1, 0.95))

    save_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path)
    plt.show()

def main() -> None:
    df = load_clean_star_wars()

    avg_scores = compute_episode_average_scores(df)
    plot_episode_average_scores(
        avg_scores,
        save_path=FIGURES_DIR / "episode_average_scores.png",
    )

    long_df = melt_episode_ranks(df)

    plot_episode_rank_boxplot(
        long_df,
        save_path=FIGURES_DIR / "episode_rank_boxplot.png",
    )

    # plot_episode_rank_violin(
    #     long_df,
    #     save_path=FIGURES_DIR / "episode_rank_violin.png",
    # )

    freq = compute_rank_frequencies(long_df)
    plot_episode_rank_stacked(
        freq,
        save_path=FIGURES_DIR / "episode_rank_stacked.png",
    )


if __name__ == "__main__":
    main()
