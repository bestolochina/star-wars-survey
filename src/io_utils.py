from src.paths import RAW_DATA_DIR, CLEAN_DATA_DIR
import pandas as pd

# ---------- project paths ----------

RAW_FILE = RAW_DATA_DIR / "star_wars.csv"
CLEAN_FILE = CLEAN_DATA_DIR / "star_wars_clean.parquet"

COLUMNS = [
    "respondent_id",
    "seen_star_wars",
    "fan_star_wars",
    "seen_ep1_phantom_menace",
    "seen_ep2_attack_clones",
    "seen_ep3_revenge_sith",
    "seen_ep4_new_hope",
    "seen_ep5_empire_strikes_back",
    "seen_ep6_return_jedi",
    "rank_ep1",
    "rank_ep2",
    "rank_ep3",
    "rank_ep4",
    "rank_ep5",
    "rank_ep6",
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
    "who_shot_first",
    "familiar_expanded_universe",
    "fan_expanded_universe",
    "fan_star_trek",
    "gender",
    "age_group",
    "household_income",
    "education_level",
    "census_region",
]

def load_raw_star_wars() -> pd.DataFrame:
    """Load raw Star Wars survey CSV and assign canonical column names."""

    try:
        df = pd.read_csv(
            RAW_FILE,
            encoding="utf-8",
            skiprows=2,
            header=None,
        )
    except UnicodeDecodeError:
        df = pd.read_csv(
            RAW_FILE,
            encoding="ISO-8859-1",
            skiprows=2,
            header=None,
        )

    assert df.shape[1] == len(COLUMNS), "Column count mismatch"
    df.columns = COLUMNS
    return df

def save_clean_star_wars(df: pd.DataFrame) -> None:
    CLEAN_DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_parquet(CLEAN_FILE, index=False)

def load_clean_star_wars() -> pd.DataFrame:
    return pd.read_parquet(CLEAN_FILE)
