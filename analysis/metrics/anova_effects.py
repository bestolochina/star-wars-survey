# analysis/metrics/anova_effects.py

from __future__ import annotations

import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf


# ==========================================================
# CONFIG
# ==========================================================

AXES = [
    "age_group",
    "gender",
    "census_region",
]


# ==========================================================
# CORE ANOVA COMPUTATION
# ==========================================================

def compute_variable_anova_table(
    long_df: pd.DataFrame,
    *,
    variable_column: str,
    value_column: str,
) -> pd.DataFrame:
    """
    Runs one-way ANOVA for each variable across demographic axes.

    Model:
        value ~ C(axis)

    Returns
    -------
    DataFrame with columns:
        variable | axis | F | p_value | eta_sq | partial_r2
    """

    results: list[dict] = []

    variables = long_df[variable_column].dropna().unique()

    for variable in variables:

        df_var = long_df.loc[
            long_df[variable_column] == variable
        ].copy()

        for axis in AXES:

            df_axis = df_var.dropna(
                subset=[axis, value_column]
            )

            if df_axis.empty:
                continue

            model = smf.ols(
                f"{value_column} ~ C({axis})",
                data=df_axis,
            ).fit()

            anova = sm.stats.anova_lm(model, typ=2)

            ss_between = anova.loc[f"C({axis})", "sum_sq"]
            ss_total = anova["sum_sq"].sum()

            eta_sq = ss_between / ss_total

            results.append(
                {
                    "variable": variable,
                    "axis": axis,
                    "F": anova.loc[f"C({axis})", "F"],
                    "p_value": anova.loc[f"C({axis})", "PR(>F)"],
                    "eta_sq": eta_sq,
                    "partial_r2": eta_sq,
                }
            )

    return pd.DataFrame(results)


# ==========================================================
# ETA² TABLE
# ==========================================================

def build_eta_squared_table(
    anova_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Wide table:
        variable | eta_age | eta_gender | eta_region
    """

    pivot = (
        anova_df.pivot(
            index="variable",
            columns="axis",
            values="eta_sq",
        )
        .rename(
            columns={
                "age_group": "eta_age",
                "gender": "eta_gender",
                "census_region": "eta_region",
            }
        )
        .reset_index()
    )

    return pivot.sort_values("eta_age", ascending=False)


# ==========================================================
# AXIS SUMMARY
# ==========================================================

def build_axis_summary(
    anova_df: pd.DataFrame,
    *,
    alpha: float = 0.05,
) -> pd.DataFrame:
    """
    Summary statistics per demographic axis.
    """

    grouped = anova_df.groupby("axis", observed=True)

    summary = pd.DataFrame(
        {
            "mean_eta_sq": grouped["eta_sq"].mean(),
            "max_eta_sq": grouped["eta_sq"].max(),
            "pct_significant": grouped["p_value"]
            .apply(lambda s: (s < alpha).mean()),
        }
    )

    return summary.sort_values("mean_eta_sq", ascending=False)