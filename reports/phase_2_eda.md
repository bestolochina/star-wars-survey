
---
# Phase 2 — Bivariate Exploratory Analysis

## Phase 2.1: Binary & Binary / Binary & Nominal Relationships

This phase explores relationships between pairs of binary (boolean) variables.
The goal is **descriptive understanding**, validation of survey logic, and identification of meaningful associations — **not** causal inference or hypothesis testing.

All results are presented as **contingency tables with row-wise percentages**, supported by visual heatmaps (generated but not embedded here).

---
## 2.1.1 Seen Star Wars × Star Wars Fandom

**Variables**

* `seen_star_wars`
* `fan_star_wars`

**Key observations**

* Among respondents who have **not** seen Star Wars, **100%** of responses for `fan_star_wars` are missing.
* Among respondents who **have** seen Star Wars:

  * **59%** identify as Star Wars fans
  * **30%** do not identify as fans
  * **11%** did not answer the fandom question

**Interpretation**

This pattern strongly suggests **structural missingness**: the fandom question is only meaningful for respondents who have seen Star Wars.
No logically impossible combinations (e.g. “fan without having seen”) are observed.

**Conclusion**

* Survey logic is internally consistent.
* The cleaned boolean variables behave exactly as expected.

*(See Figure 2.1: Seen Star Wars × Star Wars Fandom heatmap.)*
![seen_star_wars_vs_fan_star_wars_heatmap.png](figures/seen_star_wars_vs_fan_star_wars_heatmap.png)
---

## 2.1.2 Star Wars Fandom × Star Trek Fandom

**Variables**

* `fan_star_wars`
* `fan_star_trek`

**Key observations**

* Among Star Wars fans:

  * **67%** also identify as Star Trek fans
* Among Star Wars non-fans:

  * Only **16%** identify as Star Trek fans
* Respondents with missing Star Wars fandom responses show high disengagement from fandom questions overall.

**Interpretation**

There is a **strong positive association** between Star Wars fandom and Star Trek fandom.
Rather than being mutually exclusive, the two fandoms substantially overlap.

**Conclusion**

* Sci-fi fandoms appear to cluster within the same respondents.
* This finding motivates later demographic stratification (Phase 2.2).

*(See Figure 2.2: Star Wars Fandom × Star Trek Fandom heatmap.)*
![fan_star_wars_vs_fan_star_trek_heatmap.png](figures/fan_star_wars_vs_fan_star_trek_heatmap.png)
---

## 2.1.3 Seen Star Wars × Star Trek Fandom

**Variables**

* `seen_star_wars`
* `fan_star_trek`

**Key observations**

* Among respondents who have seen Star Wars:

  * Approximately **44%** identify as Star Trek fans
* Among respondents who have not seen Star Wars:

  * Only **~5%** identify as Star Trek fans

**Interpretation**

Exposure to Star Wars is strongly associated with identification as a Star Trek fan.
This may reflect broader engagement with science fiction media rather than franchise-specific preferences.

**Conclusion**

* Sci-fi exposure appears to be a shared trait among respondents.
* Further analysis by demographic groups is warranted.

*(See Figure 2.3: Seen Star Wars × Star Trek Fandom heatmap.)*
![seen_star_wars_vs_fan_star_trek_heatmap.png](figures/seen_star_wars_vs_fan_star_trek_heatmap.png)
---

## Binary & Binary Relationships Summary

Across all binary × binary analyses:

* No logical contradictions were detected
* Structural missingness behaves consistently
* Several strong descriptive associations were identified
* Results validate the earlier data cleaning decisions

This confirms that the dataset is **analysis-ready** for more granular bivariate exploration.

---

Perfect — this is **exactly** the right moment to update the Phase 2 report, and your output is *rich but still manageable*. I’ll help you turn this into **clean, analytical text**, not a data dump.

Below is a **ready-to-drop-in update** for `reports/phase_2_eda.md`.

---

## 2.1.4 Star Wars Fandom by Demographics (`fan_star_wars`)

This section explores how **demographic (nominal) variables** relate to two key binary outcomes:

* `fan_star_wars`
* `fan_star_trek`

