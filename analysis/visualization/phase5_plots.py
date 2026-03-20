# analysis/visualization/phase5_plots.py

from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
import numpy as np


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
# Audience–Character Ideology Alignment Map (Enhanced)
# ==========================================================

def plot_audience_character_ideology_alignment_map(
        character_coords: pd.DataFrame,
        cluster_coords: pd.DataFrame,
        save_path: Path,
) -> None:

    fig, ax = plt.subplots(figsize=(10, 8))

    # -------------------------
    # Characters
    # -------------------------

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
            xytext=(4, 4),
            textcoords="offset points",
            fontsize=9,
        )

    # -------------------------
    # Audience clusters
    # -------------------------

    ax.scatter(
        cluster_coords["PC1"],
        cluster_coords["PC2"],
        s=300,
        marker="X",
        label="Audience Clusters",
    )

    for _, row in cluster_coords.iterrows():

        x = row["PC1"]
        y = row["PC2"]

        ax.text(
            x + 0.1,
            y + 0.06,
            f"C{int(row['audience_cluster'])}",
            fontsize=11,
            fontweight="bold",
            ha="center",
        )

    # -------------------------
    # Convex hull territory
    # -------------------------

    points = cluster_coords[["PC1", "PC2"]].to_numpy()

    if len(points) >= 3:

        hull = ConvexHull(points)

        hull_points = points[hull.vertices]

        polygon = plt.Polygon(
            hull_points,
            fill=False,
            linestyle="--",
            linewidth=2,
            alpha=0.6,
            label="Audience Ideological Space",
        )

        ax.add_patch(polygon)

    # -------------------------
    # Axis guides
    # -------------------------

    ax.axhline(0, linewidth=1)
    ax.axvline(0, linewidth=1)

    ax.set_xlabel("Ideological Axis 1")
    ax.set_ylabel("Ideological Axis 2")

    ax.set_title("Fandom Ideological Landscape")

    ax.legend()

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()



# ==========================================================
# Cluster × Character Heatmap
# ==========================================================

def plot_cluster_character_heatmap(
    matrix: pd.DataFrame,
    path: Path,
) -> None:

    plt.figure(figsize=(12, 6))

    sns.heatmap(
        matrix,
        cmap="RdYlBu_r",
        annot=True,
        fmt=".2f",
        linewidths=0.5,
    )

    plt.title("Audience Cluster × Character Evaluation Heatmap")
    plt.ylabel("Character")
    plt.xlabel("Audience Cluster")

    plt.tight_layout()

    plt.savefig(path, dpi=300)
    plt.close()


# ==========================================================
# Cluster Character Divergence
# ==========================================================

def plot_cluster_character_divergence(
    variance_table: pd.DataFrame,
    path: Path,
) -> None:

    # sort characters by variance
    df = variance_table.sort_values(
        "character_evaluation_variance_across_audience_clusters",
        ascending=False,
    )

    plt.figure(figsize=(10, 6))

    sns.barplot(
        data=df,
        x="character_evaluation_variance_across_audience_clusters",
        y="character",
    )

    plt.title("Character Evaluation Variance Across Audience Clusters")
    plt.xlabel("Evaluation Variance Across Clusters")
    plt.ylabel("Character")

    plt.tight_layout()

    plt.savefig(path, dpi=300)
    plt.close()


# ==========================================================
# Polarization Driver Ranking
# ==========================================================

def plot_polarization_driver_ranking(
    polarization_table: pd.DataFrame,
    path: Path,
) -> None:

    df = polarization_table.sort_values(
        "audience_rating_range",
        ascending=False,
    )

    # mark top 5 polarization drivers
    df["top5"] = False
    df.loc[df.index[:5], "top5"] = True

    plt.figure(figsize=(10, 6))

    palette = {True: "#d95f02", False: "#1b9e77"}

    sns.barplot(
        data=df,
        x="audience_rating_range",
        y="character",
        hue="top5",
        dodge=False,
        palette=palette,
    )

    plt.title("Character Polarization Drivers")
    plt.xlabel("Audience Rating Range (Max − Min Cluster Rating)")
    plt.ylabel("Character")

    handles, _ = plt.gca().get_legend_handles_labels()

    plt.legend(
        handles,
        ["Other Characters", "Top 5"],
        title="Top Polarization Drivers",
    )

    plt.tight_layout()

    plt.savefig(path, dpi=300)
    plt.close()


# ==========================================================
# Cluster Narrative Archetypes
# ==========================================================

