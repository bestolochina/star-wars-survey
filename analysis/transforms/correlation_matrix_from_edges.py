# analysis/transforms/correlation_matrix_from_edges.py

import numpy as np
import pandas as pd


# ==========================================================
# Convert Edge List → Correlation Matrix
# ==========================================================

def build_correlation_matrix_from_edges(
    edge_df: pd.DataFrame,
) -> pd.DataFrame:

    characters = sorted(
        set(edge_df["source"]).union(edge_df["target"])
    )

    matrix = pd.DataFrame(
        0.0,
        index=characters,
        columns=characters,
    )

    for _, row in edge_df.iterrows():

        i = row["source"]
        j = row["target"]
        w = row["correlation"]

        matrix.loc[i, j] = w
        matrix.loc[j, i] = w

    # diagonal = 1 (self-correlation)
    matrix = matrix.copy()
    values = matrix.to_numpy(copy=True)
    np.fill_diagonal(values, 1.0)
    matrix.loc[:, :] = values

    return matrix