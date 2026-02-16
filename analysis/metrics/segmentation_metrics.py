import pandas as pd
from analysis.transforms.reshaping import melt_variable
from src.config import EPISODE_RANK_COLUMNS, MIN_GROUP_SIZE

from typing import Any

def compute_segmentation_metrics(
    long_df: pd.DataFrame,
    *,
    demographic_column: str,
    episode_column: str,
    rank_column: str,
    exclude_groups: list[str] | None = None,
) -> dict[str, Any]:

    df = long_df.copy()

    # Exclude specified groups if provided
    if exclude_groups is not None:
        df = df.loc[~df[demographic_column].isin(exclude_groups)]

    group_sizes = (
        df.groupby(demographic_column, observed=True)
        .size()
    )

    valid_groups = group_sizes[group_sizes >= MIN_GROUP_SIZE].index
    df = df[df[demographic_column].isin(valid_groups)]

    # Compute mean rank per group × episode
    mean_rank = (
        df.groupby([episode_column, demographic_column], observed=True)[rank_column]
        .mean()
        .unstack(demographic_column)
        .sort_index()
    )

    # Range across groups per episode
    range_per_episode = mean_rank.max(axis=1) - mean_rank.min(axis=1)

    # Standard deviation across groups per episode
    sd_per_episode = mean_rank.std(axis=1)

    # Aggregate metrics
    avg_range = range_per_episode.mean()
    avg_sd = sd_per_episode.mean()
    max_range = range_per_episode.max()

    summary = {
        "avg_range": avg_range,
        "avg_sd": avg_sd,
        "max_range": max_range,
    }

    return {
        "mean_rank_matrix": mean_rank,
        "range_per_episode": range_per_episode,
        "sd_per_episode": sd_per_episode,
        "summary": summary,
    }

def build_comparison_table(df: pd.DataFrame) -> pd.DataFrame:
    long_df = melt_variable(
        df,
        variable_columns=EPISODE_RANK_COLUMNS,
        variable_name="episode ranking",
        value_name="rank",
    )

    age_group_metrics = compute_segmentation_metrics(
        long_df,
        demographic_column="age_group",
        episode_column="episode ranking",
        rank_column="rank",
    )

    gender_metrics = compute_segmentation_metrics(
        long_df,
        demographic_column="gender",
        episode_column="episode ranking",
        rank_column="rank",
    )

    household_income_metrics = compute_segmentation_metrics(
        long_df,
        demographic_column="household_income",
        episode_column="episode ranking",
        rank_column="rank",
    )

    education_level_metrics = compute_segmentation_metrics(
        long_df,
        demographic_column="education_level",
        episode_column="episode ranking",
        rank_column="rank",
        exclude_groups=["Less than HS"],
    )

    census_region_metrics = compute_segmentation_metrics(
        long_df,
        demographic_column="census_region",
        episode_column="episode ranking",
        rank_column="rank",
    )

    comparison = pd.DataFrame.from_dict(
        {
            "Gender": gender_metrics["summary"],
            "Age": age_group_metrics["summary"],
            "Income": household_income_metrics["summary"],
            "Education": education_level_metrics["summary"],
            "Region": census_region_metrics["summary"],
        },
        orient="index",
    )

    comparison = comparison.sort_values("avg_range", ascending=False)

    return comparison