def plot_cluster_archetype_profiles(
    archetype_table: pd.DataFrame,
    path: Path,
) -> None:

    df = archetype_table.sort_values("audience_cluster")

    plt.figure(figsize=(8, 5))

    ax = sns.barplot(
        data=df,
        x="audience_cluster",
        y="cluster_ideology_position",
    )

    # annotate archetype labels centered above bars
    for bar, label in zip(ax.patches, df["narrative_archetype"]):
        x = bar.get_x() + bar.get_width() / 2
        y = bar.get_height()

        ax.text(
            x,
            y + 0.05,
            label,
            ha="center",
            va="bottom",
            fontsize=10,
        )

    ax.set_xlabel("Audience Cluster")
    ax.set_ylabel("Ideological Position")
    ax.set_title("Audience Cluster Narrative Archetypes")

    plt.tight_layout()
    plt.savefig(path, dpi=300)
    plt.close()


def plot_character_ideology_force_field(
    character_coords,
    cluster_coords,
    archetype_table,
    output_path,
):
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    fig, ax = plt.subplots(figsize=(10, 8))

    # -----------------------------
    # Plot characters
    # -----------------------------
    for _, row in character_coords.iterrows():

        x = row["ideology_axis_1"]
        y = row["ideology_axis_2"]

        ax.scatter(x, y, s=80, color="black")

        ax.text(
            x + 0.02,
            y + 0.02,
            row["character"],
            fontsize=9,
        )

    # -----------------------------
    # Plot clusters + arrows
    # -----------------------------
    for _, row in archetype_table.iterrows():

        cluster_id = row["audience_cluster"]
        fav_character = row["strongest_affinity_character"]
        rej_character = row["strongest_rejection_character"]

        cluster_row = cluster_coords[
            cluster_coords["audience_cluster"] == cluster_id
        ]

        if cluster_row.empty:
            continue

        cx = cluster_row["PC1"].values[0]
        cy = cluster_row["PC2"].values[0]

        ax.scatter(cx, cy, s=200, marker="X")

        ax.text(cx + 0.05, cy + 0.05, f"C{cluster_id}", weight="bold")

        # -----------------------------
        # Arrow to favorite character (attraction)
        # -----------------------------
        fav_row = character_coords[
            character_coords["character"] == fav_character
        ]

        if not fav_row.empty:

            tx = fav_row["ideology_axis_1"].values[0]
            ty = fav_row["ideology_axis_2"].values[0]

            ax.annotate(
                "",
                xy=(tx, ty),
                xytext=(cx, cy),
                arrowprops=dict(
                    arrowstyle="->",
                    lw=2,
                    color="green",
                    alpha=0.8,
                ),
            )

        # -----------------------------
        # Arrow to rejected character (repulsion)
        # -----------------------------
        rej_row = character_coords[
            character_coords["character"] == rej_character
        ]

        if not rej_row.empty:

            rx = rej_row["ideology_axis_1"].values[0]
            ry = rej_row["ideology_axis_2"].values[0]

            ax.annotate(
                "",
                xy=(rx, ry),
                xytext=(cx, cy),
                arrowprops=dict(
                    arrowstyle="->",
                    lw=2,
                    color="red",
                    linestyle="dashed",
                    alpha=0.8,
                ),
            )

    # -----------------------------
    # Legend
    # -----------------------------
    legend_elements = [
        Line2D([0], [0], color="green", lw=2, label="Strongest Affinity"),
        Line2D([0], [0], color="red", lw=2, linestyle="--", label="Strongest Rejection"),
    ]

    ax.legend(handles=legend_elements, title="Cluster Attraction Field")

    ax.set_xlabel("Ideological Axis 1")
    ax.set_ylabel("Ideological Axis 2")

    ax.set_title("Fandom Ideological Attraction Field")

    ax.grid(alpha=0.3)

    plt.tight_layout()

    plt.savefig(output_path, dpi=300)

    plt.close()


# ==========================================================
# Audience-Conditioned Character Networks
# ==========================================================