For each pairing, row-wise percentages are reported, and stacked bar charts are referenced to visualize relative differences across categories.

**Figure 2.2.1a–e** show the proportion of respondents identifying as Star Wars fans across demographic groups.
![gender_fan_star_wars.png](figures/gender_fan_star_wars.png)
#### Gender

Male respondents report a higher likelihood of identifying as Star Wars fans (71.6%) compared to female respondents (59.9%). Respondents with missing gender values show similar fan proportions but are few in number.

#### Education Level

Star Wars fandom is relatively consistent across education levels, ranging from approximately 58% to 67%. Respondents with “Less than High School” education show a 100% fandom rate; however, this category contains very few observations and should not be overinterpreted.

#### Household Income

Fandom rates increase modestly with income. Respondents in the highest income bracket ($150k+) show a higher fan proportion (71.4%) than those in lower income brackets, though differences across income groups are not extreme.

#### Census Region

Regional differences are relatively small. The Pacific region shows the lowest proportion of fans (58.9%), while New England and Mountain regions show higher fandom levels (above 72%). Overall, fandom appears broadly distributed across regions.

#### Age Group

Star Wars fandom peaks among respondents aged 30–44 (72.5%) and declines with age, reaching the lowest level among those aged 60+ (58.5%). This suggests a generational pattern consistent with the original release timeline of the franchise.

---

## 2.1.5 Star Trek Fandom by Demographics (`fan_star_trek`)

**Figure 2.2.2a–e** present the same demographic breakdown for Star Trek fandom, enabling direct comparison with Star Wars.
![gender_fan_star_trek.png](figures/gender_fan_star_trek.png)
#### Gender

Male respondents are substantially more likely to identify as Star Trek fans (47.5%) than female respondents (34.1%). This gender gap is notably larger than for Star Wars fandom.

#### Education Level

Star Trek fandom increases with education level. Respondents with some college or higher education show fandom rates above 40%, compared to lower rates among those with high school education or less.

#### Household Income

Star Trek fandom shows a mild positive association with income. Respondents in higher income brackets report slightly higher fandom rates, though differences remain moderate.

#### Census Region

Regional variation is more pronounced for Star Trek than for Star Wars. The East South Central region shows the highest fandom rate (57.9%), while East North Central and Pacific regions report lower levels (around 35%).

#### Age Group

Star Trek fandom increases with age up to the 45–60 group (49.5%) and then declines slightly among respondents aged 60+. This pattern contrasts with Star Wars fandom, which peaks earlier.

---

### 2.1.6 Comparative Observations

Across all demographic dimensions:

* **Star Wars fandom is more prevalent than Star Trek fandom**
* **Star Wars appeals more strongly to younger and middle-aged respondents**
* **Star Trek fandom skews older, more male, and more educated**
* Gender differences are substantially larger for Star Trek than for Star Wars

These descriptive patterns suggest that the two franchises occupy distinct cultural and demographic niches, despite partial audience overlap.

---

## Phase 2.2 Categorical & Ordinal Relationships


## Phase 2.2.1 — Episode Ranking Distributions (Ordinal Analysis)

**Figure 2.2.1.a** show the distribution of each episode rankings with Mean, Median, and IQR.
![episode_rank_histograms.png](figures/episode_rank_histograms.png)
---

### Key observations

**General**

* Histograms reveal the *full rank distributions* and asymmetries that were partially hidden in boxplots and stacked bars.
* Mean, median, and IQR overlays are consistent with numeric summaries, confirming visual–numeric coherence.

---

**Episode I**

* Rankings are broadly spread, with a noticeable concentration at ranks 4–6.
* Median lies around rank 4, and the wide IQR indicates mixed reception with no strong consensus.

---

**Episode II**

* Strong right skew toward unfavorable rankings (rank 5 dominates).
* Mean and median are both high (worse ranks), reflecting overall negative reception with limited polarization.

---

**Episode III**

* Distribution is concentrated in ranks 4–6, with relatively few top rankings.
* Median and mean are close, indicating consistently low evaluations rather than polarization.

---

**Episode IV**

* Balanced distribution with substantial mass at ranks 1–3.
* IQR is moderate, suggesting generally positive reception with some disagreement among respondents.

