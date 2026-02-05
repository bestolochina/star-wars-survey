from __future__ import annotations
from pathlib import Path
import numpy as np
from src.paths import FIGURES_DIR
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D
from src.io_utils import load_clean_star_wars
import math

CHARACTER_RATING_COLUMNS: dict[str, str] = {
    "rating_han_solo":              "Han Solo",
    "rating_luke_skywalker":        "Luke Skywalker",
    "rating_princess_leia_organa":  "Princess Leia Organa",
    "rating_anakin_skywalker":      "Anakin Skywalker",
    "rating_obi_wan_kenobi":        "Obi Wan Kenobi",
    "rating_emperor_palpatine":     "Emperor Palpatine",
    "rating_darth_vader":           "Darth Vader",
    "rating_lando_calrissian":      "Lando Calrissian",
    "rating_boba_fett":             "Boba Fett",
    "rating_c-3p0":                 "C-3P0",
    "rating_r2_d2":                 "R2-D2",
    "rating_jar_jar_binks":         "Jar-Jar Binks",
    "rating_padme_amidala":         "Padme Amidala",
    "rating_yoda":                  "Yoda",
}
EPISODE_RANK_COLUMNS: dict[str, str] = {
    "rank_ep1": "Episode I",
    "rank_ep2": "Episode II",
    "rank_ep3": "Episode III",
    "rank_ep4": "Episode IV",
    "rank_ep5": "Episode V",
    "rank_ep6": "Episode VI",
}
RANK_COLORS = {
    1: "#1a9641",  # dark green
    2: "#a6d96a",
    3: "#fdae61",
    4: "#f46d43",
    5: "#d73027",
    6: "#a50026",  # dark red
}
GENDER_COLUMNS: dict[str, str] = {
    "Male": "Male",
    "Female": "Female",
}

def overall_rating_behavior(df: pd.DataFrame, save_path: Path) -> None:
    columns = list(CHARACTER_RATING_COLUMNS)

    missing_summary = (
        df[columns]
        .isna()
        .mean()
        .mul(100)
        .round(1)
        .sort_values(ascending=False)
    )

    print("Missing_summary:")
    print(missing_summary)
    print()

    n_cols = 5
    n_rows = math.ceil(len(columns) / n_cols)

    # ---------- Compute global Y max ----------
    global_max = 0
    for column in columns:
        counts = df[column].value_counts(dropna=False)
        global_max = max(global_max, counts.max() * 1.15)

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, 10))
    axes = axes.flatten()

    for i, column in enumerate(columns):
        counts = df[column].value_counts(dropna=False).sort_index()
        percent = counts / counts.sum() * 100

        rating_dist = pd.DataFrame({
            "count": counts,
            "percent": percent.round(1),
        })

        counts.plot(kind="bar", ax=axes[i])
        axes[i].set_title(CHARACTER_RATING_COLUMNS[column])
        axes[i].set_ylim(0, global_max)   # ✅ same Y scale
        axes[i].set_xlabel("")
        axes[i].set_ylabel("Count")

        # ✅ Centered x tick labels
        axes[i].set_xticklabels(axes[i].get_xticklabels(), rotation=0, ha="center")

        # ✅ Color last bar (NA) gray
        for label, bar in zip(axes[i].get_xticklabels(), axes[i].patches):
            if not label.get_text().isdigit():
                bar.set_color("lightgray")

        # ✅ Add value labels on bars
        for container in axes[i].containers:
            axes[i].bar_label(container, fmt="%d", label_type="edge", padding=2)

        print(f"\n{column}")
        print(rating_dist)

    # Remove unused axes
    for j in range(len(columns), len(axes)):
        fig.delaxes(axes[j])

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

def plot_episode_rank_histograms(
    long_df: pd.DataFrame,
    *,
    save_path: Path,
) -> None:
    episodes = list(EPISODE_RANK_COLUMNS.values())
    n = len(episodes)

    fig, axes = plt.subplots(
        nrows=n,
        ncols=1,
        figsize=(9, 1.5 * n),
        sharex=True,
        sharey=True,
    )

    fig.text(
        0.01, 0.01,
        "Bar colors represent ranking quality (green = best, red = worst)",
        fontsize=9,
        alpha=0.7,
    )

    bins = np.arange(0.5, 7.5, 1)
    total_per_episode = long_df.groupby("episode").size()

    for ax, episode in zip(axes, episodes):
        data = long_df.loc[long_df["episode"] == episode, "rank"]
        counts, _, bars = ax.hist(
            data,
            bins=bins,
            edgecolor="black",
        )

        ymax = ax.get_ylim()[1]
        ax.set_ylim(0, ymax * 1.06)

        offset = ax.get_ylim()[1] * 0.015

        # recolor bars by rank
        for bar, rank in zip(bars, range(1, 7)):
            bar.set_facecolor(RANK_COLORS[rank])

            pct = counts[rank - 1] / total_per_episode[episode] * 100
            if pct >= 3:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + offset,
                    f"{pct:.1f}%",
                    ha="center",
                    va="bottom",
                    fontsize=8,
                    bbox=dict(
                        boxstyle="round,pad=0.2",
                        facecolor="white",
                        edgecolor="none",
                        alpha=0.8,
                    ),
                )

        # statistics
        mean = data.mean()
        median = data.median()
        q1, q3 = data.quantile([0.25, 0.75])

        ax.axvspan(q1, q3, alpha=0.2, color="gray", label="IQR")
        ax.axvline(median, linestyle="-", linewidth=2, color="black", alpha=0.8, label="Median",)
        ax.axvline(mean, linestyle="--", linewidth=2, color="#2b83ba", alpha=0.8, label="Mean",)

        ax.set_ylabel(episode, rotation=0, labelpad=40, va="center")
        ax.grid(axis="y", alpha=0.3)

    axes[-1].set_xlabel("Rank (1 = best)")

    # single legend (top-right)
    handles = [
        plt.Line2D([0], [0], color="black", linestyle="-", linewidth=2, label="Median"),
        plt.Line2D([0], [0], color="#2b83ba", linestyle="--", linewidth=2, label="Mean"),
        plt.Rectangle((0, 0), 1, 1, color="gray", alpha=0.2, label="IQR"),
    ]

    fig.legend(
        handles=handles,
        loc="upper right",
        bbox_to_anchor=(0.98, 0.98),
    )

    fig.suptitle("Episode Rank Distributions with Summary Statistics")
    plt.tight_layout(rect=(0, 0, 1, 0.96))

    save_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path)
    plt.show()

def episode_rank_gender(
    df: pd.DataFrame,
    *,
    save_path: Path,
) -> None:
    columns = list(GENDER_COLUMNS)


def main() -> None:
    df = load_clean_star_wars()

    episode_rank_gender(df, save_path=FIGURES_DIR / "episode_rank_gender.png")

    long_df = melt_episode_ranks(df)

    # overall_rating_behavior(df, save_path=FIGURES_DIR / "character_rating_distributions.png")


if __name__ == "__main__":
    main()
