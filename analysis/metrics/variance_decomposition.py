# analysis/metrics/variance_decomposition.py

from __future__ import annotations
import pandas as pd


def build_variance_decomposition_table(
    anova_df: pd.DataFrame,
    *,
    entity_col: str,
) -> pd.DataFrame:
    """
    Build variance decomposition from ANOVA η² results.

    η² already represents proportion of total variance explained.
    """

    if entity_col not in anova_df.columns:
        raise ValueError(
            f"{entity_col=} not found. Available columns: "
            f"{anova_df.columns.tolist()}"
        )

    table = (
        anova_df
        .pivot(
            index=entity_col,
            columns="axis",
            values="eta_sq",
        )
        .fillna(0.0)
    )

    rename_map = {
        "age_group": "pct_age",
        "gender": "pct_gender",
        "census_region": "pct_region",
    }

    table = table.rename(columns=rename_map)

    # ensure columns exist
    for col in rename_map.values():
        if col not in table.columns:
            table[col] = 0.0

    table["pct_within"] = (
        1.0
        - table["pct_age"]
        - table["pct_gender"]
        - table["pct_region"]
    ).clip(lower=0.0)

    return (
        table
        .reset_index()
        .sort_values("pct_age", ascending=False)
    )