def plot_audience_conditioned_character_networks(
    edges_df: pd.DataFrame,
    community_df: pd.DataFrame,
    output_path,
) -> None:

    import matplotlib.pyplot as plt
    import networkx as nx

    clusters = sorted(edges_df["audience_cluster"].unique())
    n_clusters = len(clusters)

    # ------------------------------------------------------
    # Layout setup (small multiples)
    # ------------------------------------------------------

    cols = min(3, n_clusters)
    rows = int(np.ceil(n_clusters / cols))

    fig, axes = plt.subplots(
        rows,
        cols,
        figsize=(5 * cols, 5 * rows),
    )

    # Ensure axes is iterable
    if n_clusters == 1:
        axes = np.array([[axes]])
    axes = axes.flatten()

    # ------------------------------------------------------
    # Plot each cluster network
    # ------------------------------------------------------

    for idx, cluster in enumerate(clusters):

        ax = axes[idx]

        cluster_edges = edges_df[
            edges_df["audience_cluster"] == cluster
        ]

        cluster_communities = community_df[
            community_df["audience_cluster"] == cluster
        ]

        G = nx.Graph()

        # Add edges
        for _, row in cluster_edges.iterrows():
            G.add_edge(
                row["char_1"],
                row["char_2"],
                weight=row["weight"],
            )

        if len(G.nodes) == 0:
            ax.set_title(f"Audience Cluster {cluster} (No edges)")
            ax.axis("off")
            continue

        # --------------------------------------------------
        # Layout (spring layout = readable structure)
        # --------------------------------------------------

        pos = nx.spring_layout(
            G,
            seed=42,
            k=0.8,
        )

        # --------------------------------------------------
        # Node colors by community
        # --------------------------------------------------

        community_map = dict(
            zip(
                cluster_communities["character"],
                cluster_communities["community_id"],
            )
        )

        node_colors = [
            community_map.get(node, -1)
            for node in G.nodes()
        ]

        # --------------------------------------------------
        # Edge styling (positive vs negative)
        # --------------------------------------------------

        weights = np.array([
            G[u][v]["weight"]
            for u, v in G.edges()
        ])

        edge_colors = [
            "green" if w > 0 else "red"
            for w in weights
        ]

        edge_widths = [
            1 + 4 * abs(w)
            for w in weights
        ]

        # --------------------------------------------------
        # Draw network
        # --------------------------------------------------

        nx.draw_networkx_nodes(
            G,
            pos,
            node_size=500,
            node_color=node_colors,
            cmap=plt.cm.tab10,
            ax=ax,
        )

        nx.draw_networkx_edges(
            G,
            pos,
            edge_color=edge_colors,
            width=edge_widths,
            alpha=0.7,
            ax=ax,
        )

        nx.draw_networkx_labels(
            G,
            pos,
            font_size=8,
            ax=ax,
        )

        # --------------------------------------------------
        # Titles & cleanup
        # --------------------------------------------------

        ax.set_title(f"Audience Cluster {cluster}")
        ax.axis("off")

    # ------------------------------------------------------
    # Remove empty subplots
    # ------------------------------------------------------

    for j in range(idx + 1, len(axes)):
        axes[j].axis("off")

    # ------------------------------------------------------
    # Global title
    # ------------------------------------------------------

    fig.suptitle(
        "Audience-Conditioned Character Networks",
        fontsize=14,
    )

    plt.tight_layout()

    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_coalition_ideology_map(
    coalition_df: pd.DataFrame,
    output_path,
) -> None:

    import matplotlib.pyplot as plt

    clusters = sorted(coalition_df["audience_cluster"].unique())

    fig, axes = plt.subplots(
        1,
        len(clusters),
        figsize=(6 * len(clusters), 6),
        sharex=True,
        sharey=True,
    )

    if len(clusters) == 1:
        axes = [axes]

    # -------------------------
    # Color mapping
    # -------------------------
    color_map = {
        "Strong Alliance": "tab:blue",
        "Contested Bloc": "tab:orange",
        "Antagonist Bloc": "tab:red",
    }

    for ax, cluster in zip(axes, clusters):

        df = coalition_df[
            coalition_df["audience_cluster"] == cluster
        ]

        for _, row in df.iterrows():

            size = (row["n_characters"] ** 2) * 80

            color = color_map.get(
                row["coalition_type"],
                "gray"
            )

            ax.scatter(
                row["ideology_axis_1"],
                row["ideology_axis_2"],
                s=size,
                alpha=0.7,
                c=color,
                edgecolor="black",
            )

            # Label with community id
            ax.text(
                row["ideology_axis_1"],
                row["ideology_axis_2"],
                str(row["community_id"]),
                ha="center",
                va="center",
                fontsize=10,
                weight="bold",
            )

        ax.set_title(f"Audience Cluster {cluster}")
        ax.set_xlabel("Ideology Axis 1")
        ax.set_ylabel("Ideology Axis 2")

        ax.axhline(0)
        ax.axvline(0)

    # -------------------------
    # Legend
    # -------------------------
    handles = [
        plt.Line2D(
            [0], [0],
            marker='o',
            color='w',
            label=label,
            markerfacecolor=color,
            markersize=10,
            markeredgecolor="black"
        )
        for label, color in color_map.items()
    ]

    fig.legend(
        handles=handles,
        loc="upper center",
        ncol=3,
    )

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
