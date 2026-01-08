from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from src.io_utils import load_clean_star_wars


BOOLEAN_COLUMNS: list[str] = [
    "seen_star_wars",
    "fan_star_wars",
    "seen_ep1_phantom_menace",
    "seen_ep2_attack_clones",
    "seen_ep3_revenge_sith",
    "seen_ep4_new_hope",
    "seen_ep5_empire_strikes_back",
    "seen_ep6_return_jedi",
    "familiar_expanded_universe",
    "fan_expanded_universe",
    "fan_star_trek",
]


def summarize_boolean_column(df: pd.DataFrame, column: str) -> pd.Series:
    """
    Return counts and proportions for a boolean column (True / False / NA).
    """
    total: int = len(df)
    counts = df[column].value_counts(dropna=False)

    true_count = counts.get(True, 0)
    false_count = counts.get(False, 0)
    na_count = counts.get(pd.NA, 0)

    return pd.Series(
        {
            "true": true_count,
            "false": false_count,
            "na": na_count,
            "true_pct": true_count / total,
            "false_pct": false_count / total,
            "na_pct": na_count / total,
        }
    )


def summarize_boolean_columns(
    df: pd.DataFrame, columns: list[str]
) -> pd.DataFrame:
    """
    Summarize multiple boolean columns.
    """
    summary = {
        col: summarize_boolean_column(df, col)
        for col in columns
    }
    return pd.DataFrame(summary).T


def plot_boolean_distribution(
    df: pd.DataFrame,
    column: str,
    *,
    title: str | None = None,
    save_path: Path | None = None,
) -> None:
    """
    Plot True / False / NA distribution for a boolean column.
    """
    summary = summarize_boolean_column(df, column)

    counts = summary[["true", "false", "na"]]
    labels = ["True", "False", "NA"]

    plt.figure(figsize=(6, 4))
    ax = counts.plot(kind="bar")

    ax.set_ylabel("Number of respondents")
    ax.set_xlabel(column.replace("_", " ").title())
    ax.set_title(title or f"Distribution of {column}")

    plt.xticks(range(len(labels)), labels, rotation=0)

    for i, value in enumerate(counts):
        ax.text(i, value, str(int(value)), ha="center", va="bottom")

    plt.tight_layout()

    if save_path is not None:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path)

    plt.show()


def run_boolean_eda() -> None:
    df: pd.DataFrame = load_clean_star_wars()

    summary: pd.DataFrame = summarize_boolean_columns(df, BOOLEAN_COLUMNS)
    print(summary)

    for column in BOOLEAN_COLUMNS:
        plot_boolean_distribution(
            df,
            column,
            save_path=Path("analysis/figures") / f"{column}.png",
        )


def main() -> None:
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)

    run_boolean_eda()


if __name__ == "__main__":
    main()
