# analysis/metrics/segmentation_strength.py

from __future__ import annotations

import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
from statsmodels.stats.multitest import multipletests


# ==========================================================
# Contingency Tables
# ==========================================================

def build_contingency_table(
    df: pd.DataFrame,
    demographic: str,
    cluster_col: str,
) -> pd.DataFrame:

    table = pd.crosstab(
        df[cluster_col],
        df[demographic],
    )

    return table

# ==========================================================
# Chi-square Test
# ==========================================================

def compute_chisquare(
    table: pd.DataFrame,
) -> dict:

    chi2, p, dof, expected = chi2_contingency(table)

    return {
        "chi_square_statistic": chi2,
        "chi_square_p_value": p,
        "chi_square_degrees_of_freedom": dof,
        "sample_size": table.values.sum(),
    }


# ==========================================================
# Cramér's V
# ==========================================================

def compute_cramers_v(
    chi2: float,
    n: int,
    table: pd.DataFrame,
) -> float:

    r, k = table.shape

    return np.sqrt(chi2 / (n * (min(k - 1, r - 1))))


# ==========================================================
# Multiple Testing Correction
# ==========================================================

def adjust_pvalues(
    results: pd.DataFrame,
    method: str = "fdr_bh",
) -> pd.DataFrame:

    corrected = multipletests(
        results["chi_square_p_value"],
        method=method,
    )[1]

    results["fdr_adjusted_p_value"] = corrected

    return results


# ==========================================================
# Robustness Checks
# ==========================================================

def check_min_expected(
    table: pd.DataFrame,
) -> bool:

    _, _, _, expected = chi2_contingency(table)

    return (expected >= 5).all()


def compute_standardized_residuals(
    table: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compute standardized residuals for a contingency table.

    residual = (observed - expected) / sqrt(expected)
    """

    observed = table.values

    chi2, p, dof, expected = chi2_contingency(table)

    residuals = (observed - expected) / np.sqrt(expected)

    residual_df = pd.DataFrame(
        residuals,
        index=table.index,
        columns=table.columns,
    )

    return residual_df
