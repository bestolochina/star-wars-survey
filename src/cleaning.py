import pandas as pd


def clean_seen_fun_columns(df: pd.DataFrame) -> pd.DataFrame:
    seen_fun_columns = ["seen_star_wars", "fan_star_wars"]

    df[seen_fun_columns] = df[seen_fun_columns].apply(
        lambda col: col.map({"Yes": True, "No": False}).astype("boolean")
    )
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
    df[seen_columns] = df[seen_columns].notna().astype("boolean")
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
    }
    # "Unfamiliar (N/A)" - option for further analysis
    for col in rank_character_columns:
        df[col] = df[col].map(rating_map).astype("Int64")
    return df


def clean_who_shot_first(df: pd.DataFrame) -> pd.DataFrame:
    df["who_shot_first"] = (
        df["who_shot_first"]
        .where(df["who_shot_first"].isin(["Han", "Greedo"])))
    df["who_shot_first"] = df["who_shot_first"].astype("category")
    #  we can convert "I don't understand this question" not to NaN but to something else (if we want to analyze it)
    return df


def clean_expanded_universe_star_trek(df: pd.DataFrame) -> pd.DataFrame:
    columns = ["familiar_expanded_universe", "fan_expanded_universe", "fan_star_trek"]

    df[columns] = df[columns].apply(
        lambda col: col.map({"Yes": True, "No": False}).astype("boolean")
    )
    return df


def clean_gender(df: pd.DataFrame) -> pd.DataFrame:
    df["gender"] = df["gender"].astype("category")
    return df


def clean_age_group(df: pd.DataFrame) -> pd.DataFrame:
    df["age_group"] = (
        df["age_group"]
        .map({
            "18-29": "18-29",
            "30-44": "30-44",
            "45-60": "45-60",
            "> 60": "60+",
        })
        .astype("category")
    )
    df["age_group"] = df["age_group"].cat.set_categories(
        ["18-29", "30-44", "45-60", "60+"],
        ordered=True
    )
    return df


def clean_household_income(df: pd.DataFrame) -> pd.DataFrame:
    df["household_income"] = (
        df["household_income"]
        .map({
            "$0 - $24,999": "$0–24k",
            "$25,000 - $49,999": "$25–49k",
            "$50,000 - $99,999": "$50–99k",
            "$100,000 - $149,999": "$100–149k",
            "$150,000+": "$150k+",
        })
        .astype("category")
    )
    df["household_income"] = df["household_income"].cat.set_categories(
        ["$0–24k", "$25–49k", "$50–99k", "$100–149k", "$150k+"],
        ordered=True
    )
    return df


def clean_education_level(df: pd.DataFrame) -> pd.DataFrame:
    df["education_level"] = (
        df["education_level"]
        .map({
            "Less than high school degree": "Less than HS",
            "High school degree": "High school",
            "Some college or Associate degree": "Some college / Associate",
            "Bachelor degree": "Bachelor’s",
            "Graduate degree": "Graduate",
        })
        .astype("category")
    )
    df["education_level"] = df["education_level"].cat.set_categories(
        [
            "Less than HS",
            "High school",
            "Some college / Associate",
            "Bachelor’s",
            "Graduate",
        ],
        ordered=True
    )
    return df


def clean_census_region(df: pd.DataFrame) -> pd.DataFrame:
    df["census_region"] = df["census_region"].astype("category")
    return df


def clean_all(df: pd.DataFrame) -> pd.DataFrame:
    df = clean_seen_fun_columns(df)
    df = clean_seen_ep_columns(df)
    df = clean_rank_ep_columns(df)
    df = clean_rank_character_columns(df)
    df = clean_who_shot_first(df)
    df = clean_expanded_universe_star_trek(df)
    df = clean_gender(df)
    df = clean_age_group(df)
    df = clean_household_income(df)
    df = clean_education_level(df)
    df = clean_census_region(df)
    return df