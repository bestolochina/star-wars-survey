from __future__ import annotations
from pathlib import Path
import numpy as np
from src.paths import FIGURES_DIR
import matplotlib.pyplot as plt
import pandas as pd
from src.io_utils import load_clean_star_wars


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

# Colors to use for each ranking (1 = best, 6 = worst)
RANK_COLORS = {
    1: "#1a9641",  # dark green
    2: "#a6d96a",
    3: "#fdae61",
    4: "#f46d43",
    5: "#d73027",
    6: "#a50026",  # dark red
}

# Demographics categories (used elsewhere in the project)
DEMOGRAPHICS_COLUMNS: dict[str, dict[str, str]] = {
    "gender": {
        "Male": "Male",
        "Female": "Female",
    }
}


def melt_episode_ranks(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts episode ranking columns from wide format to long format
    while preserving all demographic and respondent-level columns.
    """

    # Identify columns that should remain as identifiers (everything except episode ranks)
    id_vars = [col for col in df.columns if col not in EPISODE_RANK_COLUMNS]

    # Melt episode ranking columns into long format
    long_df = df.melt(
        id_vars=id_vars,                          # keep demographics and respondent info
        value_vars=EPISODE_RANK_COLUMNS.keys(),   # columns to unpivot
        var_name="episode",                       # name of new episode column
        value_name="rank",                        # name of new rank column
    )

    # Convert internal episode column names to human-readable labels
    long_df["episode"] = long_df["episode"].map(EPISODE_RANK_COLUMNS)

    # Drop rows where users did not rank that episode
    long_df = long_df.dropna(subset=["rank"])

    return long_df


def plot_episode_rank_histograms(
    long_df: pd.DataFrame,
    demographics: str,
    demographics_title: str,
    *,
    save_path: Path,
) -> None:
    """
    Plots one histogram per episode per demographic slice.
    The ordering and allowed categories are controlled by DEMOGRAPHICS_COLUMNS.
    """

    # Get readable episode names in their defined order (Episode I → Episode VI)
    episodes = list(EPISODE_RANK_COLUMNS.values())

    # Ensure the requested demographic column exists in the configuration dictionary
    if demographics not in DEMOGRAPHICS_COLUMNS:
        raise ValueError(
            f"Unknown demographics '{demographics}'. "
            f"Available options: {list(DEMOGRAPHICS_COLUMNS.keys())}"
        )

    # Get the allowed demographic values and their display labels
    # Example: {"Male": "Male", "Female": "Female"}
    demographic_map = DEMOGRAPHICS_COLUMNS[demographics]

    # Extract demographic values in logical display order
    # Example: ["Male", "Female"]
    slices = list(demographic_map.keys())

    # Prepare human-readable subplot labels (e.g., "Episode IV — Male")
    subplot_labels: list[str] = []

    # Prepare (episode, demographic) pairs for filtering the dataframe
    subplot_pairs: list[tuple[str, str]] = []

    # Create every (episode × demographic) combination in deterministic order
    for episode in episodes:
        for raw_value in slices:

            # Convert raw demographic value to display label (can be changed later)
            display_value = demographic_map[raw_value]

            # Build the label shown on the subplot
            subplot_labels.append(f"{episode} — {display_value}")

            # Store filtering keys (used later when slicing the dataframe)
            subplot_pairs.append((episode, raw_value))

    # Count how many subplots are needed in total
    n = len(subplot_labels)

    # Create a vertical stack of subplots (one per episode × demographic slice)
    fig, axes = plt.subplots(
        nrows=n,                  # One subplot per row
        ncols=1,                  # Single column layout
        figsize=(9, 1.5 * n),     # Figure height scales with number of subplots
        sharex=True,              # Share x-axis across all subplots
        sharey=True,              # Share y-axis across all subplots
    )

    # Add a small explanatory caption to the figure
    fig.text(
        0.01, 0.01,
        "Bar colors represent ranking quality (green = best, red = worst)",
        fontsize=9,
        alpha=0.7,
    )

    # Define histogram bins so that each integer rank (1–6) has its own bin
    bins = np.arange(0.5, 7.5, 1)

    # Loop over each subplot axis and its corresponding (episode, demographic) pair
    for ax, label, (episode, raw_value) in zip(axes, subplot_labels, subplot_pairs):

        # Filter the dataframe to only rows belonging to the current demographic slice
        slice_df = long_df.loc[long_df[demographics] == raw_value]

        # From that slice, select only rows for the current episode
        data = slice_df.loc[slice_df["episode"] == episode, "rank"]

        # Count how many valid rankings exist for this episode × demographic group
        total = len(data)

        # If no data exists, display a placeholder and skip plotting
        if total == 0:
            ax.text(
                0.5, 0.5,
                "No data",
                ha="center",
                va="center",
                transform=ax.transAxes,
                fontsize=10,
                alpha=0.6,
            )

            # Set the subplot label
            ax.set_ylabel(label, rotation=0, labelpad=40, va="center")

            # Set x-axis range so empty plots are visually consistent
            ax.set_xlim(0.5, 6.5)

            # Add grid lines for visual consistency
            ax.grid(axis="y", alpha=0.3)

            # Skip further plotting logic for this subplot
            continue

        # Plot the histogram of ranking values for this slice
        counts, _, bars = ax.hist(
            data,
            bins=bins,
            edgecolor="black",
        )

        # Get the current maximum y-axis value
        ymax = ax.get_ylim()[1]

        # Slightly increase the y-axis limit to leave space for labels above bars
        ax.set_ylim(0, ymax * 1.06)

        # Compute a small vertical offset for placing percentage labels above bars
        offset = ax.get_ylim()[1] * 0.015

        # Loop over each histogram bar and its corresponding rank value (1–6)
        for bar, rank in zip(bars, range(1, 7)):

            # Set the bar color based on ranking quality
            bar.set_facecolor(RANK_COLORS[rank])

            # Compute the percentage of users who gave this rank
            pct = counts[rank - 1] / total * 100

            # Only draw percentage labels if they are visually meaningful
            if pct >= 3:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,     # Center text horizontally
                    bar.get_height() + offset,             # Place text above bar
                    f"{pct:.1f}%",                          # Format percentage
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

        # Compute summary statistics for this distribution
        mean = data.mean()                 # Arithmetic mean
        median = data.median()             # Median (50th percentile)
        q1, q3 = data.quantile([0.25, 0.75])  # 25th and 75th percentiles

        # Shade the interquartile range (middle 50% of the data)
        ax.axvspan(q1, q3, alpha=0.2, color="gray")

        # Draw a solid vertical line at the median
        ax.axvline(median, linestyle="-", linewidth=2, color="black", alpha=0.8)

        # Draw a dashed vertical line at the mean
        ax.axvline(mean, linestyle="--", linewidth=2, color="#2b83ba", alpha=0.8)

        # Label the subplot with episode and demographic
        ax.set_ylabel(label, rotation=0, labelpad=40, va="center")

        # Add light horizontal grid lines
        ax.grid(axis="y", alpha=0.3)

    # Label the x-axis only on the bottom subplot
    axes[-1].set_xlabel("Rank (1 = best)")

    # Manually create legend handles so the legend appears only once
    handles = [
        plt.Line2D([0], [0], color="black", linestyle="-", linewidth=2, label="Median"),
        plt.Line2D([0], [0], color="#2b83ba", linestyle="--", linewidth=2, label="Mean"),
        plt.Rectangle((0, 0), 1, 1, color="gray", alpha=0.2, label="IQR"),
    ]

    # Attach the legend to the figure (not to individual subplots)
    fig.legend(
        handles=handles,
        loc="upper right",
        bbox_to_anchor=(0.98, 0.98),
    )

    # Add a global title to the figure
    fig.suptitle("Episode Rank Distributions by " + demographics_title)

    # Adjust layout so subplot labels and title do not overlap
    plt.tight_layout(rect=(0, 0, 1, 0.96))

    # Create the output directory if it does not exist
    save_path.parent.mkdir(parents=True, exist_ok=True)

    # Save the figure to disk
    plt.savefig(save_path)

    # Display the figure to the screen
    plt.show()

def sanity_check_rank_percentages(
    long_df: pd.DataFrame,
    demographics: str,
) -> pd.DataFrame:
    """
    Computes rank percentage tables per episode, optionally split by a demographic slice.
    The output is useful for sanity-checking histogram percentages.
    """

    # Ensure the requested demographic column exists in the configuration dictionary
    if demographics not in DEMOGRAPHICS_COLUMNS:
        raise ValueError(
            f"Unknown demographics '{demographics}'. "
            f"Available options: {list(DEMOGRAPHICS_COLUMNS.keys())}"
        )

    # Get the mapping of raw demographic values to display labels
    # Example: {"Male": "Male", "Female": "Female"}
    demographic_map = DEMOGRAPHICS_COLUMNS[demographics]

    # Extract demographic values in the desired logical order
    slices = list(demographic_map.keys())

    # Create an empty dictionary to store frequency tables per demographic slice
    tables: dict[str, pd.DataFrame] = {}

    # Loop over each demographic slice (e.g. Male, Female)
    for raw_value in slices:

        # Filter the dataframe to only rows belonging to the current demographic slice
        slice_df = long_df.loc[long_df[demographics] == raw_value]

        # Create a normalized crosstab:
        #   - rows   → episodes
        #   - columns → rank values (1–6)
        #   - normalize="index" → percentages sum to 1 across each row (episode)
        freq = (
            pd.crosstab(
                slice_df["episode"],   # rows: episode
                slice_df["rank"],      # columns: rank
                normalize="index",     # normalize per episode
            )
            * 100                     # convert proportions to percentages
        )

        # Round percentages to one decimal place for readability
        freq = freq.round(1)

        # Store the table using the display label as the key
        tables[demographic_map[raw_value]] = freq

    # Combine all slice tables into a single multi-indexed dataframe
    # Outer index  → demographic label (e.g. Male, Female)
    # Inner index  → episode (Episode I, Episode II, ...)
    combined = pd.concat(tables, names=[demographics, "episode"])

    # Return the combined sanity-check table
    return combined


def main() -> None:
    # Load the cleaned Star Wars survey dataset
    df = load_clean_star_wars()

    # Convert episode rankings to long format
    long_df = melt_episode_ranks(df)

    plot_episode_rank_histograms(long_df,
                                 demographics="gender",
                                 demographics_title="Gender",
                                 save_path=FIGURES_DIR / "episode_ranking_gender")

    print(sanity_check_rank_percentages(long_df, demographics="gender"))


if __name__ == "__main__":
    main()
