import pandas as pd

def melt_variable(
    df: pd.DataFrame,
    *,
    variable_columns: dict[str, str],
    variable_name: str,
    value_name: str,
) -> pd.DataFrame:
    """
    Converts wide-format ranking columns into long format
    while preserving all demographic and respondent-level columns.
    """

    # Select all columns that are NOT part of the variable being melted
    id_vars = [col for col in df.columns if col not in variable_columns]

    # Convert wide columns (e.g., rank_ep1, rank_ep2, ...) into long format
    long_df = df.melt(
        id_vars=id_vars,                     # columns to keep as identifiers
        value_vars=variable_columns.keys(),  # columns to unpivot
        var_name=variable_name,              # name of new variable column
        value_name=value_name,               # name of new value column
    )

    # Map internal column names to human-readable labels
    long_df[variable_name] = long_df[variable_name].map(variable_columns)

    if long_df[variable_name].isna().any():
        raise ValueError("Unmapped variable column detected.")

    # Drop rows where the user did not provide a rating
    long_df = long_df.dropna(subset=[value_name])

    # Return the cleaned long-format dataframe
    return long_df
