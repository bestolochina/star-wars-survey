from __future__ import annotations
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
    expected_cols = [False, True, pd.NA]
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
    ax.legend(title="")

    for container in ax.containers:
        ax.bar_label(container, fmt="%.1f%%", label_type="center")

    plt.tight_layout()

    if save_path is not None:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path)

    plt.show()

def main() -> None:
    df = load_clean_star_wars()

    counts, pct = nominal_binary_crosstab(
        df,
        nominal_col="gender",
        binary_col="fan_star_wars",
    )

    plot_nominal_binary(
        pct,
        title="Star Wars Fandom by Gender",
        save_path = FIGURES_DIR /
                    "gender_fan_star_wars.png",
    )

    print("\nCounts:")
    print(counts)

    print("\nRow percentages (%):")
    print(pct)


if __name__ == "__main__":
    main()
