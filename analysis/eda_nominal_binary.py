from __future__ import annotations
from pathlib import Path
from src.paths import FIGURES_DIR
import pandas as pd
from src.io_utils import load_clean_star_wars
import matplotlib.pyplot as plt


def nominal_binary_crosstab(
    df: pd.DataFrame,
    nominal_col: str,
    binary_col: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Returns:
    - count table
    - row-wise percentage table
    """
    counts: pd.DataFrame = pd.crosstab(
        df[nominal_col],
        df[binary_col],
        dropna=False,
        normalize=False
    )
    expected_cols = [True, False, pd.NA]
    counts = counts.reindex(
        columns=[c for c in expected_cols if c in counts.columns],
        fill_value=0,
    )

    percentages: pd.DataFrame = (
        counts.div(counts.sum(axis=1), axis=0) * 100
    ).round(1)

    return counts, percentages


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

    plt.show()

def main() -> None:
    df = load_clean_star_wars()

    binary_columns = [
        ("fan_star_wars", "Star Wars Fandom"),
        ("fan_star_trek", "Star Trek Fandom"),
    ]

    nominal_columns = [
        ("gender", "Gender"),
        ("education_level", "Education Level"),
        ("household_income", "Household Income Level"),
        ("census_region", "Census Region"),
        ("age_group", "Age Group"),
    ]

    for bin_col, bin_title in binary_columns:
        for nom_col, nom_title in nominal_columns:

            title = bin_title + " by " + nom_title
            save_path = FIGURES_DIR / f"{nom_col}_{bin_col}.png"
            counts, pct = nominal_binary_crosstab(
                df,
                nominal_col=nom_col,
                binary_col=bin_col,
            )

            plot_nominal_binary(
                pct,
                title=title,
                save_path=save_path,
            )

            print("\nCounts:")
            print(counts)

            print("\nRow percentages (%):")
            print(pct)


if __name__ == "__main__":
    main()
