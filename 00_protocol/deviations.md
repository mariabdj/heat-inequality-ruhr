# Deviations from the preregistration

Every change to the registered plan is written here, with the date, what changed, why, and whether the result of the changed analysis had been seen.

## D1. 2026-11-02: population column name (Step 2)
- **Registered text (Q5):** population value column `Bevoelkerungszahl`, as written in the official description file `datensatzbeschreibung_bevoelkerungszahlen.xlsx` (Version 2, 30.09.2024).
- **What the data file contains:** the header of `Zensus2022_Bevoelkerungszahl_100m-Gitter.csv` is `GITTER_ID_100m;x_mp_100m;y_mp_100m;Einwohner`. The value column is called `Einwohner` (inhabitants), and there is no flag column.
- **Change:** we use `Einwohner` as the population value. Same variable (number of inhabitants per cell), only the name differs between the description file and the data file.
- **Result seen before the change?** No. Only the header was read; the change does not depend on any value.
- **Effect on the analysis:** none.

## D2. 2026-11-02: census dashes read as zero (Step 3, recorded at Step 7)
- **Registered text:** the preregistration says how bracketed values are handled (Q14: missing in the primary analysis, included in S1) but does not say how a dash ("–") is read.
- **What the description files say:** a dash means "exactly zero, or changed to zero" by the confidentiality procedure.
- **Rule applied:** a dash is stored as the value 0 with a dash flag (rule written in the workflow guide, Step 3, before any data were read). It was applied at Step 3, before any LST value existed, so the choice did not depend on any heat result.
- **Why it matters:** for the foreign share, 55.8% of the usable cells passing rule 3 are 0; for under 18, 27.8%; for 65+, 12.9%. Some of these zeros are small true values changed to zero, which we cannot tell apart.
- **Planned addition (exploratory, not preregistered):** at Step 8, Model A is refitted with dashes treated as missing. It is labelled exploratory. It was decided at Gate 7, after the Step 7 descriptive tables had been seen, and before any model was fitted.
- **Effect on the primary analysis:** none (the registered handling is unchanged; this entry makes it explicit).

## D3. 2026-11-02: wording of the primary estimand (Step 6, recorded at Step 7)
- **Registered text:** the summary sentence of the primary estimand says "among cells with a non-bracketed rent value (Model A, Q19)", while Q13 rule 5 says "non-missing, non-bracketed values for the variables of the model".
- **Clarification:** Model A contains rent and the three shares, so by rule 5 its sample is the cells where all four social variables are present and not bracketed (12,609 cells; the number did not change when Steps 4 to 6 were rerun after the city-mask fix). The summary sentence named only rent; rule 5 is the operative rule and is the one applied.
- **Result seen before the clarification?** No model has been fitted. Sample sizes and descriptive tables had been seen.
- **Effect:** none on the method; the wording of the estimand in the paper will say "all four variables usable". S2 (Q14) already covers the cells without a rent value.

## D4. 2026-11-02: tie rule for the city-specific deciles (Step 7)
- **Registered text (Q19, Descriptive):** "population-weighted mean LST anomaly by city-specific decile of each social variable". No rule for ties.
- **Problem found at Gate 7 (expert panel round 1):** the first implementation ranked cells within each city and broke ties by cell ID. Because many cells have the same value (above all the value 0: 55.8% of usable cells for the foreign share), cells with the same value fell into different deciles depending only on their ID.
- **Clarified rule:** cells with the value 0 form a separate "zero" group; the non-zero values are cut, within each city, into 10 classes with ties sharing the lowest rank (class = ceiling(rank_min / n × 10)), so equal values are always in the same class. Number of cells, population and median population are reported per class.
- **Result seen before the change?** Yes: the first decile table had been produced. The change was made because the ID rule is arbitrary, not because of the pattern of the results. Both versions are kept (`05_analysis/discarded/`, see VERIFICATION_LOG.md).
- **Effect:** descriptive tables and the decile figure only; no hypothesis test uses deciles.

## D5. 2026-11-02: sample of the descriptive analyses (Step 7)
- **Registered text (Q19, Descriptive):** the deciles, Moran's I and LISA are listed, but the sample they use is not stated.
- **Choice:** each social variable uses its own usable cells (cells passing rules 1 to 4 with that variable present and not bracketed); the LST anomaly uses all cells passing rules 1 to 4. This keeps the most cells for each description. Sample sizes are printed in every figure and table (27,452 to 51,409 cells).
- **Result seen before the choice?** The choice was made when Step 7 was first run, before any figure was seen; it is recorded here because the expert panel asked for it to be explicit.
- **Effect:** descriptive results only. Because samples differ by variable, the decile curves of two variables are not computed on the same cells, and LISA maps of census variables have holes where values are missing or uncertain (said in the captions).

## D6. 2026-11-02: definition of "extreme value" for the Q15 count (Step 6)
- **Registered text (Q15):** extreme values are kept and their number is reported; no definition of "extreme" is given.
- **Choice:** a value is counted as extreme if it lies below Q1 − 3 × IQR or above Q3 + 3 × IQR (IQR = Q3 − Q1), computed on the cells passing rules 1 to 4 that have a usable value of that variable (present and, for census variables, not bracketed). Only counted, never removed.
- **Result seen before the choice?** The census distributions (Step 3) had been seen; no relationship with heat had been computed. The first version (Gate 7 round 1 fixes) counted bracketed values too; corrected after round 2 to usable values only. The Step 7 descriptive results had been seen when the rule was corrected at Gate 7; the rule affects reporting only.
- **Effect:** reporting only (`05_analysis/results/step6_extreme_values.csv`).

