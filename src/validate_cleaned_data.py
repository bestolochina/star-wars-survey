import pandas as pd

from src.io_utils import load_raw_star_wars
from cleaning import clean_all

def check_boolean_columns(df: pd.DataFrame, columns: list[str]) -> None:
    # Boolean columns must be boolean
    for col in columns:
        dtype = df[col].dtype.name
        print(f"{col}: {dtype}")
        assert dtype == "boolean", f"{col} is not boolean"

def check_rank_columns(df: pd.DataFrame, columns: list[str]) -> None:
    # Episode ranks must be 1–6 (or NA)
    for col in columns:
        values = set(df[col].dropna().unique())
        assert values.issubset({1, 2, 3, 4, 5, 6}), f"{col} out of range"

def check_rating_columns(df: pd.DataFrame, columns: list[str]) -> None:
    # Character ratings must be 0–5
    for col in columns:
        values = set(df[col].dropna().unique())
        assert values.issubset({0, 1, 2, 3, 4, 5}), f"{col} invalid rating"

def inspect_ordered_category(df: pd.DataFrame, col: str) -> None:
    # Ordered categorical validation
    cat = df[col].cat
    print(f"\n{col}")
    print("categories:", list(cat.categories))
    print("ordered:", cat.ordered)
    print(df[col].value_counts(dropna=False))

def check_row_count(raw: pd.DataFrame, clean: pd.DataFrame) -> None:
    # Row count sanity check (very important)
    assert len(raw) == len(clean), "Row count changed during cleaning"


if __name__ == "__main__":

    raw_df = load_raw_star_wars()
    clean_df = clean_all(raw_df.copy())

    check_row_count(raw_df, clean_df)

    check_boolean_columns(
        clean_df,
        [
            "seen_star_wars",
            "fan_star_wars",
            "familiar_expanded_universe",
            "fan_expanded_universe",
            "fan_star_trek",
        ],
    )

    check_rank_columns(
        clean_df,
        ["rank_ep1", "rank_ep2", "rank_ep3", "rank_ep4", "rank_ep5", "rank_ep6"],
    )

    check_rating_columns(
        clean_df,
        [
            "rating_han_solo",
            "rating_luke_skywalker",
            "rating_princess_leia_organa",
            "rating_anakin_skywalker",
            "rating_obi_wan_kenobi",
            "rating_emperor_palpatine",
            "rating_darth_vader",
            "rating_lando_calrissian",
            "rating_boba_fett",
            "rating_c-3p0",
            "rating_r2_d2",
            "rating_jar_jar_binks",
            "rating_padme_amidala",
            "rating_yoda",
        ],
    )

    inspect_ordered_category(clean_df, "age_group")
    inspect_ordered_category(clean_df, "household_income")
    inspect_ordered_category(clean_df, "education_level")

    print("\n✅ Cleaned-data EDA passed")

