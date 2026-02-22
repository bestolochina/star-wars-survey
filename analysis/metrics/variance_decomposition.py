# analysis/metrics/variance_decomposition.py

from __future__ import annotations

import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf


# ---------------------------------------------------------
# Core SS extractor
# ---------------------------------------------------------

def _anova_ss(
    df: pd.DataFrame,
    *,
    response: str,
    factor: str,
) -> tuple[float, float]:
    """
    Return (SS_between, SS_total) from one-way ANOVA.
    """

    model = smf.ols(
        f'Q("{response}") ~ C({factor})',
        data=df,
    ).fit()

    anova = sm.stats.anova_lm(model, typ=2)

    ss_between = float(anova.loc[f"C({factor})", "sum_sq"])
    ss_residual = float(anova.loc["Residual", "sum_sq"])

    ss_total = ss_between + ss_residual

    return ss_between, ss_total


# ---------------------------------------------------------
# Character-level variance decomposition
# ---------------------------------------------------------

def compute_variance_decomposition(
    long_df: pd.DataFrame,
    *,
    character_col: str,
    rating_col: str,
    age_col: str = "age_group",
    gender_col: str = "gender",
    region_col: str = "census_region",
) -> pd.DataFrame:
    """
    Compute variance explained by demographic axes
    for each character.
    """

    results: list[dict[str, float | str]] = []

    characters = sorted(long_df[character_col].unique())

    for character in characters:

        df_char = long_df[
            long_df[character_col] == character
        ].dropna(
            subset=[rating_col, age_col, gender_col, region_col]
        )

        if len(df_char) < 10:
            continue

        ss_age, ss_total = _anova_ss(
            df_char,
            response=rating_col,
            factor=age_col,
        )

        ss_gender, _ = _anova_ss(
            df_char,
            response=rating_col,
            factor=gender_col,
        )

        ss_region, _ = _anova_ss(
            df_char,
            response=rating_col,
            factor=region_col,
        )

        pct_age = ss_age / ss_total
        pct_gender = ss_gender / ss_total
        pct_region = ss_region / ss_total

        # conservative unexplained estimate
        pct_within = 1.0 - max(
            pct_age,
            pct_gender,
            pct_region,
        )

        results.append(
            {
                "character": character,
                "pct_age": pct_age,
                "pct_gender": pct_gender,
                "pct_region": pct_region,
                "pct_within": pct_within,
            }
        )

    return pd.DataFrame(results).sort_values(
        "pct_age",
        ascending=False,
    )