## D7. 2026-11-02: exploratory LISA with 9,999 permutations (Step 7)
- **Registered text (Q19):** LISA with 999 conditional permutations and FDR 5%. Kept as the primary map.
- **Addition (exploratory, not preregistered):** the same LISA with 9,999 permutations; the number of significant cells and their overlap with the primary map (Jaccard index) are reported in results.json.
- **Why:** with 999 permutations the smallest pseudo p-value is 0.001, close to the FDR thresholds of the census variables, so the exact set of significant cells depends on the random draw (expert panel, Gate 7 round 2).
- **Result seen before the addition?** Yes, the primary LISA maps had been seen. The addition does not replace them.

## D8. 2026-11-02: exploratory group-versus-rest heat comparison (Step 7)
- **Registered text (Q19):** population-weighted mean LST anomaly by city-specific decile. No comparison weighted by group size.
- **Addition (exploratory, not preregistered, descriptive only):** for the foreign, 65+ and under-18 shares, the mean LST anomaly of the estimated group members (weight share / 100 × population) against the rest of the residents (weight (1 − share / 100) × population), over each variable's usable cells, pooled across cities, not adjusted. Bracketed cells are left out and dash cells count as 0 members.
- **Why:** population-weighted deciles describe cells, not the heat the average member of a group lives in; the expert panel (Gate 7 rounds 1 and 2) asked for the group-weighted view, labelled exploratory.
- **Result seen before the addition?** Yes: decided after the decile tables had been seen. It does not replace any registered result and no hypothesis is tested with it.

## D9. 2026-11-05: estimator of S3 (population-weighted models)
- **Registered text (Q24):** "S3: population-weighted models", with the Q19 estimator, fallback and inference rule unless stated otherwise.
- **Problem:** spreg 1.9.1 (the preregistered package) offers no weights for the GMM spatial error estimators (GM_Error_Het, GM_Error_Hom), so the two GM p-values of the inference rule cannot be computed for a weighted model.
- **Change:** S3 is fitted by weighted least squares (weights = cell population), with the OLS block bootstrap of Q19 (1 km blocks by city, B = 999) giving the interval and the p-value. This is a change of estimator (no spatial term), not the Q19 fallback, which covers GM fits that raise an error. To separate the effect of weighting from the change of estimator, an unweighted OLS + bootstrap reference row is reported next to S3.
- **Result seen before the change?** No. Decided and written before S3 was run (the Step 8a primary results had been seen).
- **Effect:** S3 only.

## D10. 2026-11-05: S13 rule for cities with few valid pixels (Step 8c)
- **Registered text (Q24):** "S13: anomaly referenced to the median of each city (computed on the core reference domain)". No rule for a city with few valid pixels in a scene.
- **Rule added:** if a city has fewer than 1,000 valid core reference pixels in a scene, that scene gives no anomaly for that city's pixels. Written before S13 was built; never triggered (0 city-scene pairs).

## D11. 2026-11-05: S18 bootstrap design (Step 8b)
- **Registered text:** S18 with the Q19 inference rule; the bootstrap part is not specified for lagged regressors.
- **Choice:** the lagged columns WX are computed once on the full sample and kept fixed in every bootstrap replicate (resampled blocks are duplicated, so W cannot be rebuilt). Written before S18 was run.

## D12. 2026-11-05: S11 needed water shares not computed at Step 2 (Step 8b)
- **What happened:** Step 2 computed the water share (rule 3) only for cells with at least 10 inhabitants, so a first S11 run (minimum 3) silently gave the primary sample. The same Earth Engine calculation was then applied to the 9,739 cells with 1 to 9 inhabitants (01_data/step8_water_small_cells.py). The first S11 result was seen and is not used; the method of S11 is unchanged.

## D13. 2026-11-05: effects of S7 on the 1 km grid
- **Registered text (Q20):** P10 and P90 from the pooled analysis sample, treated as fixed. Applied to S7 too, with the 100 m values, as written.
- **Note added:** 1 km values are averages, so their spread is smaller than at 100 m; the S7 effects computed with the 100 m P10 to P90 are therefore larger than a 1 km contrast would be. The 1 km P10 to P90 effects are reported next to them as a descriptive figure.

## D14. 2026-11-05: R check of the spatial error model changed after it failed (Step 8a)
- **Registered/decided:** recomputation with sphet 2.1.1, tolerance fixed before the run. It failed (betas up to 6.4 SE apart).
- **Change:** the gate compares spreg with the published two-step procedure written out by hand in R (Arraiz et al. 2010; Drukker et al. 2013), same tolerance; sphet's difference was traced to a different estimator (instrumental variables with the unfiltered X as instruments). Logged as a post-failure change; standard errors and the step-2b lambda are checked too (Gate 8 round 1).

## D15. 2026-11-05: MGWR bandwidth search floor
- **Registered text (Q19):** golden-section search with AICc; the lower search bound is not mentioned.
- **Problem:** mgwr 2.2.1 starts each covariate's search at 42 neighbours by default, so the AICc optimum for the intercept (about 30, found by GWmodel; AICc 741.9 vs 748.2) could not be reached.
- **Change:** the search floor is set to 20 neighbours for every covariate so that the AICc optimum can be reached. The default output (intercept bandwidth 45, AICc 748.2) is kept as a footnote. MGWR is descriptive; no hypothesis depends on it.
- **Result seen before the change?** Yes (the default output and the GWmodel comparison).

## D16. 2026-11-05: exploratory analyses of Q25 (Steps 8b and 8c)
- **Vacancy rate:** moved to Step 8c because it needs a new census file (Leerstandsquote_in_Gitterzellen.zip, registered); exploratory, no hypothesis.
- **ECOSTRESS:** not done; it needs a NASA Earthdata account, which only Maria can create. Recorded as not done.
- **Rent x tree cover:** done in Step 8b, exploratory; the primary (heteroskedastic) p-value is the one reported.
