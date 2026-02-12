from __future__ import annotations
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from src.paths import FIGURES_DIR
from src.io_utils import load_clean_star_wars


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
    }
    # "education": {"High school": "High school", "Bachelor": "Bachelor", ...}
}


# =========================
# DATA TRANSFORMATION
# =========================

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

    # Drop rows where the user did not provide a rating
    long_df = long_df.dropna(subset=[value_name])

    # Return the cleaned long-format dataframe
    return long_df


def sanity_check_rank_percentages_multi(
    long_df: pd.DataFrame,
    *,
    variable_name: str,
    value_name: str,
    slice_column: str,
    slice_config: dict[str, dict[str, str]],
) -> pd.DataFrame:
    """
    Computes rank percentage tables per variable (e.g. episode, character),
    split by ONE demographic slice dimension (e.g. gender OR education).

    The output is useful for sanity-checking histogram percentages.
    """

    # Ensure the requested slice column exists in the configuration dictionary
    if slice_column not in slice_config:
        raise ValueError(
            f"Unknown slice column '{slice_column}'. "
            f"Available options: {list(slice_config.keys())}"
        )

    # Retrieve the mapping of raw demographic values to display labels
    # Example: {"Male": "Male", "Female": "Female"}
    slice_map = slice_config[slice_column]

    # Extract slice values in the desired logical display order
    # Example: ["Male", "Female"]
    slices = list(slice_map.keys())

    # Create an empty dictionary to store frequency tables per slice
    tables: dict[str, pd.DataFrame] = {}

    # Loop over each slice value (e.g. Male, Female)
    for raw_value in slices:

        # Filter the dataframe to only rows belonging to the current slice
        slice_df = long_df.loc[long_df[slice_column] == raw_value]

        # Create a normalized crosstab:
        #   - rows    → main variable (e.g. Episode I, Episode II)
        #   - columns → rank values (1–6)
        #   - normalize="index" ensures each row sums to 1
        freq = (
            pd.crosstab(
                slice_df[variable_name],   # rows: variable values
                slice_df[value_name],      # columns: ranking values
                normalize="index",         # normalize within each variable
            )
            * 100                          # convert proportions to percentages
        )

        # Round percentages to one decimal place for readability
        freq = freq.round(1)

        # Store the table using the display label as the dictionary key
        tables[slice_map[raw_value]] = freq

    # Combine all slice tables into a single multi-indexed dataframe
    # Outer index → slice label (e.g. Male, Female)
    # Inner index → variable value (e.g. Episode I, Episode II, ...)
    combined = pd.concat(tables, names=[slice_column, variable_name])

    # Return the combined sanity-check table
    return combined


# =========================
# PLOTTING
# =========================