---

**Episode V**

* Clear dominance of top rankings (ranks 1–2), visually standing out from all other episodes.
* Median equals rank 2, while the mean is slightly higher (~2.5) due to a small but non-negligible tail of low rankings.
* Narrow IQR confirms strong consensus on high quality.

---

**Episode VI**

* Bimodal tendency: many high rankings (2–3) alongside a visible lower-rank tail.
* Median around rank 3, with a wider spread than Episode V, indicating more divided opinions.

---

### Methodological note

* Histograms provide exact rank frequencies and expose skewness and tail effects that are obscured in summary-only plots.
* Given the inclusion of mean, median, and IQR overlays, histograms subsume the analytical role of both boxplots and stacked bar charts for ordinal comparisons.

---

### Conclusion

* Episode V is the clear consensus favorite.
* Original trilogy episodes (IV–VI) outperform prequels overall but differ in agreement strength.
* Prequel episodes (I–III), especially II and III, show consistently weaker reception rather than polarization.

---

## 2.2.2 Character Rating Distributions

**Figure 2.2.2.a** presents the distribution of ratings for all character variables.
![character\_rating\_distributions.png](figures/character_rating_distributions.png)

Across all character rating variables, **missingness is substantial (≈30–45%)**, indicating that ratings are conditional on respondent familiarity rather than universally held opinions. This reflects a selection effect rather than random nonresponse.

### Core protagonists

**Luke Skywalker**

* Extremely strong ceiling effect, with a dominant concentration at the highest rating.
* Minimal use of low ratings indicates near-universal positive evaluation among raters.

**Han Solo**

* Similar ceiling effect to Luke, though with slightly more mid-scale usage.
* Distribution suggests broad appeal with limited polarization.

**Princess Leia Organa**

* High concentration at top ratings, with marginally greater dispersion than Luke or Han.
* Indicates strong approval with some differentiation among respondents.

**Yoda**

* Pronounced ceiling effect paired with moderate missingness.
* Ratings suggest iconic status rather than narrative-driven evaluation.

**R2-D2**

* One of the strongest ceiling effects across all characters.
* Extremely limited use of lower ratings implies near-consensus approval.

**C-3P0**

* Still positively skewed, but with noticeably greater mid-scale usage than R2-D2.
* Suggests appreciation tempered by irritation or comedic divisiveness.

---

### Prequel-era and supporting protagonists

**Anakin Skywalker**

* Broad distribution across the full scale.
* Indicates mixed reception, likely reflecting differences between trilogy portrayals.

**Obi-Wan Kenobi**

* Strongly positive skew with less extreme ceiling effects than Luke or Yoda.
* Distribution suggests widespread approval with some evaluative nuance.

**Padmé Amidala**

* Moderate ceiling effect combined with higher missingness.
* Indicates approval among familiar respondents but weaker cultural salience.

**Lando Calrissian**

* Positive skew with visible mid-scale mass.
* Suggests general likability without iconic consensus.

---

### Antagonists and controversial characters

**Darth Vader**

* Broad distribution with substantial mass at both high and mid-scale values.
* Reflects polarized interpretation between admiration and moral negativity.

**Emperor Palpatine**

* Heavily mid- to low-skewed distribution.
* Ratings appear to encode narrative role rather than personal likability.

**Boba Fett**

* Wide dispersion despite limited screen presence.
* Indicates cult popularity alongside indifference among other respondents.

**Jar Jar Binks**

* Strong left skew with dominant low ratings.
* Represents the clearest case of negative consensus in the dataset.

---

### Methodological note

Character ratings exhibit **non-uniform scale usage**, strong **ceiling effects**, and **conditional missingness**. In this context, numeric summaries (mean, median, IQR) would mask polarization and selection effects rather than clarify them. Distributional inspection therefore provides the most faithful descriptive representation.

Overall, these patterns indicate that character ratings capture a mixture of **likability**, **cultural symbolism**, and **narrative role**, which must be considered explicitly in any later comparative or demographic analysis.

---

