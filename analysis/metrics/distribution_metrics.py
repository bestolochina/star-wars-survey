# analysis/metrics/distribution_metrics.py

import pandas as pd
from typing import Dict, List

from src.paths import PHASE1_TABLES_DIR


# ==========================================================
# LOW-LEVEL METRIC ENGINE
# ==========================================================

def compute_rank_percentage_distribution(
    df: pd.DataFrame,
    *,
    demographic_column: str,
    episode_column: str,
    rank_column: str,
) -> pd.DataFrame:
    """
    Compute tidy percentage distribution of ranks within each
    demographic × episode combination.

    Returns long-format dataframe:
    [demographic, episode, rank, count, percentage]
    """

    grouped = (
        df.groupby([demographic_column, episode_column, rank_column], observed=True)
        .size()
        .reset_index(name="count")
    )

    grouped["percentage"] = (
        grouped.groupby([demographic_column, episode_column], observed=True)["count"]
        .transform(lambda x: x / x.sum())
    )

    return grouped


# ==========================================================
# HIGH-LEVEL REPORT TABLE BUILDER
# ==========================================================

## old function
# def sanity_check_rank_percentages_multi(
#     long_df: pd.DataFrame,
#     *,
#     variable_name: str,
#     value_name: str,
#     slice_column: str,
#     slice_config: dict[str, dict[str, str]],
# ) -> pd.DataFrame:
#
#     if slice_column not in slice_config:
#         raise ValueError(
#             f"Unknown slice column '{slice_column}'. "
#             f"Available options: {list(slice_config.keys())}"
#         )
#
#     if slice_column not in long_df.columns:
#         raise ValueError(
#             f"Column '{slice_column}' not found in dataframe."
#         )
#
#     slice_map = slice_config[slice_column]
#     slices = list(slice_map.keys())
#
#     tables: dict[str, pd.DataFrame] = {}
#
#     for raw_value in slices:
#
#         slice_df = long_df.loc[long_df[slice_column] == raw_value]
#
#         if slice_df.empty:
#             continue
#
#         # N per variable
#         n_counts = slice_df.groupby(variable_name)[value_name].count()
#
#         freq = (
#             pd.crosstab(
#                 slice_df[variable_name],
#                 slice_df[value_name],
#                 normalize="index",
#             )
#             * 100
#         ).round(1)
#
#         # Add N column
#         freq["n"] = n_counts
#
#         tables[slice_map[raw_value]] = freq
#
#     combined = pd.concat(tables, names=[slice_column, variable_name])
#
#     return combined

def build_rank_distribution_table(
    df: pd.DataFrame,
    *,
    demographic_column: str,
    episode_column: str,
    rank_column: str,
    slice_config: Dict[str, Dict[str, str]],
    as_percentage: bool = True,
    round_digits: int = 1,
) -> pd.DataFrame:
    """
    Build formatted distribution table (report-ready).

    Returns multi-index table:
        index: (demographic_display_name, episode)
        columns: rank values + 'n'
    """

    if demographic_column not in slice_config:
        raise ValueError(
            f"Unknown demographic column '{demographic_column}'. "
            f"Available: {list(slice_config.keys())}"
        )

    if demographic_column not in df.columns:
        raise ValueError(
            f"Column '{demographic_column}' not found in dataframe."
        )

    slice_map = slice_config[demographic_column]
    ordered_slices = list(slice_map.keys())

    tables: Dict[str, pd.DataFrame] = {}

    for raw_value in ordered_slices:

        slice_df = df.loc[df[demographic_column] == raw_value]

        if slice_df.empty:
            continue

        # N per episode
        n_counts = (
            slice_df.groupby(episode_column, observed=True)[rank_column]
            .count()
        )

        freq = pd.crosstab(
            slice_df[episode_column],
            slice_df[rank_column],
            normalize="index",
        )

        if as_percentage:
            freq = (freq * 100).round(round_digits)

        # Add sample size column
        freq["n"] = n_counts

        tables[slice_map[raw_value]] = freq

    if not tables:
        raise ValueError("No valid slices found for table construction.")

    combined = pd.concat(
        tables,
        names=[demographic_column, episode_column],
    )

    return combined

def build_all_rank_distribution_tables(
    df: pd.DataFrame,
    *,
    episode_column: str,
    rank_column: str,
    slice_config: dict[str, dict[str, str]],
) -> dict[str, pd.DataFrame]:

    tables = {}

    for demographic_column in slice_config.keys():
        tables[demographic_column] = build_rank_distribution_table(
            df,
            demographic_column=demographic_column,
            episode_column=episode_column,
            rank_column=rank_column,
            slice_config=slice_config,
        )

    return tables


# ==========================================================
# VALIDATION UTILITY
# ==========================================================

def validate_rank_percentage_sums(
    df: pd.DataFrame,
    *,
    demographic_columns: List[str],
    episode_column: str,
    rank_column: str,
    tolerance: float = 1e-6,
) -> pd.DataFrame:
    """
    Validate that percentages sum to 1 for each
    demographic × episode combination.

    Returns dataframe of sums for inspection.
    """

    results = []

    for demo in demographic_columns:

        dist = compute_rank_percentage_distribution(
            df,
            demographic_column=demo,
            episode_column=episode_column,
            rank_column=rank_column,
        )

        check = (
            dist.groupby([demo, episode_column], observed=True)["percentage"]
            .sum()
            .reset_index(name="sum_percentage")
        )

        check["valid"] = (
            (check["sum_percentage"] - 1.0).abs() < tolerance
        )

        check["demographic"] = demo

        results.append(check)

    return pd.concat(results, ignore_index=True)
