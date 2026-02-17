# analysis/metrics/segmentation_metrics.py

import pandas as pd
from typing import Any, Dict
from src.config import MIN_GROUP_SIZE


# ==========================================================
# CORE SEGMENTATION METRIC (PURE COMPUTATION)
# ==========================================================

def compute_segmentation_metrics(
    long_df: pd.DataFrame,
    *,
    demographic_column: str,
    episode_column: str,
    rank_column: str,
    exclude_groups: list[str] | None = None,
) -> dict[str, Any]:

    df = long_df.copy()

    if exclude_groups is not None:
        df = df.loc[~df[demographic_column].isin(exclude_groups)]

    group_sizes = (
        df.groupby(demographic_column, observed=True)
        .size()
    )

    valid_groups = group_sizes[group_sizes >= MIN_GROUP_SIZE].index
    df = df[df[demographic_column].isin(valid_groups)]

    # Mean rank per episode × demographic group
    mean_rank = (
        df.groupby([episode_column, demographic_column], observed=True)[rank_column]
        .mean()
        .unstack(demographic_column)
        .sort_index()
    )

    # Divergence metrics
    range_per_episode = mean_rank.max(axis=1) - mean_rank.min(axis=1)
    sd_per_episode = mean_rank.std(axis=1)

    summary = {
        "avg_range": range_per_episode.mean(),
        "avg_sd": sd_per_episode.mean(),
        "max_range": range_per_episode.max(),
    }

    return {
        "mean_rank_matrix": mean_rank,
        "range_per_episode": range_per_episode,
        "sd_per_episode": sd_per_episode,
        "summary": summary,
    }


# ==========================================================
# COMPUTE ALL DEMOGRAPHIC SEGMENTATION METRICS ONCE
# ==========================================================

def compute_all_segmentation_metrics(
    episode_long: pd.DataFrame,
) -> Dict[str, dict[str, Any]]:

    demographics = {
        "gender": "gender",
        "age_group": "age_group",
        "household_income": "household_income",
        "education_level": "education_level",
        "census_region": "census_region",
    }

    results = {}

    for key, column in demographics.items():

        exclude = ["Less than HS"] if column == "education_level" else None

        metrics = compute_segmentation_metrics(
            episode_long,
            demographic_column=column,
            episode_column="episode",
            rank_column="rank",
            exclude_groups=exclude,
        )

        results[key] = metrics

    return results


# ==========================================================
# BUILD COMPARISON TABLE FROM STORED METRICS
# ==========================================================

def build_comparison_table_from_metrics(
    metrics_store: Dict[str, dict[str, Any]],
) -> pd.DataFrame:

    readable_labels = {
        "gender": "Gender",
        "age_group": "Age Group",
        "household_income": "Household Income",
        "education_level": "Education Level",
        "census_region": "Census Region",
    }

    comparison = pd.DataFrame.from_dict(
        {
            readable_labels[key]: metrics_store[key]["summary"]
            for key in metrics_store
        },
        orient="index",
    )

    return comparison.sort_values("avg_range", ascending=False)


# ==========================================================
# EPISODE-LEVEL DIVERGENCE TABLES
# ==========================================================

def build_episode_divergence_table(
    metrics: dict[str, Any],
) -> pd.DataFrame:

    episode_table = pd.DataFrame({
        "range": metrics["range_per_episode"],
        "sd": metrics["sd_per_episode"],
    })

    return episode_table.sort_values("range", ascending=False)


def build_all_episode_divergence_tables_from_metrics(
    metrics_store: Dict[str, dict[str, Any]],
) -> dict[str, pd.DataFrame]:

    return {
        key: build_episode_divergence_table(metrics)
        for key, metrics in metrics_store.items()
    }


# ==========================================================
# EPISODE DRIVER EXTRACTION
# ==========================================================

def extract_episode_drivers(
    metrics: dict[str, Any],
    *,
    top_n: int = 2,
) -> pd.DataFrame:

    mean_rank = metrics["mean_rank_matrix"]
    range_per_episode = metrics["range_per_episode"]

    top_episodes = (
        range_per_episode
        .sort_values(ascending=False)
        .head(top_n)
        .index
    )

    results = []

    for episode in top_episodes:

        row = mean_rank.loc[episode]

        best_group = row.idxmin()
        worst_group = row.idxmax()

        best_value = row.min()
        worst_value = row.max()

        results.append({
            "episode": episode,
            "best_group": best_group,
            "best_mean_rank": best_value,
            "worst_group": worst_group,
            "worst_mean_rank": worst_value,
            "rank_gap": worst_value - best_value,
        })

    return pd.DataFrame(results)


def extract_all_episode_drivers(
    metrics_store: Dict[str, dict[str, Any]],
    *,
    top_n: int = 2,
) -> dict[str, pd.DataFrame]:

    return {
        key: extract_episode_drivers(metrics, top_n=top_n)
        for key, metrics in metrics_store.items()
    }