> These distributional patterns motivate Phase 2.3, where episode rankings and selected character ratings are examined by demographic group, with particular attention to ceiling effects, polarization, and conditional missingness when interpreting group-level differences.


---

## Phase 2.3 — Episode Rankings and Character ratings by Demographic Group

---

# 2.3.1 Episode Ranking Distributions by Gender

**Figure 2.3.1.a** presents episode ranking distributions separately for male and female respondents. Rankings are shown as histograms with overlaid median (solid line), mean (dashed line), and interquartile range (shaded region). Percentages are computed within each episode × gender group.

![episode\_ranking\_gender.png](figures/episode_ranking_gender.png)

### Overall structure

Across both genders, the broad ranking hierarchy remains consistent:

* **Episode V** (The Empire Strikes Back) is the dominant entry, with approximately one-third of respondents in both groups assigning it rank 1. Dispersion is low, and the median lies firmly at the top of the scale.
* **Episode II** is consistently among the lowest-ranked films, with large mass at ranks 5 and 6 across both genders.
* The original trilogy (Episodes IV–VI) generally occupies higher ranking positions than the prequel trilogy (Episodes I–III), regardless of gender.

Thus, episode-to-episode variation is substantially larger than gender-based variation.

---

### Episode V: Strong consensus across genders

* Males: 35.9% rank it 1; 63.1% rank it within the top two.
* Females: 33.0% rank it 1; 62.0% rank it within the top two.
* Median is 1 for both groups; IQR tightly concentrated near ranks 1–2.

Gender differences here are minimal, suggesting near-universal cross-gender approval.

---

### Episodes I–III: Modest gender shifts

The prequel trilogy shows slightly more gender differentiation:

**Episode I**

* Females are somewhat less likely to assign the lowest rank (rank 6) compared to males (13.1% vs 26.7%).
* Female distribution is more concentrated in mid-to-lower ranks (3–4).

**Episode II**

* Both groups rank it poorly overall.
* Males show heavier mass at rank 5 (38.3%), while females distribute more evenly across ranks 3–5.

**Episode III**

* Females assign rank 6 slightly more frequently than males (27.7% vs 24.4%).
* Dispersion is similar across groups, with medians around the lower-middle of the ranking scale.

Overall, gender differences for the prequels are present but modest in magnitude relative to the general preference ordering.

---

### Episode IV: Slight polarization among females

* Males: 26.5% assign rank 1.
* Females: 22.7% assign rank 1, but 23.4% assign rank 6.

Female respondents display a somewhat broader distribution, with both high and low extreme rankings more visible. This suggests greater heterogeneity in evaluation rather than a clear directional shift.

---

### Episode VI: Divergence at the extremes

* Males cluster around mid-to-high ranks (2–3), with relatively low mass at rank 6 (13.7%).
* Females show a more bimodal structure, with noticeable mass at both rank 1 (19.4%) and rank 6 (20.7%).

This indicates that Episode VI may generate more polarized reactions among female respondents than male respondents.

---

### Interpretation

Gender differences in episode rankings exist but are secondary to the dominant global preference structure. The hierarchy of episodes—particularly the strong preference for Episode V and the relative weakness of Episode II—remains stable across groups.

Where differences emerge, they primarily reflect **dispersion and polarization effects** rather than complete reversals of ranking order. These patterns suggest that gender influences the intensity and spread of evaluations more than the fundamental ordering of the films.

---

# 2.3.2 Episode Ranking Distributions by Age Group

**Figure 2.3.2.a** shows episode ranking distributions across four age groups: 18–29, 30–44, 45–60, and 60+. As in the previous section, rankings are shown as histograms with mean, median, and interquartile range overlays. Percentages are computed within each episode × age group.

![episode\_ranking\_age\_group.png](figures/episode_ranking_age_group.png)

---

## 1. A Stable Anchor: Episode V Across Generations

Episode V remains the top-ranked film in every age group:

* Rank 1 share:

  * 18–29: 31.1%
  * 30–44: 37.7%
  * 45–60: 37.1%
  * 60+: 31.1%
* Combined top-two share exceeds 57% in all groups and reaches over 70% in ages 30–44.

