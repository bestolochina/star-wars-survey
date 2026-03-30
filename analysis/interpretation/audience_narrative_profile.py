# analysis/interpretation/audience_narrative_profile.py

from __future__ import annotations
import pandas as pd


def interpret_cluster_type(polarization: float, hero_dom: float) -> str:

    if polarization > 2.5 and hero_dom < 3:
        return "Interpretive / Fragmented Audience"

    if polarization < 1 and hero_dom > 4:
        return "Canonical Consensus Audience"

    if polarization > 2.5 and hero_dom > 3:
        return "Ideologically Polarized Audience"

    return "Mixed Narrative Audience"


def build_audience_narrative_profiles(
    narrative_identity: pd.DataFrame,
    narrative_intensity: pd.DataFrame,
    audience_profiles: pd.DataFrame,
) -> pd.DataFrame:

    df = narrative_identity.merge(
        narrative_intensity,
        on="audience_cluster",
        how="left",
    )

    results = []

    for _, row in df.iterrows():

        cluster = row["audience_cluster"]
        identity_text = row["narrative_identity_report"]

        polarization = row["polarization_strength"]
        hero_dom = row["hero_core_dominance"]

        # -------------------------
        # Extract demographics
        # -------------------------
        demo = audience_profiles[
            audience_profiles["audience_cluster"] == cluster
        ]

        top_demos = []

        if not demo.empty:
            for demo_type in demo["demographic"].unique():

                sub = demo[demo["demographic"] == demo_type]

                if sub.empty:
                    continue

                top = sub.sort_values("share", ascending=False).iloc[0]

                cat = top["category"]
                share = top["share"]

                top_demos.append(f"{demo_type}: {cat} ({share:.0%})")

        demo_text = ", ".join(top_demos) if top_demos else "no dominant demographic skew"

        # -------------------------
        # Interpretation logic
        # -------------------------
        label = interpret_cluster_type(polarization, hero_dom)

        article = "an" if label[0].lower() in "aeiou" else "a"

        intensity_label = (
            "high" if polarization > 2 else
            "moderate" if polarization > 1 else
            "low"
        )

        dominance_label = (
            "strong" if hero_dom > 4 else
            "moderate" if hero_dom > 3 else
            "weak"
        )

        profile_text = (
            f"{identity_text} "
            f"This cluster can be characterized as {article} {label}. "
            f"Narrative intensity is {intensity_label} "
            f"(polarization={polarization:.2f}). "
            f"Hero core dominance is {dominance_label} "
            f"(score={hero_dom:.2f}). "
            f"Key demographics: {demo_text}."
        )

        results.append({
            "audience_cluster": cluster,
            "cluster_type": row["cluster_type"],
            "polarization_strength": polarization,
            "hero_core_dominance": hero_dom,
            "audience_profile": profile_text,
        })

    return pd.DataFrame(results)