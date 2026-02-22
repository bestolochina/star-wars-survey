# analysis/metrics/anova_effects.py

from __future__ import annotations

import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from typing import Dict, List


# ==========================================================
# CORE ANOVA COMPUTATION
# ==========================================================

def compute_oneway_anova_effect(
    df: pd.DataFrame,
    *,
    response: str,
    axis: str,
) -> dict[str, float]:
    """
    Run one-way ANOVA and compute effect sizes.

    Returns
    -------
    dict with:
        F
        p_value
        eta_sq
        partial_r2
    """

    formula = f"{response} ~ C({axis})"

    model = smf.ols(formula, data=df).fit()
    anova = sm.stats.anova_lm(model, typ=2)

    ss_between = anova.loc[f"C({axis})", "sum_sq"]
    ss_resid = anova.loc["Residual", "sum_sq"]
    ss_total = ss_between + ss_resid

    eta_sq = ss_between / ss_total
    partial_r2 = ss_between / (ss_between + ss_resid)

    return {
        "F": anova.loc[f"C({axis})", "F"],
        "p_value": anova.loc[f"C({axis})", "PR(>F)"],
        "eta_sq": eta_sq,
        "partial_r2": partial_r2,
    }


# ==========================================================
# CHARACTER LOOP
# ==========================================================

def compute_character_anova_table(
    character_long: pd.DataFrame,
    *,
    response_column: str = "rating",
    character_column: str = "character",
    axes: List[str] | None = None,
) -> pd.DataFrame:
    """
    Run one-way ANOVA for each character across axes.
    """

    if axes is None:
        axes = ["age_group", "gender", "census_region"]

    results: List[dict] = []

    for character, df_char in character_long.groupby(character_column):

        for axis in axes:

            df_valid = df_char[[response_column, axis]].dropna()

            if df_valid[axis].nunique() < 2:
                continue

            stats = compute_oneway_anova_effect(
                df_valid,
                response=response_column,
                axis=axis,
            )

            results.append({
                "character": character,
                "axis": axis,
                **stats,
            })

    return pd.DataFrame(results)

# ==========================================================
# WIDE ETA-SQUARED TABLE
# ==========================================================

def build_eta_squared_table(
    anova_results: pd.DataFrame,
) -> pd.DataFrame:
    """
    character | eta_age | eta_gender | eta_region
    """

    table = (
        anova_results
        .pivot(index="character", columns="axis", values="eta_sq")
        .rename(columns={
            "age_group": "eta_age",
            "gender": "eta_gender",
            "census_region": "eta_region",
        })
        .sort_index()
    )

    return table

def build_axis_summary(
    anova_df: pd.DataFrame,
    *,
    alpha: float = 0.05,
) -> pd.DataFrame:
    """
    Summarise ANOVA effect sizes across demographic axes.
    """

    eta_mean = (
        anova_df
        .groupby("axis")["eta_sq"]
        .mean()
        .rename("mean_eta_sq")
    )

    significant_rate = (
        (anova_df["p_value"] < alpha)
        .groupby(anova_df["axis"])
        .mean()
        .rename("significant_rate")
    )

    summary = pd.concat([eta_mean, significant_rate], axis=1)

    return summary.reset_index().sort_values(
        "mean_eta_sq",
        ascending=False,
    )