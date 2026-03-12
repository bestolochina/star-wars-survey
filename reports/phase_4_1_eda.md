
# Phase 4 — Audience Segmentation and Narrative Identity

### A Structural Analysis of Character Preference in the Star Wars Fandom

---

# 1. Introduction

Earlier phases of the analysis established:

1. **Phase 1 — Distribution analysis**
   Character ratings across the entire survey population.

2. **Phase 2 — Demographic divergence**
   Demographic variables explain **very little variance** in preferences.

3. **Phase 3 — Character archetype structure**
   Characters cluster into **three narrative archetype groups**.

The goal of **Phase 4** is to determine whether **latent audience segments** exist that structure how audiences evaluate characters.

Rather than segmenting by demographics, we segment by **behavioral preference patterns**.

The key research questions are:

* Do distinct **audience clusters** exist?
* How strongly do clusters diverge in their character preferences?
* What **narrative identities** do these clusters represent?

---

# 2. Narrative Archetype Structure of Characters

Phase 3 clustering grouped the 14 characters into **three narrative archetypes**.

## Table 1 — Character archetype clusters

| Archetype                      | Characters                                                  |
| ------------------------------ | ----------------------------------------------------------- |
| **C1 – Power & Villainy**      | Darth Vader, Emperor Palpatine, Boba Fett, Lando Calrissian |
| **C2 – Heroic Core**           | Luke, Leia, Han Solo, Obi-Wan, Yoda, R2-D2, C-3PO           |
| **C3 – Prequel Emotional Arc** | Anakin, Padme, Jar-Jar                                      |

These clusters capture **narrative roles**:

### C1 — Power/Villainy Archetype

Characters associated with power, authority, or morally ambiguous roles.

### C2 — Heroic Core Archetype

The moral center of the original trilogy.

### C3 — Prequel Narrative Arc

Characters strongly associated with the prequel era.

---

# 3. Audience Clustering

Audience segmentation was performed using **character rating vectors**.

The model identifies **three distinct audience clusters**.

---

# 4. Character Rating Profiles by Audience Cluster

## Table 2 — Mean character ratings per audience cluster

| Character   | Cluster 1 | Cluster 2 | Cluster 3 |
| ----------- | --------- | --------- | --------- |
| Anakin      | 4.01      | 3.54      | 3.81      |
| Boba Fett   | 3.56      | 3.65      | 2.53      |
| C-3PO       | 4.11      | 4.44      | 4.76      |
| Darth Vader | 3.95      | 4.29      | **1.71**  |
| Palpatine   | 3.60      | 3.19      | 2.08      |
| Han Solo    | 4.32      | **4.93**  | 4.77      |
| Jar-Jar     | **3.50**  | **1.89**  | 3.15      |
| Luke        | 4.29      | 4.74      | 4.74      |
| Obi-Wan     | 4.27      | 4.84      | 4.83      |
| Leia        | 4.23      | 4.73      | 4.73      |
| R2-D2       | 4.34      | 4.60      | 4.83      |
| Yoda        | 4.46      | 4.62      | **4.87**  |

Key observations:

1. **Cluster 2** gives the **highest ratings to heroic characters**.
2. **Cluster 3 strongly dislikes villain archetypes**.
3. **Cluster 1 displays the most balanced ratings**.

---

# 5. Extremeness of Audience Clusters

To measure polarization we compute an **extremeness score**.

## Table 3 — Cluster extremeness

| Cluster   | Extremeness |
| --------- | ----------- |
| Cluster 3 | **0.391**   |
| Cluster 1 | 0.339       |
| Cluster 2 | 0.307       |

Interpretation:

* **Cluster 3** is the most **ideologically extreme** group.
* **Cluster 2** is the most **normative / mainstream fan group**.

---

# 6. Character Deviations (Key Evidence)

Cluster behavior becomes clearer when we examine **deviations from global character means**.

## Table 4 — Largest positive/negative deviations

| Character   | Cluster   | Deviation |
| ----------- | --------- | --------- |
| Darth Vader | Cluster 2 | **+0.97** |
| Jar-Jar     | Cluster 2 | **−0.96** |
| Darth Vader | Cluster 3 | **−1.61** |
| Palpatine   | Cluster 3 | −0.88     |
| Boba Fett   | Cluster 3 | −0.72     |
| Jar-Jar     | Cluster 1 | +0.65     |

