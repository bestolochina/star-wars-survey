# analysis/metrics/segmentation_metrics.py

from __future__ import annotations

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
    variable_column: str,
    value_column: str,
    exclude_groups: list[str] | None = None,
) -> dict[str, Any]:

    df = long_df.copy()

    # Optional exclusion (e.g. small or special categories)
    if exclude_groups is not None:
        df = df.loc[~df[demographic_column].isin(exclude_groups)]

    # Enforce minimum group size
    group_sizes = (
        df.groupby(demographic_column, observed=True)
        .size()
    )

    valid_groups = group_sizes[group_sizes >= MIN_GROUP_SIZE].index
    df = df[df[demographic_column].isin(valid_groups)]

    # Mean value per variable × demographic group
    mean_matrix = (
        df.groupby([variable_column, demographic_column], observed=True)[value_column]
        .mean()
        .unstack(demographic_column)
        .sort_index()
    )

    # Divergence metrics
    range_per_variable = mean_matrix.max(axis=1) - mean_matrix.min(axis=1)
    sd_per_variable = mean_matrix.std(axis=1)

    summary = {
        "avg_range": range_per_variable.mean(),
        "avg_sd": sd_per_variable.mean(),
        "max_range": range_per_variable.max(),
    }

    return {
        "mean_matrix": mean_matrix,
        "range_per_variable": range_per_variable,
        "sd_per_variable": sd_per_variable,
        "summary": summary,
    }


# ==========================================================
# COMPUTE ALL DEMOGRAPHIC SEGMENTATION METRICS
# ==========================================================

def compute_all_segmentation_metrics(
    long_df: pd.DataFrame,
    *,
    variable_column: str,
    value_column: str,
) -> Dict[str, dict[str, Any]]:

    demographics = {
        "gender": "gender",
        "age_group": "age_group",
        "household_income": "household_income",
        "education_level": "education_level",
        "census_region": "census_region",
    }

    results: Dict[str, dict[str, Any]] = {}

    for key, column in demographics.items():

        exclude = ["Less than HS"] if column == "education_level" else None

        metrics = compute_segmentation_metrics(
            long_df,
            demographic_column=column,
            variable_column=variable_column,
            value_column=value_column,
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
# VARIABLE-LEVEL DIVERGENCE TABLES
# ==========================================================

def build_variable_divergence_table(
    metrics: dict[str, Any],
) -> pd.DataFrame:

    variable_table = pd.DataFrame({
        "range": metrics["range_per_variable"],
        "sd": metrics["sd_per_variable"],
    })

    return variable_table.sort_values("range", ascending=False)


def build_all_variable_divergence_tables_from_metrics(
    metrics_store: Dict[str, dict[str, Any]],
) -> dict[str, pd.DataFrame]:

    return {
        key: build_variable_divergence_table(metrics)
        for key, metrics in metrics_store.items()
    }


# ==========================================================
# DRIVER EXTRACTION
# ==========================================================

def extract_variable_drivers(
    metrics: dict[str, Any],
    *,
    top_n: int = 2,
) -> pd.DataFrame:

    mean_matrix = metrics["mean_matrix"]
    range_per_variable = metrics["range_per_variable"]

    top_variables = (
        range_per_variable
        .sort_values(ascending=False)
        .head(top_n)
        .index
    )

    results = []

    for variable in top_variables:

        row = mean_matrix.loc[variable]

        best_group = row.idxmin()
        worst_group = row.idxmax()

        best_value = row.min()
        worst_value = row.max()

        results.append({
            "variable": variable,
            "best_group": best_group,
            "best_mean_value": best_value,
            "worst_group": worst_group,
            "worst_mean_value": worst_value,
            "value_gap": worst_value - best_value,
        })

    return pd.DataFrame(results)


def extract_all_variable_drivers(
    metrics_store: Dict[str, dict[str, Any]],
    *,
    top_n: int = 2,
) -> dict[str, pd.DataFrame]:

    return {
        key: extract_variable_drivers(metrics, top_n=top_n)
        for key, metrics in metrics_store.items()
    }