def plot_rank_histograms_single_slice(
    long_df: pd.DataFrame,
    *,
    variable_name: str,
    value_name: str,
    slice_column: str,
    slice_title: str,
    slice_config: dict[str, dict[str, str]],
    save_path: Path,
) -> None:
    """
    Plots histograms of rankings for a single slice dimension (e.g. gender OR education).
    """

    # Validate that the slice column exists in the configuration
    if slice_column not in slice_config:
        raise ValueError(
            f"Unknown slice column '{slice_column}'. "
            f"Available options: {list(slice_config.keys())}"
        )

    # Extract the ordered slice values (e.g., ["Male", "Female"])
    slice_map = slice_config[slice_column]
    slices = list(slice_map.keys())

    # Extract the ordered variable values (e.g., Episode I → Episode VI)
    variables = long_df[variable_name].dropna().unique().tolist()

    # Build subplot labels and filtering keys
    subplot_labels: list[str] = []
    subplot_pairs: list[tuple[str, str]] = []

    # Create every (variable × slice) combination
    for variable in variables:
        for raw_value in slices:
            subplot_labels.append(f"{variable} — {slice_map[raw_value]}")
            subplot_pairs.append((variable, raw_value))

    # Count total number of subplots
    n = len(subplot_labels)

    # Create vertical subplot layout
    fig, axes = plt.subplots(
        nrows=n,
        ncols=1,
        figsize=(9, 1.5 * n),
        sharex=True,
        sharey=True,
    )

    # Add figure caption
    fig.text(
        0.01, 0.01,
        "Bar colors represent ranking quality (green = best, red = worst)",
        fontsize=9,
        alpha=0.7,
    )

    # Define bins so each rank (1–6) gets its own bar
    bins = np.arange(0.5, 7.5, 1)

    # Iterate over subplots
    for ax, label, (variable, raw_value) in zip(axes, subplot_labels, subplot_pairs):

        # Filter to the current slice (e.g. only Male respondents)
        slice_df = long_df.loc[long_df[slice_column] == raw_value]

        # Filter to the current variable (e.g. Episode V)
        data = slice_df.loc[slice_df[variable_name] == variable, value_name]

        # Count how many valid responses exist
        total = len(data)

        # Handle empty slices gracefully
        if total == 0:
            ax.text(0.5, 0.5, "No data", ha="center", va="center", transform=ax.transAxes)
            ax.set_ylabel(label, rotation=0, labelpad=40, va="center")
            ax.grid(axis="y", alpha=0.3)
            continue

        # Draw histogram
        counts, _, bars = ax.hist(data, bins=bins, edgecolor="black")

        # Add headroom for labels
        ymax = ax.get_ylim()[1]
        ax.set_ylim(0, ymax * 1.06)

        # Label offset
        offset = ax.get_ylim()[1] * 0.015

        # Color bars and add percentages
        for bar, rank in zip(bars, range(1, 7)):
            bar.set_facecolor(RANK_COLORS[rank])
            pct = counts[rank - 1] / total * 100

            if pct >= 3:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + offset,
                    f"{pct:.1f}%",
                    ha="center",
                    va="bottom",
                    fontsize=8,
                    bbox=dict(
                        boxstyle="round,pad=0.2",
                        facecolor="white",
                        edgecolor="none",
                        alpha=0.8,
                    ),
                )

        # Compute summary statistics
        mean = data.mean()
        median = data.median()
        q1, q3 = data.quantile([0.25, 0.75])

        # Draw summary overlays
        ax.axvspan(q1, q3, alpha=0.2, color="gray")
        ax.axvline(median, linestyle="-", linewidth=2, color="black", alpha=0.8)
        ax.axvline(mean, linestyle="--", linewidth=2, color="#2b83ba", alpha=0.8)

        # Label subplot
        ax.set_ylabel(label, rotation=0, labelpad=40, va="center")
        ax.grid(axis="y", alpha=0.3)

    # Label x-axis once
    axes[-1].set_xlabel("Rank (1 = best)")

    # Global legend
    handles = [
        plt.Line2D([0], [0], color="black", linestyle="-", linewidth=2, label="Median"),
        plt.Line2D([0], [0], color="#2b83ba", linestyle="--", linewidth=2, label="Mean"),
        plt.Rectangle((0, 0), 1, 1, color="gray", alpha=0.2, label="IQR"),
    ]

    fig.legend(handles=handles, loc="upper right", bbox_to_anchor=(0.98, 0.98))

    # Global title
    fig.suptitle(f"{variable_name.title()} Distributions by {slice_title}")

    # Layout polish
    plt.tight_layout(rect=(0, 0, 1, 0.96))

    # Ensure output directory exists
    save_path.parent.mkdir(parents=True, exist_ok=True)

    # Save figure
    plt.savefig(save_path)

    # Show figure
    plt.show()

from typing import Literal
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path


