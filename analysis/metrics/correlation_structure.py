# analysis/metrics/correlation_structure.py

from __future__ import annotations

import pandas as pd


def compute_character_correlation(
    matrix: pd.DataFrame,
) -> pd.DataFrame:
    """
    Pearson correlation between characters.
    """

    corr = matrix.corr(method="pearson")

    return corr