# analysis/visualization/phase2_2_visualization.py

from __future__ import annotations
from pathlib import Path
from src.paths import FIGURES_DIR
import matplotlib.pyplot as plt
import pandas as pd

from src.io_utils import load_clean_star_wars


def plot_heatmap(
    percent_table: pd.DataFrame,
    *,
    title: str,
    save_path: Path | None = None,
) -> None:
    """
    Plots a heatmap of row-normalized percentages.
    """
    plt.figure(figsize=(6, 5))
    ax = plt.gca()

    im = ax.imshow(percent_table, aspect="auto")

    ax.set_xticks(range(len(percent_table.columns)))
    ax.set_yticks(range(len(percent_table.index)))

    ax.set_xticklabels(percent_table.columns)
    ax.set_yticklabels(percent_table.index)

    plt.xlabel(percent_table.columns.name or "")
    plt.ylabel(percent_table.index.name or "")
    plt.title(title)

    # Annotate cells
    for i in range(percent_table.shape[0]):
        for j in range(percent_table.shape[1]):
            value = percent_table.iloc[i, j]
            ax.text(
                j,
                i,
                f"{value:.1f}%",
                ha="center",
                va="center",
                color="black",
            )

    plt.colorbar(im, fraction=0.046, pad=0.04)
    plt.tight_layout()

    if save_path is not None:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path)

    plt.close()


def plot_nominal_binary(
    percentages: pd.DataFrame,
    *,
    title: str,
    save_path: Path | None = None,
) -> None:
    ax = percentages.plot(
        kind="bar",
        stacked=True,
        figsize=(8, 5),
    )

    ax.set_ylabel("Percentage (%)")
    ax.set_xlabel("")
    ax.set_title(title)

    ax.legend(
        title="",
        loc="lower right",
        bbox_to_anchor=(1, 1.05),
        ncol=1,  # len(percentages.columns),
        # frameon=False,
    )
    ax.set_xticklabels(ax.get_xticklabels(), rotation=20, ha="right")

    # Loop over containers (stacked segments)
    for container in ax.containers:
        # Label only non-zero bars
        labels: list[str] = [
            f"{bar.get_height():.1f}%" if bar.get_height() > 0 else ""
            for bar in container
        ]
        ax.bar_label(container, labels=labels, label_type="center")

    # Handle zero-height bars separately
    for i, col in enumerate(percentages.columns):
        values = percentages[col].values

        for j, value in enumerate(values):
            if value == 0:
                # Total height of the stack at this x-position
                stack_top: float = percentages.iloc[j, :].sum()

                ax.text(
                    j,
                    stack_top + 0.5,
                    "0.0%",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                )

    plt.tight_layout(rect=(0, 0, 1, 0.95))

    if save_path is not None:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path)

    plt.close()