def plot_rank_histograms_single_slice_horizontal_grid(
    long_df: pd.DataFrame,
    *,
    variable_name: str,
    value_name: str,
    slice_column: str,
    slice_title: str,
    slice_config: dict[str, dict[str, str]],
    better: Literal["low", "high"],   # "low" = smaller is better (ranks), "high" = larger is better (ratings)
    ncols: int | None = None,         # number of histograms per row (default = number of slice values)
    save_path: Path,
) -> None:
    """
    Plot horizontal histograms in a flat grid for one slice dimension.

    Each subplot shows the distribution of `value_name` for one `variable_name`
    within one category of `slice_column`.

    The `better` parameter controls:
    - Axis direction (best value appears at the top)
    - Color semantics (green = best, red = worst)

    The `ncols` parameter controls how many histograms appear in each row.
    If None, defaults to the number of slice categories.
    """

    # -------------------------
    # 1. Validate slice column
    # -------------------------

    if slice_column not in slice_config:
        raise ValueError(
            f"Unknown slice column '{slice_column}'. "
            f"Available options: {list(slice_config.keys())}"
        )

    # -----------------------------------------
    # 2. Resolve slice ordering & display names
    # -----------------------------------------

    slice_map = slice_config[slice_column]
    slices = list(slice_map.keys())

    # -----------------------------------------
    # 3. Determine which variables to plot
    # -----------------------------------------

    variables = long_df[variable_name].dropna().unique().tolist()

    # -----------------------------------------
    # 4. Build plotting grid layout
    # -----------------------------------------

    cells: list[tuple[str, str]] = [
        (variable, raw_value)
        for variable in variables
        for raw_value in slices
    ]

    n_cells = len(cells)

    if ncols is None:
        ncols = len(slices)

    nrows = int(np.ceil(n_cells / ncols))

    fig, axes = plt.subplots(
        nrows=nrows,
        ncols=ncols,
        figsize=(2.0 * ncols, 3.2 * nrows),
        sharex=True,
        sharey=True,
    )

    axes = np.asarray(axes).reshape(nrows, ncols)

    fig.text(
        0.01, 0.01,
        "Bar colors represent quality (green = best, red = worst)",
        fontsize=9,
        alpha=0.7,
    )

    # -----------------------------------------
    # 5. Define histogram bins (1–6 ranking)
    # -----------------------------------------

    bins = np.arange(0.5, 7.5, 1)
    min_val = int(bins[0] + 0.5)
    max_val = int(bins[-1] - 0.5)

    # -----------------------------------------
    # 6. Plot each histogram cell
    # -----------------------------------------

    for ax, (variable, raw_value) in zip(axes.flat, cells):

        slice_df = long_df.loc[long_df[slice_column] == raw_value]
        data = slice_df.loc[slice_df[variable_name] == variable, value_name]
        total = len(data)

        if total == 0:
            ax.text(
                0.5, 0.5,
                "No data",
                ha="center",
                va="center",
                transform=ax.transAxes,
                fontsize=9,
                alpha=0.6,
            )
            ax.grid(axis="x", alpha=0.3)
            continue

        counts, _, bars = ax.hist(
            data,
            bins=bins,
            edgecolor="black",
            orientation="horizontal",
        )

        xmax = counts.max()
        ax.set_xlim(0, xmax * 2.0)
        offset = ax.get_xlim()[1] * 0.02

        for bar, value in zip(bars, range(min_val, max_val + 1)):

            if better == "low":
                color_key = value
            elif better == "high":
                color_key = max_val - value + 1
            else:
                raise ValueError("better must be either 'low' or 'high'")

            bar.set_facecolor(RANK_COLORS[color_key])

            pct = counts[value - min_val] / total * 100

            if pct >= 3:
                ax.text(
                    bar.get_width() + offset,
                    bar.get_y() + bar.get_height() / 2,
                    f"{pct:.1f}%",
                    va="center",
                    ha="left",
                    fontsize=8,
                    bbox=dict(
                        boxstyle="round,pad=0.1",
                        facecolor="white",
                        edgecolor="none",
                        alpha=0.8,
                    ),
                )

        mean = data.mean()
        median = data.median()
        q1, q3 = data.quantile([0.25, 0.75])

        ax.axhspan(q1, q3, alpha=0.2, color="gray")
        ax.axhline(median, linestyle="-", linewidth=2, color="black", alpha=0.8)
        ax.axhline(mean, linestyle="--", linewidth=2, color="#2b83ba", alpha=0.8)

        if better == "low":
            ax.invert_yaxis()

        ax.set_title(f"{variable} — {slice_map[raw_value]}", fontsize=9)
        ax.grid(axis="x", alpha=0.3)

    # -----------------------------------------
    # 7. Turn off unused axes
    # -----------------------------------------

    for ax in axes.flat[len(cells):]:
        ax.axis("off")

    # -----------------------------------------
    # 8. Global labels & legend
    # -----------------------------------------

    fig.supxlabel("Count of responses")

    if better == "low":
        fig.supylabel(f"{value_name.title()} (1 = best)")
    else:
        fig.supylabel(f"{value_name.title()} (higher = better)")

    handles = [
        plt.Line2D([0], [0], color="black", linestyle="-", linewidth=2, label="Median"),
        plt.Line2D([0], [0], color="#2b83ba", linestyle="--", linewidth=2, label="Mean"),
        plt.Rectangle((0, 0), 1, 1, color="gray", alpha=0.2, label="IQR"),
    ]

    fig.legend(handles=handles, loc="upper right", bbox_to_anchor=(0.98, 1), ncol=2)

    fig.suptitle(f"{variable_name.title()} Distributions by {slice_title}")
    plt.tight_layout(rect=(0, 0, 1, 0.96))

    save_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path)
    plt.show()

