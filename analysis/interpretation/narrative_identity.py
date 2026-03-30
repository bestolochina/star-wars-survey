# analysis/interpretation/narrative_identity.py

from __future__ import annotations

import pandas as pd


def build_narrative_identity_reports(
    coalition_roles_df: pd.DataFrame,
    audience_typology_df: pd.DataFrame,
) -> pd.DataFrame:

    results = []

    for cluster, df in coalition_roles_df.groupby("audience_cluster"):

        # -------------------------
        # 1. Structure
        # -------------------------
        cluster_type = audience_typology_df.loc[
            audience_typology_df["audience_cluster"] == cluster,
            "cluster_type"
        ].values[0]

        # -------------------------
        # 2. Coalition composition
        # -------------------------
        coalition_types = df["coalition_type"].value_counts().to_dict()

        # -------------------------
        # 3. Ideological roles
        # -------------------------
        roles = df["ideological_role"].value_counts().to_dict()

        # Helper flags
        has_hero = any("Hero" in r for r in roles)
        has_dark = any("Dark" in r for r in roles)
        has_rejected = any("Rejected" in r for r in roles)

        # -------------------------
        # 4. Build narrative text
        # -------------------------
        if cluster_type == "Polarized Narrative":
            if has_rejected:
                description = (
                    "This audience exhibits a polarized narrative structure, "
                    "anchored by a rejected opposing bloc and a dominant heroic core."
                )
            else:
                description = (
                    "This audience exhibits a polarized narrative structure "
                    "with competing ideological blocs."
                )

        elif "Strong Narrative" in cluster_type:
            description = (
                "This audience demonstrates a highly consolidated narrative structure, "
                "with multiple strong and internally cohesive coalitions aligned around a shared core."
            )

        elif "Fragmented" in cluster_type:
            description = (
                "This audience displays a fragmented narrative structure, "
                "with multiple coexisting coalitions and no single dominant interpretation."
            )

        elif cluster_type == "Unified Narrative":
            description = (
                "This audience exhibits a unified narrative structure with a single dominant coalition."
            )

        else:
            description = (
                "This audience shows a layered narrative structure with partially overlapping coalitions."
            )

        # -------------------------
        # 5. Add ideological refinement
        # -------------------------
        if has_hero and not has_dark:
            description += " The narrative space is strongly aligned around a heroic core."

        elif has_hero and has_dark:
            if has_rejected:
                description += " A clear boundary exists between a dominant heroic narrative and a rejected opposing core."
            else:
                description += " The narrative includes both heroic and opposing ideological elements."

        elif has_dark and not has_hero:
            description += " The narrative is centered around darker or controversial elements."

        # -------------------------
        # 6. Save
        # -------------------------
        results.append({
            "audience_cluster": cluster,
            "cluster_type": cluster_type,
            "narrative_identity_report": description,
        })

    narrative_identity = pd.DataFrame(results)
    narrative_identity["audience_cluster"] = narrative_identity["audience_cluster"].astype(int)

    return narrative_identity