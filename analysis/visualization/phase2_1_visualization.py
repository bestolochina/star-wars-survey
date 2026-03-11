# analysis/visualization/phase2_1_visualization.py

from __future__ import annotations

import math

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import numpy as np
from matplotlib.lines import Line2D
from src.config import EPISODE_RANK_COLUMNS, RANK_COLORS, CHARACTER_RATING_COLUMNS
from pandas.api.types import CategoricalDtype


# ==========================================================
# GENERIC BAR DISTRIBUTION
# ==========================================================

def plot_categorical_distribution(
    table: pd.DataFrame,
    title: str,
    save_path,
) -> None:

    plt.figure(figsize=(8, 5))

    table["percent"].plot(
        kind="bar",
    )

    plt.title(title)
    plt.ylabel("Percent")

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig(save_path)

    plt.close()


# ==========================================================
# EPISODE AVERAGE SCORES
# ==========================================================

def plot_episode_scores(
    table: pd.DataFrame,
    save_path,
) -> None:

    plt.figure(figsize=(8, 5))

    table["average_rank"].plot(
        kind="bar",
    )

    plt.title("Average Episode Ranking")
    plt.ylabel("Average Rank")

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig(save_path)

    plt.close()


# ==========================================================
# EPISODE RANK HISTOGRAMS
# ==========================================================

def plot_episode_rank_histograms(
    long_df: pd.DataFrame,
    *,
    save_path: Path,
) -> None:
    """
    Plot rank distributions for each Star Wars episode.

    Each subplot shows:
    - Histogram of ranking positions (1 = best, 6 = worst)
    - Percentage labels above bars
    - Median (solid black line)
    - Mean (dashed blue line)
    - Interquartile Range (IQR) shaded area

    Bars are colored by rank quality (green = best, red = worst).
    """

    # ------------------------------------------------------
    # Prepare episode order and subplot layout
    # ------------------------------------------------------
    episodes = list(EPISODE_RANK_COLUMNS.values())
    n = len(episodes)

    fig, axes = plt.subplots(
        nrows=n,
        ncols=1,
        figsize=(9, 1.5 * n),
        sharex=True,
        sharey=True,
    )

    # Explanation text for color encoding
    fig.text(
        0.01,
        0.01,
        "Bar colors represent ranking quality (green = best, red = worst)",
        fontsize=9,
        alpha=0.7,
    )

    # ------------------------------------------------------
    # Define histogram bins centered on ranks 1–6
    # ------------------------------------------------------
    bins = np.arange(0.5, 7.5, 1)

    # Precompute total responses per episode for percentages
    total_per_episode = long_df.groupby("episode").size()

    # ------------------------------------------------------
    # Plot histogram for each episode
    # ------------------------------------------------------
    for ax, episode in zip(axes, episodes):

        # Extract ranking data for the episode
        data = long_df.loc[long_df["episode"] == episode, "rank"]

        # Plot histogram
        counts, _, bars = ax.hist(
            data,
            bins=bins,
            edgecolor="black",
        )

        # Slightly increase y-limit so labels fit above bars
        ymax = ax.get_ylim()[1]
        ax.set_ylim(0, ymax * 1.06)

        offset = ax.get_ylim()[1] * 0.015

        # --------------------------------------------------
        # Color bars and add percentage labels
        # --------------------------------------------------
        for bar, rank in zip(bars, range(1, 7)):

            # Color bars by rank quality
            bar.set_facecolor(RANK_COLORS[rank])

            # Compute percentage for this rank
            pct = counts[rank - 1] / total_per_episode[episode] * 100

            # Show label only if visible enough
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

        # --------------------------------------------------
        # Summary statistics
        # --------------------------------------------------
        mean = data.mean()
        median = data.median()
        q1, q3 = data.quantile([0.25, 0.75])

        # Interquartile range (middle 50%)
        ax.axvspan(
            q1,
            q3,
            alpha=0.2,
            color="gray",
            label="IQR",
        )

        # Median line
        ax.axvline(
            median,
            linestyle="-",
            linewidth=2,
            color="black",
            alpha=0.8,
            label="Median",
        )

        # Mean line
        ax.axvline(
            mean,
            linestyle="--",
            linewidth=2,
            color="#2b83ba",
            alpha=0.8,
            label="Mean",
        )

        # Episode label on the left
        ax.set_ylabel(
            episode,
            rotation=0,
            labelpad=40,
            va="center",
        )

        # Light horizontal grid
        ax.grid(axis="y", alpha=0.3)

    # ------------------------------------------------------
    # Final axis labels
    # ------------------------------------------------------
    axes[-1].set_xlabel("Rank (1 = best)")

    # ------------------------------------------------------
    # Create a single legend for the entire figure
    # ------------------------------------------------------
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

    # ------------------------------------------------------
    # Title and layout adjustments
    # ------------------------------------------------------
    fig.suptitle("Episode Rank Distributions with Summary Statistics")

    plt.tight_layout(rect=(0, 0, 1, 0.96))

    # Ensure output directory exists
    save_path.parent.mkdir(parents=True, exist_ok=True)

    # Save figure
    plt.savefig(save_path)

    # Display plot
    plt.close()