def character_rating_gender(df: pd.DataFrame) -> None:
    long_df = melt_variable(
        df,
        variable_columns=CHARACTER_RATING_COLUMNS,
        variable_name="character rating",
        value_name="rating",
    )

    plot_rank_histograms_single_slice_horizontal_grid(
        long_df,
        variable_name="character rating",
        value_name="rating",
        better="high",
        slice_column="gender",
        slice_title="Gender",
        slice_config=DEMOGRAPHICS_COLUMNS,
        save_path=FIGURES_DIR / "character_rating_gender.png",
    )

    print(
        sanity_check_rank_percentages_multi(
            long_df,
            variable_name="character rating",
            value_name="rating",
            slice_column="gender",
            slice_config=DEMOGRAPHICS_COLUMNS,
        )
    )

def episode_ranking_gender(df: pd.DataFrame) -> None:
    long_df = melt_variable(
        df,
        variable_columns=EPISODE_RANK_COLUMNS,
        variable_name="episode ranking",
        value_name="rank",
    )

    plot_rank_histograms_single_slice_horizontal_grid(
        long_df,
        variable_name="episode ranking",
        value_name="rank",
        better="low",
        slice_column="gender",
        slice_title="Gender",
        slice_config=DEMOGRAPHICS_COLUMNS,
        save_path=FIGURES_DIR / "episode_ranking_gender.png",
    )

    print(
        sanity_check_rank_percentages_multi(
            long_df,
            variable_name="episode ranking",
            value_name="rank",
            slice_column="gender",
            slice_config=DEMOGRAPHICS_COLUMNS,
        )
    )

def episode_ranking_age_group(df: pd.DataFrame) -> None:
    long_df = melt_variable(
        df,
        variable_columns=EPISODE_RANK_COLUMNS,
        variable_name="episode ranking",
        value_name="rank",
    )

    plot_rank_histograms_single_slice_horizontal_grid(
        long_df,
        variable_name="episode ranking",
        value_name="rank",
        better="low",
        slice_column="age_group",
        slice_title="Age Group",
        slice_config=DEMOGRAPHICS_COLUMNS,
        save_path=FIGURES_DIR / "episode_ranking_age_group.png",
    )

    print(
        sanity_check_rank_percentages_multi(
            long_df,
            variable_name="episode ranking",
            value_name="rank",
            slice_column="age_group",
            slice_config=DEMOGRAPHICS_COLUMNS,
        )
    )

def episode_ranking_household_income(df: pd.DataFrame) -> None:
    long_df = melt_variable(
        df,
        variable_columns=EPISODE_RANK_COLUMNS,
        variable_name="episode ranking",
        value_name="rank",
    )

    plot_rank_histograms_single_slice_horizontal_grid(
        long_df,
        variable_name="episode ranking",
        value_name="rank",
        better="low",
        slice_column="household_income",
        slice_title="Household Income",
        slice_config=DEMOGRAPHICS_COLUMNS,
        save_path=FIGURES_DIR / "episode_ranking_household_income.png",
    )

    print(
        sanity_check_rank_percentages_multi(
            long_df,
            variable_name="episode ranking",
            value_name="rank",
            slice_column="household_income",
            slice_config=DEMOGRAPHICS_COLUMNS,
        )
    )

# =========================
# MAIN
# =========================

def main() -> None:
    df = load_clean_star_wars()

    episode_ranking_household_income(df)


if __name__ == "__main__":
    main()