This indicates strong intergenerational consensus. While intensity varies slightly (strongest among 30–60), Episode V functions as a cross-cohort anchor in the franchise.

---

## 2. Prequel Trilogy: Clear Generational Gradient

The most pronounced age effect appears in Episodes I–III.

### Episode I

Rank 1 share:

* 18–29: 11.7%
* 30–44: 7.2%
* 45–60: 14.2%
* 60+: 27.6%

Surprisingly, the 60+ group assigns rank 1 far more often than younger groups. At the same time, the 30–44 group shows the strongest negative skew (34.3% rank 6).

This produces a non-monotonic pattern rather than a simple “younger like prequels more” story.

---

### Episode II

Consistently weak across all age groups, but especially among 30–44:

* 30–44: 44.4% assign rank 5.
* 45–60: 35.8% assign rank 5.
* 18–29: more dispersed across 4–6.
* 60+: slightly less concentrated at rank 5 than middle-aged groups.

Episode II is broadly disfavored, but strongest rejection appears among middle cohorts.

---

### Episode III

Displays a clearer generational divide:

* 18–29: relatively balanced, with meaningful mass in ranks 1–4.
* 30–44 and 45–60: heavy concentration in ranks 5–6 (~53% combined for both groups).
* 60+: split between mid and low ranks, but 24.9% assign rank 6.

Younger respondents (18–29) are noticeably more favorable toward Episode III compared to middle-aged groups.

---

## 3. Original Trilogy: Generational Reordering

### Episode IV

Rank 1 share:

* 18–29: 21.1%
* 30–44: 27.1%
* 45–60: 29.2%
* 60+: 19.7%

Middle cohorts (30–60) show strongest preference for Episode IV.
The 60+ group exhibits more dispersion, with 25.9% assigning rank 6 — indicating polarization rather than uniform reverence.

---

### Episode VI

Clear generational split:

* 30–44: heavily concentrated at ranks 2–3 (57% combined).
* 45–60: strong concentration at rank 2 (34.6%).
* 60+: 25.9% assign rank 6 (highest among groups).
* 18–29: broader distribution, including 16.7% at rank 6.

Episode VI shows increasing dispersion at the youngest and oldest ends of the spectrum.

---

## 4. Cohort Patterns

Three structural patterns emerge:

### (1) Middle-Aged Cohort Consolidation (30–44)

* Strongest endorsement of Episode V.
* Strongest rejection of Episode II.
* Generally tight distributions.
* Reflects high internal consensus.

### (2) Younger Cohort Moderation (18–29)

* More balanced distributions across ranks.
* Less extreme rejection of prequels.
* Greater tolerance across trilogy boundaries.

### (3) Oldest Cohort Polarization (60+)

* Higher rank 1 share for Episode I.
* High rank 6 shares for Episodes IV and VI.
* Wider dispersion across multiple films.

This suggests the 60+ group exhibits less uniform adherence to the dominant franchise hierarchy.

---

## 5. Interpretation

Unlike gender, age introduces **meaningful structural variation** in episode evaluations.

Key effects include:

* Generational differences in prequel reception.
* Strong middle-cohort consolidation around Episode V.
* Increased dispersion and polarization at the oldest age bracket.

However, the fundamental hierarchy—Episode V at the top and Episode II near the bottom—remains intact across all age groups.

Age therefore modifies intensity and dispersion more strongly than it overturns the global ordering.

---

Good. Income looks structurally weaker than age — which is interesting in itself.

Here is a **draft of Section 2.3.3 (Household Income)** consistent with your prior sections.

---

# 2.3.3 Episode Ranking Distributions by Household Income

**Figure 2.3.3.a** presents episode ranking distributions across five household income brackets:
$0–24k, $25–49k, $50–99k, $100–149k, and $150k+.

Percentages are computed within each episode × income group.

![episode\_ranking\_income.png](figures/episode_ranking_household_income.png)

---

## 1. Structural Stability Across Income

The most immediate observation is structural consistency:

* **Episode V** remains the dominant entry in every income bracket.
* **Episode II** consistently concentrates mass in ranks 5–6.
* The original trilogy generally outperforms the prequel trilogy in all income groups.

Unlike age, income does not meaningfully reorder the global hierarchy of episodes.

