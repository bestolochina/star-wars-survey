# analysis/transforms/matrix_builder.py

from __future__ import annotations

import pandas as pd


def build_character_matrix(
    df: pd.DataFrame,
    *,
    respondent_id: str,
    character_columns: dict[str, str],
    standardize: bool = False,
) -> pd.DataFrame:
    """
    Build respondent × character matrix.

    character_columns:
        {raw_column_name: display_name}
    """

    raw_cols = list(character_columns.keys())

    matrix = (
        df[[respondent_id] + raw_cols]
        .set_index(respondent_id)
        .rename(columns=character_columns)  # ⭐ KEY STEP
        .copy()
    )

    if standardize:
        matrix = (matrix - matrix.mean()) / matrix.std(ddof=0)

    return matrix