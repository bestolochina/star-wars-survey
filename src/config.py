# =========================
# CONFIGURATION DICTIONARIES
# =========================

# Mapping from dataset column names to human-readable character names
CHARACTER_RATING_COLUMNS: dict[str, str] = {
    "rating_han_solo":              "Han Solo",
    "rating_luke_skywalker":        "Luke Skywalker",
    "rating_princess_leia_organa":  "Princess Leia Organa",
    "rating_anakin_skywalker":      "Anakin Skywalker",
    "rating_obi_wan_kenobi":        "Obi Wan Kenobi",
    "rating_emperor_palpatine":     "Emperor Palpatine",
    "rating_darth_vader":           "Darth Vader",
    "rating_lando_calrissian":      "Lando Calrissian",
    "rating_boba_fett":             "Boba Fett",
    "rating_c-3p0":                 "C-3P0",
    "rating_r2_d2":                 "R2-D2",
    "rating_jar_jar_binks":         "Jar-Jar Binks",
    "rating_padme_amidala":         "Padme Amidala",
    "rating_yoda":                  "Yoda",
}

# Mapping from dataset column names to readable episode labels
EPISODE_RANK_COLUMNS: dict[str, str] = {
    "rank_ep1": "Episode I",
    "rank_ep2": "Episode II",
    "rank_ep3": "Episode III",
    "rank_ep4": "Episode IV",
    "rank_ep5": "Episode V",
    "rank_ep6": "Episode VI",
}

# Colors used for each ranking (1 = best, 6 = worst)
RANK_COLORS = {
    1: "#1a9641",   # dark green
    2: "#a6d96a",
    3: "#fdae61",
    4: "#f46d43",
    5: "#d73027",
    6: "#a50026",   # dark red
}

# Allowed demographic slices and their display order
DEMOGRAPHICS_COLUMNS: dict[str, dict[str, str]] = {
    "gender": {
        "Male": "Male",
        "Female": "Female",
    },
    "age_group": {
        "18-29": "18-29",
        "30-44": "30-44",
        "45-60": "45-60",
        "60+": "60+",
    },
    "household_income": {
        "$0–24k": "$0–24k",
        "$25–49k": "$25–49k",
        "$50–99k": "$50–99k",
        "$100–149k": "$100–149k",
        "$150k+": "$150k+",
    },
    "education_level": {
        "Less than HS": "Less than HS",
        "High school": "High school",
        "Some college / Associate": "Some college / Associate",
        "Bachelor’s": "Bachelor’s",
        "Graduate": "Graduate",
    },
    "census_region": {
        "East North Central": "East North Central",
        "Pacific": "Pacific",
        "South Atlantic": "South Atlantic",
        "Middle Atlantic": "Middle Atlantic",
        "West South Central": "West South Central",
        "West North Central": "West North Central",
        "Mountain": "Mountain",
        "New England": "New England",
        "East South Central": "East South Central",
    }
}

MIN_GROUP_SIZE = 30