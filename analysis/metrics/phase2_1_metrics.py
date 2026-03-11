# analysis/metrics/phase2_1_metrics.py

from __future__ import annotations

import pandas as pd
from pandas.api.types import CategoricalDtype
from src.config import EPISODE_RANK_COLUMNS, CHARACTER_RATING_COLUMNS


# ==========================================================
# GENERIC CATEGORICAL DISTRIBUTION
# ==========================================================

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


def categorical_distribution(
    df: pd.DataFrame,
    column: str,
    dropna: bool = False,
) -> pd.DataFrame:
    """
    Compute counts and percentages for a categorical variable.
    """

    counts = df[column].value_counts(dropna=dropna)

    percents = (
        df[column]
        .value_counts(normalize=True, dropna=dropna)
        * 100
    )

    table = pd.DataFrame({
        "count": counts,
        "percent": percents.round(2),
    })

    return table


# ==========================================================
# EPISODE RANKINGS
# ==========================================================

def compute_episode_average_scores(df: pd.DataFrame) -> pd.Series:

    ranks = df[list(EPISODE_RANK_COLUMNS.keys())]
    scores = 7 - ranks

    avg_scores = scores.mean()
    avg_scores.index = EPISODE_RANK_COLUMNS.values()

    return avg_scores


def episode_average_scores(
    df: pd.DataFrame,
    episode_columns: list[str],
) -> pd.DataFrame:
    """
    Compute mean ranking score for each episode.
    """

    means = df[episode_columns].mean()

    table = (
        means
        .sort_values()
        .rename("average_rank")
        .to_frame()
    )

    return table


def melt_episode_ranks(df: pd.DataFrame) -> pd.DataFrame:

    long_df = df.melt(
        value_vars=EPISODE_RANK_COLUMNS.keys(),
        var_name="episode",
        value_name="rank",
    )

    long_df["episode"] = long_df["episode"].map(EPISODE_RANK_COLUMNS)

    return long_df.dropna(subset=["rank"])

# ==========================================================
# CHARACTER RATINGS
# ==========================================================

def character_rating_distribution(
    df: pd.DataFrame,
    character_columns: list[str],
) -> pd.DataFrame:
    """
    Count rating frequencies across all characters.
    """

    long_df = df[character_columns].melt(
        var_name="character",
        value_name="rating",
    )

    table = (
        long_df["rating"]
        .value_counts(dropna=False)
        .sort_index()
        .to_frame(name="count")
    )

    table["percent"] = (
        table["count"] /
        table["count"].sum()
        * 100
    ).round(2)

    return table


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

