"""
Phase 1.3 — Nominal EDA

Assumptions:
- Missing values may be structural (survey logic)
- Percentages are unconditional unless stated otherwise
- Ordered categoricals are treated as ordinal, not nominal
"""


from pathlib import Path
from src.io_utils import load_clean_star_wars
import matplotlib.pyplot as plt
import pandas as pd
from pandas.api.types import CategoricalDtype


# For every nominal column, we will answer:
# What are the unique values?
# Are there:
# typos?
# inconsistent casing?
# semantic duplicates?
# What is the distribution (counts + %)?
# How much missing data (NA)?
# Is missingness:
# random?
# structural (survey design)?
# Is the column analytically useful?

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

    plt.show()

def analyze_nominal_column(
    df: pd.DataFrame,
    column: str,
    title: str,
) -> None:
    print(f"\n=== {column.upper()} ===")
    summary = summarize_nominal_column(df, column)
    print(summary)

    plot_nominal_distribution(
        df,
        column,
        title=title,
        save_path=Path("analysis/figures") / f"{column}.png",
    )

def run_nominal_eda() -> None:
    df: pd.DataFrame = load_clean_star_wars()

    nominal_columns: dict[str, str] = {
        "gender": "Gender distribution",
        "education_level": "Education level distribution",
        "household_income": "Household income distribution",
        "census_region": "Census region distribution",
        "who_shot_first": "Who shot first?",
    }

    for column, title in nominal_columns.items():
        analyze_nominal_column(df, column, title)

def main() -> None:
    run_nominal_eda()


if __name__ == "__main__":
    main()