---

## 2. Episode V: Uniform Cross-Income Dominance

Rank 1 share by income:

* $0–24k: 36.7%
* $25–49k: 39.5%
* $50–99k: 32.4%
* $100–149k: 35.7%
* $150k+: 39.0%

Top-two shares exceed 60% in all brackets.

There is no clear monotonic relationship between income and preference strength. The dominance of Episode V appears income-invariant.

---

## 3. Episode II: Consistent Rejection, Slight Middle-Upper Concentration

Episode II is weakest across brackets, with especially strong rank-5 concentration in middle-to-upper income groups:

* $50–99k: 42.4% assign rank 5.
* $100–149k: 38.3% assign rank 5.
* $150k+: 32.5% assign rank 5 and 22.1% rank 6.

Lower-income groups show slightly more dispersion across ranks 2–6.

The pattern suggests modest intensification of rejection in middle-income cohorts but no reversal of ordering.

---

## 4. Prequel Trilogy: Mild Dispersion Differences

### Episode I

Rank 1 share ranges from 11.7% to 17.7% across brackets — relatively narrow variation.

The $50–99k and $100–149k groups show higher mass at rank 4 (30%+), suggesting middle-tier positioning rather than extreme rejection.

No clear income gradient emerges.

---

### Episode III

Upper-income groups ($100k+) show heavier mass at ranks 5–6 (approx. 55–57% combined), suggesting somewhat stronger negative positioning.

Lower-income groups distribute more evenly across mid ranks (3–4).

Still, magnitude differences remain moderate.

---

## 5. Episode IV and VI: Minor Polarization in Upper Brackets

### Episode IV

* Rank 1 share increases in higher brackets (31.2% for $150k+).
* However, $100–149k shows notable polarization, with 28.7% assigning rank 6.

This indicates dispersion rather than uniform preference shift.

---

### Episode VI

Higher-income groups show strong clustering around ranks 2–3:

* $150k+: 39.0% assign rank 3.
* $100–149k: 35.7% assign rank 3.

Lower-income groups display slightly broader dispersion, including higher rank-6 shares.

---

## 6. Comparative Interpretation

Relative to gender and especially age:

* Income effects are present but comparatively weak.
* There is no systematic monotonic gradient (e.g., “higher income → stronger original trilogy preference”).
* Variation primarily manifests in dispersion and intensity rather than reordering.

In terms of segmentation strength:

> Age > Gender ≈ Income (tentative, pending education and region).

We will formally evaluate this ordering in Section 2.3.6 once all demographic slices are complete.

---

# 2.3.4 Episode Ranking Distributions by Education Level

**Figure 2.3.4.a** presents episode ranking distributions across education levels:

* Less than High School
* High School
* Some College / Associate
* Bachelor’s
* Graduate

Percentages are computed within each episode × education group.

*Note:* The “Less than HS” category contains only **n = 3** respondents. It is displayed for completeness but excluded from substantive interpretation due to insufficient sample size.

![episode_ranking_education_level.png](figures/episode_ranking_education_level.png)

---

## 1. Structural Stability Across Education Levels

Excluding the “Less than HS” group (n=3), the overall episode hierarchy remains stable:

* **Episode V** is the dominant entry across all education levels.
* **Episode IV** consistently ranks near the top.
* **Episode II** clusters toward ranks 5–6.
* The original trilogy outperforms the prequel trilogy in every education category.

Unlike age, education does not reorder the global ranking structure.

---

## 2. Episode V: Slight Strengthening with Higher Education

Rank 1 share by education:

* High School: 25.4%
* Some College: 33.9%
* Bachelor’s: 37.8%
* Graduate: 34.1%

Top-two concentration increases modestly among Bachelor’s and Graduate respondents.

The effect appears incremental rather than structural: Episode V is widely preferred across all education levels.

---

## 3. Episode II: Rejection More Concentrated Among Higher Education

Rank 5 share:

* High School: 29.6%
* Some College: 28.7%
* Bachelor’s: 42.4%
* Graduate: 38.5%

Higher-education respondents exhibit stronger clustering at rank 5.

