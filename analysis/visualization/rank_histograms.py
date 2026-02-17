# analysis/visualization/rank_histograms.py

from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from typing import Literal
from src.config import RANK_COLORS

def plot_rank_histograms_single_slice_horizontal_grid(
    long_df: pd.DataFrame,
    *,
    variable_name: str,
    value_name: str,
    slice_column: str,
    slice_title: str,
    slice_config: dict[str, dict[str, str]],
    better: Literal["low", "high"],
    ncols: int | None = None,
    save_path: Path,
) -> None:
    """
    Plot horizontal histograms (percentage-normalized) in a flat grid
    for one slice dimension.
    """

    # -------------------------
    # 1. Validate slice column
    # -------------------------
    if slice_column not in slice_config:
        raise ValueError(
            f"Unknown slice column '{slice_column}'. "
            f"Available options: {list(slice_config.keys())}"
        )

    # -----------------------------------------
    # 2. Resolve slice ordering & display names
    # -----------------------------------------
    slice_map = slice_config[slice_column]
    slices = list(slice_map.keys())

    # -----------------------------------------
    # 3. Determine which variables to plot
    # -----------------------------------------
    variables = long_df[variable_name].dropna().unique().tolist()

    # -----------------------------------------
    # 4. Build plotting grid layout
    # -----------------------------------------
    cells: list[tuple[str, str]] = [
        (variable, raw_value)
        for variable in variables
        for raw_value in slices
    ]

    n_cells = len(cells)

    if ncols is None:
        ncols = len(slices)

    nrows = int(np.ceil(n_cells / ncols))

    fig, axes = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        figsize=(2.2 * ncols, 3.2 * nrows),
        sharex=True,
        sharey=True,
    )

    axes = np.asarray(axes).reshape(nrows, ncols)

    fig.text(
        0.01, 0.01,
        "Bar colors represent quality (green = best, red = worst)",
        fontsize=9,
        alpha=0.7,
    )

    # -----------------------------------------
    # 5. Histogram bins (auto-detect ranks)
    # -----------------------------------------
    min_val = int(long_df[value_name].min())
    max_val = int(long_df[value_name].max())
    bins = np.arange(min_val - 0.5, max_val + 1.5, 1)

    # -----------------------------------------
    # 6. Plot each histogram cell
    # -----------------------------------------
    for ax, (variable, raw_value) in zip(axes.flat, cells):

        slice_df = long_df.loc[long_df[slice_column] == raw_value]
        data = slice_df.loc[slice_df[variable_name] == variable, value_name]
        total = len(data)

        if total == 0:
            ax.text(
                0.5, 0.5,
                "No data",
                ha="center",
                va="center",
                transform=ax.transAxes,
                fontsize=9,
                alpha=0.6,
            )
            ax.grid(axis="x", alpha=0.3)
            continue

        # ✅ NORMALIZE TO PERCENTAGES
        weights = np.ones_like(data) / total * 100

        counts, _, bars = ax.hist(
            data,
            bins=bins,
            weights=weights,
            edgecolor="black",
            orientation="horizontal",
        )

        # ✅ FIXED SCALE FOR ALL SUBPLOTS
        ax.set_xlim(0, 100)
        offset = 2

        # ---------------------------------
        # Color + Percentage Labels
        # ---------------------------------
        for bar, value in zip(bars, range(min_val, max_val + 1)):

            if better == "low":
                color_key = value
            elif better == "high":
                color_key = max_val - value + 1
            else:
                raise ValueError("better must be either 'low' or 'high'")

            bar.set_facecolor(RANK_COLORS[color_key])

            pct = counts[value - min_val]

            if pct >= 3:
                ax.text(
                    bar.get_width() + offset,
                    bar.get_y() + bar.get_height() / 2,
                    f"{pct:.1f}%",
                    va="center",
                    ha="left",
                    fontsize=8,
                    bbox=dict(
                        boxstyle="round,pad=0.1",
                        facecolor="white",
                        edgecolor="none",
                        alpha=0.8,
                    ),
                )

        # ---------------------------------
        # Distribution statistics
        # ---------------------------------
        mean = data.mean()
        median = data.median()
        q1, q3 = data.quantile([0.25, 0.75])

        ax.axhspan(q1, q3, alpha=0.2, color="gray")
        ax.axhline(median, linestyle="-", linewidth=2, color="black", alpha=0.8)
        ax.axhline(mean, linestyle="--", linewidth=2, color="#2b83ba", alpha=0.8)

        if better == "low":
            ax.invert_yaxis()

        n = len(data)
        ax.set_title(
            f"{variable} — \n{slice_map[raw_value]} \n(n={n})",
            fontsize=9,
        )
        ax.grid(axis="x", alpha=0.3)

    # -----------------------------------------
    # 7. Turn off unused axes
    # -----------------------------------------
    for ax in axes.flat[len(cells):]:
        ax.axis("off")

    # -----------------------------------------
    # 8. Global labels & legend
    # -----------------------------------------
    fig.supxlabel("Percentage of responses (0–100%)")

    if better == "low":
        fig.supylabel(f"{value_name.title()} (1 = best)")
    else:
        fig.supylabel(f"{value_name.title()} (higher = better)")

    handles = [
        plt.Line2D([0], [0], color="black", linestyle="-", linewidth=2, label="Median"),
        plt.Line2D([0], [0], color="#2b83ba", linestyle="--", linewidth=2, label="Mean"),
        plt.Rectangle((0, 0), 1, 1, color="gray", alpha=0.2, label="IQR"),
    ]

    fig.legend(handles=handles, loc="upper right", bbox_to_anchor=(0.98, 1), ncol=2)

    fig.suptitle(f"{variable_name.title()} Distributions by {slice_title}")
    plt.tight_layout(rect=(0, 0, 1, 0.96))

    save_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path)
    plt.show()
