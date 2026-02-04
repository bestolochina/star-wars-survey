from __future__ import annotations
from pathlib import Path
import numpy as np
from src.paths import FIGURES_DIR
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D
from src.io_utils import load_clean_star_wars
import math

RATING_COLUMNS: dict[str, str] = {
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

def overall_rating_behavior(df: pd.DataFrame, save_path: Path) -> None:
    columns = list(RATING_COLUMNS)

    missing_summary = (
        df[columns]
        .isna()
        .mean()
        .mul(100)
        .round(1)
        .sort_values(ascending=False)
    )

    print("Missing_summary:")
    print(missing_summary)
    print()

    n_cols = 5
    n_rows = math.ceil(len(columns) / n_cols)

    # ---------- Compute global Y max ----------
    global_max = 0
    for column in columns:
        counts = df[column].value_counts(dropna=False)
        global_max = max(global_max, counts.max() * 1.15)

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, 10))
    axes = axes.flatten()

    for i, column in enumerate(columns):
        counts = df[column].value_counts(dropna=False).sort_index()
        percent = counts / counts.sum() * 100

        rating_dist = pd.DataFrame({
            "count": counts,
            "percent": percent.round(1),
        })

        counts.plot(kind="bar", ax=axes[i])
        axes[i].set_title(RATING_COLUMNS[column])
        axes[i].set_ylim(0, global_max)   # ✅ same Y scale
        axes[i].set_xlabel("")
        axes[i].set_ylabel("Count")

        # ✅ Centered x tick labels
        axes[i].set_xticklabels(axes[i].get_xticklabels(), rotation=0, ha="center")

        # ✅ Color last bar (NA) gray
        for label, bar in zip(axes[i].get_xticklabels(), axes[i].patches):
            if not label.get_text().isdigit():
                bar.set_color("lightgray")

        # ✅ Add value labels on bars
        for container in axes[i].containers:
            axes[i].bar_label(container, fmt="%d", label_type="edge", padding=2)

        print(f"\n{column}")
        print(rating_dist)

    # Remove unused axes
    for j in range(len(columns), len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()

    save_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path)
    plt.show()


def main() -> None:
    df = load_clean_star_wars()

    overall_rating_behavior(df, save_path=FIGURES_DIR / "character_rating_distributions.png")


if __name__ == "__main__":
    main()
