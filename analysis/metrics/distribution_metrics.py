# analysis/metrics/distribution_metrics.py

import pandas as pd
from typing import List

# =========================
# DATA TRANSFORMATION
# =========================

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




def compute_rank_percentage_distribution(
    df: pd.DataFrame,
    *,
    demographic_column: str,
    episode_column: str,
    rank_column: str,
) -> pd.DataFrame:
    """
    Computes percentage distribution of ranks within each demographic group.
    """

    grouped = (
        df.groupby([demographic_column, episode_column, rank_column])
        .size()
        .reset_index(name="count")
    )

    grouped["percentage"] = (
        grouped.groupby([demographic_column, episode_column])["count"]
        .transform(lambda x: x / x.sum())
    )

    return grouped


def sanity_check_rank_percentages_multi(
    df: pd.DataFrame,
    *,
    demographic_columns: List[str],
    episode_column: str,
    rank_column: str,
) -> None:
    """
    Validates that rank percentages sum to 1 per demographic + episode.
    Prints diagnostic output.
    """

    for demo in demographic_columns:
        dist = compute_rank_percentage_distribution(
            df,
            demographic_column=demo,
            episode_column=episode_column,
            rank_column=rank_column,
        )

        check = (
            dist.groupby([demo, episode_column])["percentage"]
            .sum()
            .round(6)
        )

        print(f"\nSanity Check — {demo}")
        print(check.value_counts())
