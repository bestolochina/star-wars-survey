# analysis/metrics/bootstrap_effects.py

from __future__ import annotations

import numpy as np
import pandas as pd

from analysis.metrics.anova_effects import compute_character_anova_table


def bootstrap_eta_squared(
    df: pd.DataFrame,
    *,
    characters: list[str],
    n_boot: int = 1000,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Bootstrap eta-squared estimates for selected characters.
    """

    rng = np.random.default_rng(random_state)
    results: list[pd.DataFrame] = []

    n = len(df)

    for i in range(n_boot):

        sample_idx = rng.integers(0, n, n)
        sample_df = df.iloc[sample_idx].copy()

        anova_df = compute_character_anova_table(sample_df)

        subset = anova_df[
            anova_df["character"].isin(characters)
            & anova_df["factor"].isin(["age_group", "gender"])
        ].copy()

        subset["bootstrap_iter"] = i
        results.append(subset)

    return pd.concat(results, ignore_index=True)

def summarize_bootstrap(boot_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute bootstrap mean and confidence intervals.
    """

    summary = (
        boot_df
        .groupby(["character", "factor"])["eta_sq"]
        .agg(
            mean="mean",
            lower=lambda x: x.quantile(0.025),
            upper=lambda x: x.quantile(0.975),
        )
        .reset_index()
    )

    return summary