Rank 6 also increases modestly among Bachelor’s and Graduate groups.

This suggests somewhat sharper negative positioning among more educated cohorts.

---

## 4. Episode III: Mild Downward Shift with Higher Education

Rank 6 share:

* High School: 18.3%
* Some College: 20.5%
* Bachelor’s: 31.4%
* Graduate: 28.3%

Bachelor’s and Graduate groups show heavier lower-rank concentration relative to High School respondents.

However, the episode does not become dominant in any group, nor does it radically shift in ordering.

---

## 5. Episode IV and VI: Broad Cross-Education Appeal

### Episode IV

Rank 1 share:

* High School: 22.5%
* Some College: 17.3%
* Bachelor’s: 29.0%
* Graduate: 28.8%

Upper education groups show somewhat stronger top-ranking concentration, but mid-rank dispersion remains present.

---

### Episode VI

Displays consistent clustering around ranks 2–3 across all education levels.

No strong education-based polarization is observed.

---

## 6. Comparative Interpretation

Relative to previously examined demographics:

* Education produces visible but moderate shifts in intensity.
* There is no major reordering of episode hierarchy.
* Effects resemble those observed for income.

Tentative segmentation strength ranking so far:

> Age > Gender > (Income ≈ Education)

We will formalize this comparison in Section 2.3.6 after completing the regional slice.

---

# 2.3.5 Episode Ranking Distributions by Census Region

**Figure 2.3.5.a** presents episode ranking distributions across U.S. census regions:

* East North Central
* West North Central
* Middle Atlantic
* South Atlantic
* East South Central
* West South Central
* Mountain
* Pacific
* New England

Percentages are computed within each episode × region group.

![episode\_ranking\_region.png](figures/episode_ranking_census_region.png)

---

## 1. Strong Structural Stability Across Regions

Across all nine regions, the overall hierarchy remains remarkably consistent:

* **Episode V** dominates rank 1 everywhere.
* **Episode IV** is consistently among the strongest entries.
* **Episode II** clusters at ranks 5–6 in all regions.
* The original trilogy outperforms the prequel trilogy across the country.

No region reverses the global episode ordering.

Relative to age, regional variation is modest.

---

## 2. Episode V: Nationwide Dominance

Rank 1 share by region:

* Ranges from **26.5% (Mountain)** to **39.8% (South Atlantic)**.
* Most regions cluster between 30–38%.

Top-two concentration exceeds ~55–65% in nearly all regions.

There is no clear geographic gradient (e.g., coastal vs inland, north vs south). Episode V’s appeal appears geographically invariant.

---

## 3. Episode II: Uniformly Weak Across Regions

Rank 5 share:

* Typically between 32–44%.
* Particularly high in Mountain (44.1%) and East South Central (53.1%).

Rank 6 share also remains substantial across regions.

The rejection pattern is consistent nationwide, with only intensity differences.

---

## 4. Episode III: Moderate Regional Dispersion

Rank 6 share:

* Higher in Mountain (30.9%) and East South Central (34.4%).
* Lower in Pacific (23.3%) and Middle Atlantic (26.1%).

While some southern and mountain regions show stronger lower-rank concentration, differences remain incremental rather than structural.

---

## 5. Episode IV: Broad Regional Appeal with Mild Polarization

Rank 1 share:

* Peaks in East South Central (34.4%).
* Also strong in Pacific (28.1%) and Middle Atlantic (29.0%).

However, some regions show heavier lower-rank mass (e.g., West South Central rank 6 = 28.9%).

This indicates mild dispersion but not geographic reordering.

---

## 6. Episode VI: Consistent Mid-Upper Placement

Across regions:

* Strong clustering at ranks 2–3.
* Particularly high rank-3 concentration in East South Central (43.8%).

No region exhibits extreme polarization relative to others.

---

## 7. Comparative Interpretation

Relative to other demographic variables:

* Regional variation is present but limited.
* No systematic geographic gradient emerges.
* Episode hierarchy remains stable nationwide.

Tentative segmentation strength ordering now appears:

> Age > Gender > (Income ≈ Education ≈ Region)

Regional identity appears less predictive of ranking behavior than generational cohort.

---



