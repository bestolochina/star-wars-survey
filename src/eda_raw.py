import pandas as pd

from src.io_utils import load_raw_star_wars


def summarize_column(df: pd.DataFrame, col: str) -> None:
    print(f"\n=== {col} ===")
    print("dtype:", df[col].dtype)
    print("NaNs:", df[col].isna().sum())
    print("Unique values:")
    print(df[col].value_counts(dropna=False))


def summarize_columns(df: pd.DataFrame, columns: list[str]) -> None:
    for col in columns:
        summarize_column(df, col)


def check_boolean_candidates(df: pd.DataFrame) -> None:
    for col in df.columns:
        values = set(df[col].dropna().unique())
        if values.issubset({"Yes", "No"}):
            print(col, "→ boolean candidate")


def check_rank_ranges(df: pd.DataFrame, columns: list[str]) -> None:
    for col in columns:
        series = df[col].dropna()
        if not series.empty:
            print(
                col,
                "min:", series.min(),
                "max:", series.max(),
                "unique:", sorted(series.unique())
            )


def missingness_report(df: pd.DataFrame, threshold: float = 0.2) -> None:
    missing_ratio = df.isna().mean()
    bad = missing_ratio[missing_ratio > threshold]

    print("Columns with high missingness:")
    print(bad.sort_values(ascending=False))


if __name__ == "__main__":

    df = load_raw_star_wars()

    summarize_column(df, "who_shot_first")
    summarize_column(df, "gender")
    summarize_columns(df, ["age_group", "education_level"])

    check_boolean_candidates(df)