# ==========================================================
# CHARACTER RATING DISTRIBUTION
# ==========================================================

def plot_character_ratings(
    table: pd.DataFrame,
    save_path,
) -> None:

    plt.figure(figsize=(8, 5))

    table["percent"].plot(
        kind="bar",
    )

    plt.title("Character Rating Distribution")
    plt.ylabel("Percent")

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig(save_path)

    plt.close()


def prepare_boolean_plot_data(summary: pd.DataFrame) -> pd.DataFrame:
    """
    Converts boolean summary table into percentages suitable for plotting.
    """
    return summary[["true_pct", "false_pct", "na_pct"]] * 100


def plot_boolean_summary(
    summary: pd.DataFrame,
    *,
    title: str = "Boolean Variable Distributions",
    save_path: Path | None = None,
) -> None:
    """
    Plots a stacked bar chart of True / False / NA percentages
    for boolean survey variables.
    """
    plot_df: pd.DataFrame = prepare_boolean_plot_data(summary)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax = plot_df.plot(
        kind="bar",
        stacked=True,
        width=0.8,
        ax=ax,
    )

    ax.set_ylabel("Percentage of respondents")
    ax.set_xlabel("Variable")
    ax.set_title(title)

    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Response", loc="lower right", bbox_to_anchor=(1.0, 1.05))

    # --------------------------------------------------
    # Add percentage labels inside bars
    # Hide labels when the value is 0
    # --------------------------------------------------
    for container in ax.containers:
        labels = []
        for value in container.datavalues:
            if value == 0:
                labels.append("")  # hide 0%
            else:
                labels.append(f"{value:.1f}%")

        ax.bar_label(container, labels=labels, label_type="center")

    plt.tight_layout()

    if save_path is not None:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path)

    plt.close()

def value_counts_nominal(series: pd.Series) -> pd.Series:
    """
    Nominal columns:
    - unordered → sort by frequency
    - ordered categoricals → preserve category order
    """
    dtype = series.dtype
    if isinstance(dtype, CategoricalDtype) and dtype.ordered:
        return series.value_counts(dropna=False, sort=False)
    return series.value_counts(dropna=False)


def summarize_nominal_column(
    df: pd.DataFrame,
    column: str,
) -> pd.DataFrame:
    """
    Returns count and percentage table for a nominal column,
    including NaN.
    """
    counts: pd.Series = value_counts_nominal(df[column])
    percentages: pd.Series = counts / counts.sum() * 100

    summary: pd.DataFrame = pd.DataFrame(
        {
            "count": counts,
            "percent": percentages.round(2),
        }
    )

    return summary


def plot_nominal_distribution(
    df: pd.DataFrame,
    column: str,
    *,
    title: str | None = None,
    save_path: Path | None = None,
) -> None:
    """
    Plots a bar chart of a nominal categorical column.
    """
    summary: pd.DataFrame = summarize_nominal_column(df, column)

    plt.figure(figsize=(8, 5))
    ax = summary["count"].plot(kind="bar")

    ax.set_ylabel("Number of respondents")
    ax.set_xlabel(column.replace("_", " ").title())
    ax.set_title(title or f"Distribution of {column}")

    plt.xticks(rotation=45, ha="right")

    for i, value in enumerate(summary["count"]):
        ax.text(i, value, str(value), ha="center", va="bottom")

    plt.tight_layout()

    if save_path is not None:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path)

    plt.close()


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
    plt.close()


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
    plt.close()