These deviations reveal **dramatic differences in interpretation of certain characters**.

---

# 7. The Most Surprising Result

### Darth Vader is the strongest polarization axis in the entire dataset.

Cluster 3 rates Vader:

**1.71 / 5**

Global mean:

**3.32**

Deviation:

**−1.61**

This is the **largest deviation observed in the entire analysis**.

Interpretation:

Cluster 3 appears to **morally reject villain archetypes**, even when those villains are iconic.

This result is extremely surprising because:

* Darth Vader is one of the **most popular characters in cinema history**
* Yet a **large segment of the audience strongly dislikes him**

This suggests the fandom is divided between:

1. **Mythic villain appreciation**
2. **Moral narrative rejection**

---

# 8. Archetype-Level Audience Preferences

We now aggregate characters into their archetypes.

## Table 5 — Archetype ratings by audience cluster

| Cluster   | Villain (C1) | Hero (C2) | Prequel (C3) |
| --------- | ------------ | --------- | ------------ |
| Cluster 1 | 3.70         | 4.29      | 3.78         |
| Cluster 2 | 3.72         | **4.70**  | **2.86**     |
| Cluster 3 | **2.40**     | **4.79**  | 3.70         |

Interpretation:

### Cluster 1 — Balanced audience

Moderate appreciation across all archetypes.

### Cluster 2 — Classic trilogy loyalists

Strong preference for heroic characters, strong rejection of prequel characters.

### Cluster 3 — Moral purists

Extremely negative toward villain archetypes.

---

# 9. Statistical Significance of Archetype Preferences

Bootstrap tests confirm all block deviations are **statistically significant**.

Example:

| Cluster     | Archetype | Deviation      | CI |
| ----------- | --------- | -------------- | -- |
| C1 Cluster1 | +0.43     | [0.34, 0.51]   |    |
| C3 Cluster2 | −0.58     | [−0.66, −0.50] |    |
| C1 Cluster3 | −0.88     | [−0.95, −0.81] |    |

Thus these patterns are **not sampling noise**.

---

# 10. Structural Tension in the Narrative

We compute **variance across clusters for each archetype**.

## Table 6 — Archetype tension

| Archetype    | Variance | Interpretation           |
| ------------ | -------- | ------------------------ |
| Villain (C1) | **0.58** | Highest polarization     |
| Prequel (C3) | 0.26     | Moderate conflict        |
| Heroic (C2)  | 0.07     | Near universal agreement |

Key insight:

The fandom **agrees on heroes**, but **fights over villains**.

---

# 11. Narrative Identity Typology

Clusters correspond to **distinct narrative identities**.

## Table 7 — Identity types

| Cluster | Identity Type    | Description                   |
| ------- | ---------------- | ----------------------------- |
| 1       | Broad Mainstream | Balanced narrative engagement |
| 2       | Cult Archetype   | Strong selective preferences  |
| 3       | Cult Archetype   | Highly polarized moral stance |

---

# 12. Structural Interpretation

### Cluster 1 — The Mainstream Audience

Characteristics:

* Balanced preferences
* Moderate engagement
* Accepts most characters

This cluster represents the **largest general audience**.

---

### Cluster 2 — The Classic Trilogy Fan

Traits:

* Strong preference for heroic characters
* Strong rejection of prequel archetypes

This audience likely formed its identity around the **original trilogy narrative structure**.

---

### Cluster 3 — The Moral Purist

Traits:

* Strong rejection of villain characters
* Very high admiration for heroes

This group treats the narrative **as a moral drama**, not a mythic saga.

---

# 13. Key Structural Insight

The **core axis of fandom conflict** is not:

* demographics
* age
* education

Instead it is:

### **narrative moral interpretation**

Fans disagree about whether villain characters should be:

* admired as mythic figures
* condemned as immoral figures

---

# 14. Conclusion

The Star Wars audience contains **three distinct narrative identities**:

1. **Mainstream viewers** with balanced preferences
2. **Classic-trilogy loyalists** who reject prequel narratives
3. **Moral purists** who reject villain archetypes

The most surprising discovery is the **extreme rejection of Darth Vader by one audience segment**, revealing a fundamental divide in how audiences interpret villain characters.

The results suggest that fandom divisions emerge not from demographics but from **competing interpretations of the narrative's moral structure**.

---
