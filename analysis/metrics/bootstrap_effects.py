# analysis/metrics/bootstrap_effects.py

"""
Bootstrap robustness checks for ANOVA effect sizes.

Phase 2 — Step 2.4.5 Robustness Validation

Purpose
-------
Estimate stability of η² effect sizes via bootstrap resampling.

Outputs:
    • bootstrap mean η²
    • confidence intervals
    • ordering stability across demographic axes

Designed to work for:
    - character ratings
    - episode rankings
"""

from __future__ import annotations

from typing import Iterable
import numpy as np
import pandas as pd
from pathlib import Path


# ---------------------------------------------------------------------
# Core η² computation
# ---------------------------------------------------------------------

def _eta_squared(
    df: pd.DataFrame,
    *,
    value_col: str,
    axis_col: str,
) -> float:
    """
    Compute η² = SS_between / SS_total for one axis.
    """

    grand_mean = df[value_col].mean()

    # Between-group SS
    ss_between = (
        df.groupby(axis_col, observed=True)[value_col]
        .apply(lambda g: len(g) * (g.mean() - grand_mean) ** 2)
        .sum()
    )

    # Total SS
    ss_total = ((df[value_col] - grand_mean) ** 2).sum()

    if ss_total == 0:
        return 0.0

    return float(ss_between / ss_total)


# ---------------------------------------------------------------------
# Bootstrap engine
# ---------------------------------------------------------------------

def bootstrap_eta_squared(
    df: pd.DataFrame,
    *,
    entity_col: str,
    value_col: str,
    axes: Iterable[str],
    entities: Iterable[str],
    n_boot: int = 1000,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Bootstrap η² estimates.

    Parameters
    ----------
    df :
        Long-format dataframe (character_long or episode_long)

    entity_col :
        Column identifying entity (character / episode)

    value_col :
        Rating or ranking column

    axes :
        Demographic columns (age_group, gender, etc.)

    entities :
        Subset to bootstrap (top 3 characters)

    Returns
    -------
    DataFrame with bootstrap summaries.
    """

    rng = np.random.default_rng(random_state)

    results: list[dict] = []

    for entity in entities:

        sub = df[df[entity_col] == entity]

        n = len(sub)
        if n == 0:
            continue

        for axis in axes:

            estimates: list[float] = []

            for _ in range(n_boot):

                sample_idx = rng.integers(0, n, n)
                sample = sub.iloc[sample_idx]

                eta = _eta_squared(
                    sample,
                    value_col=value_col,
                    axis_col=axis,
                )

                estimates.append(eta)

            estimates_arr = np.array(estimates)

            results.append(
                {
                    "entity": entity,
                    "axis": axis,
                    "eta_mean": estimates_arr.mean(),
                    "eta_std": estimates_arr.std(ddof=1),
                    "ci_low": np.percentile(estimates_arr, 2.5),
                    "ci_high": np.percentile(estimates_arr, 97.5),
                }
            )

    return pd.DataFrame(results)


# ---------------------------------------------------------------------
# Convenience wrapper (Phase 2 pipeline)
# ---------------------------------------------------------------------

def run_bootstrap_validation(
    *,
    df: pd.DataFrame,
    entity_col: str,
    value_col: str,
    axes: list[str],
    top_entities: list[str],
    save_path: Path,
) -> pd.DataFrame:
    """
    Execute robustness validation and save results.
    """

    bootstrap_df = bootstrap_eta_squared(
        df,
        entity_col=entity_col,
        value_col=value_col,
        axes=axes,
        entities=top_entities,
    )

    save_path.parent.mkdir(parents=True, exist_ok=True)
    bootstrap_df.to_csv(save_path, index=False)

    print("\n=== BOOTSTRAP ROBUSTNESS RESULTS ===")
    print(bootstrap_df)

    return bootstrap_df