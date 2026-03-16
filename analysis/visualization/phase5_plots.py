# analysis/visualization/phase5_plots.py

from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from src.config import CHARACTER_RATING_COLUMNS


# ==========================================================
# Audience × Character Ideological Bloc Heatmap
# ==========================================================

def plot_audience_character_bloc_affinity_heatmap(
    affinity: pd.DataFrame,
    path
) -> pd.DataFrame:

    # Convert wide → long
    long_df = affinity.melt(
        id_vars="audience_cluster",
        var_name="character_ideological_bloc",
        value_name="affinity",
    )

    long_df["character_ideological_bloc"] = long_df[
        "character_ideological_bloc"
    ].astype(int)

    # Pivot for heatmap
    heatmap_df = long_df.pivot(
        index="audience_cluster",
        columns="character_ideological_bloc",
        values="affinity",
    )

    # Create figure
    plt.figure(figsize=(6, 4))

    sns.heatmap(
        heatmap_df,
        annot=True,
        cmap="RdYlBu_r",
        center=3,
        linewidths=0.5,
        fmt=".2f",
    )

    plt.xlabel("Character Ideological Bloc")
    plt.ylabel("Audience Cluster")
    plt.title("Audience × Character Ideological Bloc Affinity")

    # Save figure
    plt.savefig(
        path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    return heatmap_df


# ==========================================================
# Audience × Character Ideology Map
# ==========================================================

def plot_audience_character_ideology_map(
    character_coords: pd.DataFrame,
    audience_coords: pd.DataFrame,
    path: Path,
) -> None:

    plt.figure(figsize=(7, 6))

    # --- characters ---
    plt.scatter(
        character_coords["ideology_axis_1"],
        character_coords["ideology_axis_2"],
        s=120,
        alpha=0.8,
        color="steelblue",
        label="Characters",
    )

    for _, row in character_coords.iterrows():
        plt.text(
            row["ideology_axis_1"],
            row["ideology_axis_2"],
            row["character"],
            fontsize=9,
            ha="center",
            va="bottom",
        )

    # --- audience clusters ---
    plt.scatter(
        audience_coords["ideology_axis_1"],
        audience_coords["ideology_axis_2"],
        s=300,
        marker="X",
        color="darkred",
        label="Audience Clusters",
    )

    for _, row in audience_coords.iterrows():
        plt.text(
            row["ideology_axis_1"],
            row["ideology_axis_2"],
            f"Cluster {row['audience_cluster']}",
            fontsize=11,
            ha="center",
            va="center",
            fontweight="bold",
        )

    plt.axhline(0, linewidth=1)
    plt.axvline(0, linewidth=1)

    plt.xlabel("Character Ideology Axis 1")
    plt.ylabel("Character Ideology Axis 2")

    plt.title("Audience–Character Ideological Alignment Map")

    plt.legend()

    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()


# ==========================================================
# Cluster Character Preference Profiles
# ==========================================================

def plot_cluster_character_preference_profiles(
    respondents: pd.DataFrame,
    path: Path,
) -> pd.DataFrame:

    # dataset column names
    rating_cols = list(CHARACTER_RATING_COLUMNS.keys())

    # compute cluster means
    profile_df = (
        respondents
        .groupby("audience_cluster")[rating_cols]
        .mean()
        .T
    )

    # replace column names with human-readable character names
    profile_df.index = [
        CHARACTER_RATING_COLUMNS[col]
        for col in profile_df.index
    ]

    profile_df["mean_rating"] = profile_df.mean(axis=1)
    profile_df = profile_df.sort_values("mean_rating", ascending=False)
    profile_df = profile_df.drop(columns="mean_rating")

    plt.figure(figsize=(12, 6))

    for cluster in profile_df.columns:
        plt.plot(
            profile_df.index,
            profile_df[cluster],
            marker="o",
            linewidth=2,
            label=f"Cluster {cluster}",
        )

    plt.xticks(rotation=45, ha="right")

    plt.ylabel("Average Rating")
    plt.xlabel("Character")

    plt.title("Audience Cluster Character Preference Profiles")

    plt.legend()
    plt.grid(alpha=0.3)

    plt.tight_layout()

    plt.savefig(path, dpi=300)
    plt.close()

    return profile_df


# ==========================================================
# Audience–Character Ideology Alignment Map
# ==========================================================

def plot_audience_character_ideology_alignment_map(
        character_coords: pd.DataFrame,
        cluster_coords: pd.DataFrame,
        save_path,
) -> None:

    fig, ax = plt.subplots(figsize=(10, 8))

    # Characters
    ax.scatter(
        character_coords["ideology_axis_1"],
        character_coords["ideology_axis_2"],
        s=120,
        alpha=0.9,
        label="Characters",
    )

    for _, row in character_coords.iterrows():
        ax.annotate(
            row["character"],
            (row["ideology_axis_1"], row["ideology_axis_2"]),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=9,
        )

    # Audience clusters
    ax.scatter(
        cluster_coords["PC1"],
        cluster_coords["PC2"],
        s=200,
        marker="X",
        label="Audience Clusters",
    )

    for _, row in cluster_coords.iterrows():
        ax.text(
            row["PC1"],
            row["PC2"],
            f"Cluster {int(row['audience_cluster'])}",
            fontsize=11,
            fontweight="bold",
        )

    ax.axhline(0)
    ax.axvline(0)

    ax.set_title("Audience–Character Ideological Alignment Map")
    ax.set_xlabel("Ideological Axis 1")
    ax.set_ylabel("Ideological Axis 2")

    ax.legend()

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
