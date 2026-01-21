from __future__ import annotations
from src.paths import FIGURES_DIR
import matplotlib.pyplot as plt
import pandas as pd

from src.io_utils import load_clean_star_wars


# -------------------------
# Core computation
# -------------------------

def contingency_table(
    df: pd.DataFrame,
    col_a: str,
    col_b: str,
) -> pd.DataFrame:
    """
    Returns a contingency table (counts) including NaN.
    """
    return pd.crosstab(
        df[col_a],
        df[col_b],
        dropna=False,
    )


def row_percentages(table: pd.DataFrame) -> pd.DataFrame:
    """
    Returns row-normalized percentages.
    """
    return table.div(table.sum(axis=1), axis=0) * 100


# -------------------------
# Plotting
# -------------------------

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

    plt.show()


# -------------------------
# Analysis runner
# -------------------------

def analyze_binary_pair(
    df: pd.DataFrame,
    col_a: str,
    col_b: str,
) -> None:
    print(f"\n=== {col_a.upper()} × {col_b.upper()} ===")

    counts = contingency_table(df, col_a, col_b)
    percents = row_percentages(counts)

    print("\nCounts:")
    print(counts)

    print("\nRow percentages (%):")
    print(percents.round(1))

    plot_heatmap(
        percents,
        title=f"{col_a} × {col_b} (row %)",
        save_path=FIGURES_DIR /
                  f"{col_a}_vs_{col_b}_heatmap.png",
    )


# -------------------------
# Main
# -------------------------

def main() -> None:
    df: pd.DataFrame = load_clean_star_wars()

    binary_pairs: list[tuple[str, str]] = [
        ("seen_star_wars", "fan_star_wars"),
        ("fan_star_wars", "fan_star_trek"),
        ("seen_star_wars", "fan_star_trek"),
    ]

    for col_a, col_b in binary_pairs:
        analyze_binary_pair(df, col_a, col_b)


if __name__ == "__main__":
    main()
