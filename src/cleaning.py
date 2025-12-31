import pandas as pd


def clean_seen_fun_columns(df: pd.DataFrame) -> pd.DataFrame:
    seen_fun_columns = ["seen_star_wars", "fan_star_wars"]

    df[seen_fun_columns] = df[seen_fun_columns].apply(
        lambda col: col.map({"Yes": True, "No": False}).astype("boolean")
    )
    return df


def clean_fan_star_wars_column(df: pd.DataFrame) -> pd.DataFrame:
    df["fan_star_wars"] = df["fan_star_wars"].map({"Yes": True, "No": False})
    return df


def clean_seen_ep_columns(df: pd.DataFrame) -> pd.DataFrame:
    seen_columns = [
        "seen_ep1_phantom_menace",
        "seen_ep2_attack_clones",
        "seen_ep3_revenge_sith",
        "seen_ep4_new_hope",
        "seen_ep5_empire_strikes_back",
        "seen_ep6_return_jedi",
    ]
    df[seen_columns] = df[seen_columns].notna()
    return df


def clean_rank_ep_columns(df: pd.DataFrame) -> pd.DataFrame:
    rank_ep_columns = [
        "rank_ep1",
        "rank_ep2",
        "rank_ep3",
        "rank_ep4",
        "rank_ep5",
        "rank_ep6",
    ]
    df[rank_ep_columns] = df[rank_ep_columns].astype("Int64")
    return df


def clean_rank_character_columns(df: pd.DataFrame) -> pd.DataFrame:
    rank_character_columns = [
        'rating_han_solo', 'rating_luke_skywalker', 'rating_princess_leia_organa', 'rating_anakin_skywalker',
        'rating_obi_wan_kenobi', 'rating_emperor_palpatine', 'rating_darth_vader', 'rating_lando_calrissian',
        'rating_boba_fett', 'rating_c-3p0', 'rating_r2_d2', 'rating_jar_jar_binks', 'rating_padme_amidala',
        'rating_yoda',
    ]
    rating_map = {
        "Very favorably": 5,
        "Somewhat favorably": 4,
        "Neither favorably nor unfavorably (neutral)": 3,
        "Somewhat unfavorably": 2,
        "Very unfavorably": 1,
        "Unfamiliar (N/A)": 0,  # Another option - "Unfamiliar (N/A)": pd.NA
    }
    for col in rank_character_columns:
        df[col] = (
            df[col]
            .map(rating_map)  # maps known ratings → numbers
            .astype("Int64")  # keeps NaN as <NA>
        )
    return df


def clean_who_shot_first(df: pd.DataFrame) -> pd.DataFrame:
    df["who_shot_first"] = (
        df["who_shot_first"]
        .where(df["who_shot_first"].isin(["Han", "Greedo"])))
    df["who_shot_first"] = df["who_shot_first"].astype("category")
    #  we can convert "I don't understand this question" not to NaN but to something else (if we want to analyze it)
    return df