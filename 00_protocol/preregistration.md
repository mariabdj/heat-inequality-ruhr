# Preregistration: surface heat and social composition on the 100 m census grid of the Ruhr

**Template:** Preregistration for secondary data analysis (van den Akker et al., 2021; OSF template https://osf.io/x4gzt). Questions Q1 to Q25 follow that template. Additions requested by Weston et al. (2019) are in Q17 and Q18.
**Version:** draft 6, 2 November 2026 (after expert review rounds 1 to 5). Status: not yet registered.

---

## Part 1. Study information

**Q1. Working title.**
Are lower-rent neighbourhoods and neighbourhoods with more foreign citizens hotter? Surface heat and social composition on the 100 m census grid of the Ruhr, Germany.

**Q2. Author.**
Maria Boudjelal (MB), independent researcher, Algiers, Algeria. ORCID: https://orcid.org/0009-0002-6434-784X

**Q3. Research questions.**
- **RQ1.** In the 11 independent cities (kreisfreie Städte) of the Ruhr, is summer daytime land surface temperature (LST) higher in 100 m census cells with lower average rent and with a higher share of foreign citizens?
- **RQ2.** Is LST related to the share of residents aged 65 and over, and to the share aged under 18?
- **RQ3.** How much do the associations of RQ1 change when tree cover and sealed (impervious) surfaces of the cell are taken into account?

**Primary estimand.** For each social variable: its within-city association with the LST anomaly (°C per unit), adjusted for the other three social variables, elevation and log population, among cells with a non-bracketed rent value (Model A, Q19). Single-variable models on each variable's own available cells are reported alongside as unadjusted disparities.

**Q4. Hypotheses and statistical framework.**
Framework: frequentist estimation with 95% confidence intervals; two-sided tests at α = .05. Family 1 (H1, H2, RQ2): four tests, Holm correction. Family 2 (H3): two tests, Holm correction. Direction is read from the sign of the estimate.

- **H1 (directional).** Lower average net cold rent per m² goes with higher LST: the rent coefficient in Model A is negative.
  Rationale: Chakraborty et al. (2019) and Hsu et al. (2021) found poorer neighbourhoods hotter in most cities they studied; Chawla, Keller and Benz (2026) found mixed results for rent per resident across German cities at 1 km. We test whether the expected pattern appears at 100 m in the Ruhr.
- **H2 (directional).** A higher share of foreign citizens goes with higher LST: the coefficient is positive.
  Rationale: Chawla et al. (2026) found foreigners disproportionately in hotter areas in more than half of German cities, for both LST and air temperature.
- **RQ2 (no direction predicted).** Shares aged 65+ and under 18. Rationale: Chawla et al. (2026) report older residents slightly cooler; older residents in the Ruhr live both in dense centres and in green outer districts.
- **H3 (directional).** Adding tree cover and imperviousness to Model A moves the rent and foreign-share coefficients toward zero. Measure: Δ* = sign(β_A) × (β_A − β_B) in °C per unit, with sign(β_A) fixed from the full-sample OLS fit (positive = the coefficient moved toward zero). Test: one-sided block-bootstrap p-value (Q19). H3 is supported for a variable if Δ* > 0 and its Holm-adjusted p < .05. If β_B has the opposite sign to β_A and |β_B| > |β_A|, this is reported as "sign reversal", not as attenuation.
  Rationale: greenery is a main surface driver of intra-urban LST (Zhou et al., 2019), and green space is unequally distributed across German neighbourhoods (König, 2024; Klopfer & Pfeiffer, 2023).
  Δ* is a descriptive change in estimate (statistical attenuation). It is not a mediation or causal effect: tree cover and sealing can be causes, consequences or companions of social composition, and all are measured at about the same time.

All hypotheses concern associations between areas. None is a causal claim, and none describes individual people (ecological fallacy).

---

## Part 2. Data description

**Q5. Datasets.**
1. **Zensus 2022 grid data**, Statistische Ämter des Bundes und der Länder (publisher Destatis). Cross-sectional, reference date 15 May 2022, values per 100 m INSPIRE grid cell (EPSG:3035). Files used (exact names from the official description files saved in `00_protocol/census_descriptions/`):

| Variable | 100 m CSV | Value column | Unit | Description version |
|---|---|---|---|---|
| Population | `Zensus2022_Bevoelkerungszahl_100m-Gitter.csv` | `Bevoelkerungszahl` | persons | Version 2, 30.09.2024 |
| Average net cold rent | `Zensus2022_Durchschn_Nettokaltmiete_Anzahl_der_Wohnungen_100m-Gitter.csv` | `durchschnMieteQM` (and `AnzahlWohnungen`) | EUR per m², rented dwellings in residential buildings, no dormitories, rent-free dwellings excluded | Version 2, 08.07.2025 |
| Share of foreign citizens | `Zensus2022_Anteil_Auslaender_100m-Gitter.csv` | `AnteilAuslaender` | % of population | Version 1, 07.10.2024 |
| Share aged 65+ | `Zensus2022_Anteil_ueber_65_100m-Gitter.csv` | `AnteilUeber65` | % of population | Version 1, 07.10.2024 |
| Share aged under 18 | `Zensus2022_Anteil_unter_18_100m-Gitter.csv` | `AnteilUnter18` | % of population | Version 1, 07.10.2024 |

Every file also has a cell ID (`GITTER_ID_100m` in most files, `Gitter_ID_100m` in the rent file: names are matched without regard to case), cell centre coordinates (`x_mp_100m`, `y_mp_100m`) and a flag column `werterlaeuternde_Zeichen` (value `KLAMMERN` = the value is statistically uncertain). We check that every cell ID matches its centre coordinates.

2. **Landsat 8 and 9, Collection 2, Level 2, Tier 1, surface temperature** (USGS), via Google Earth Engine collections `LANDSAT/LC08/C02/T1_L2` and `LANDSAT/LC09/C02/T1_L2`, filtered to `PROCESSING_LEVEL` = L2SP (L2SR products carry no surface temperature). Band `ST_B10`, converted to kelvin as `ST_B10 × 0.00341802 + 149.0` (USGS Landsat 8-9 Collection 2 Level 2 Science Product Guide, Table 6-1), then minus 273.15 for °C. Thermal data are acquired at 100 m and delivered resampled to 30 m. The Ruhr is covered by WRS-2 row 24 of paths 196 and 197; scene centre times are about 10:21 UTC on path 196 and about 10:28 UTC on path 197 (12:21 to 12:28 local summer time), read from `SCENE_CENTER_TIME` of 2022 scenes.
3. **Copernicus Land Monitoring Service** (European Union): High Resolution Layer **Tree Cover Density** 10 m, reference year 2022 if published at download time, otherwise the nearest earlier year (year recorded), and **Imperviousness Density** 10 m, reference year 2021.
4. **Elevation: Geobasis NRW digital terrain model** (bare earth, without buildings or trees), via the official WCS service "WCS NW DGM" (https://www.wcs.nrw.de/geobasis/wcs_nw_dgm), requested at 10 m. A surface model (such as the Copernicus DEM, which includes buildings and canopy) is not used, because it would mix surface information into the elevation control. Licence recorded at download.
5. **ESA WorldCover 10 m v200** (reference year 2021), Earth Engine `ESA/WorldCover/v200`, band `Map`, class 80 "Permanent water bodies", used only to define water.
6. **DWD Climate Data Center**, daily climate data (product "KL"), station Essen-Bredeney (station ID 01303), element `TXK` (daily maximum air temperature), used only to select hot days.
7. **Municipal boundaries**: BKG VG250 (latest edition at download), to assign each cell to one of the 11 cities.

**Q6. Openness.** All datasets are public. Zensus grid data: Datenlizenz Deutschland Namensnennung 2.0. Landsat: public domain (credit USGS). Copernicus: free and open, attribution required; download needs a free CLMS login (Maria has one). Earth Engine needs a registered noncommercial Cloud project (Maria has one). Geobasis NRW, DWD, ESA WorldCover and VG250: open, with the attribution each licence requires.

**Q7. Access.** Zensus: https://www.destatis.de/zensus2022 (grid ZIP files). Landsat and WorldCover: Earth Engine IDs above. Copernicus: https://land.copernicus.eu. Elevation: WCS above. DWD: https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/. Exact URLs, download dates, versions, licences and SHA-256 checksums go into `01_data/data_register.csv` at download.

**Q8. Date of download or access.**
- Census: only the six description files (no data) were downloaded on 2 November 2026. No census value has been downloaded or seen.
- Landsat: on 2 November 2026 one connection test counted scenes over central Bochum (115 summer scenes 2018 to 2025, 28 with less than 20% cloud cover), and the scene centre times, paths and processing level of 2022 scenes over Essen and other Ruhr points were read. No temperature value was computed or seen.
- Earth Engine band names of the Copernicus DEM (no longer used, see Q5 item 4) and WorldCover collections were listed; expert reviewers (review rounds 3 and 4) computed, from scene footprints and fill bits only (no temperatures), that the core reference domain of Q12.4 covers about 95% of the area of the 11 cities; the DWD file list for station 01303 was read (files exist up to 31 December 2025). No values were opened.
All data downloads happen after registration (Steps 2 to 5 of the project).

**Q9. Data collection.** Census: register-based census with a household sample, documented at https://www.destatis.de/zensus2022; grid values are perturbed for confidentiality with the Cell-Key Method. Landsat ST: single-channel algorithm with ASTER GED emissivity and reanalysis atmospheric profiles (USGS guide; Cook et al., 2014). Copernicus layers: produced from satellite imagery (product user manuals saved with the data).

**Q10. Codebooks.** Census description files (sheets "Erläuterungen" and "Erläuterung zu CSV pro 100 m") in `00_protocol/census_descriptions/`. USGS Science Product Guide: `Documentation/02_Remote_Sensing_LST/`. Earth Engine catalogue pages: `Documentation/05_Software_Manuals/Google_Earth_Engine/`.

---

## Part 3. Variables

**Q11. Manipulated variables.** None (observational study).

**Q12. Measured variables.**

*Outcome: summer daytime LST anomaly (°C), per cell.*
1. **Scene** = one Landsat L2SP product (one WRS path, row and date). Used: Landsat 8 and 9 Tier 1 L2SP scenes of path 196 or 197, row 24, acquired 1 June to 31 August, 2018 to 2025.
2. **Hot days:** scenes acquired on days with `TXK` ≥ 25 °C at Essen-Bredeney (DWD's "Sommertag" threshold). A day counts as hot only if `TXK` is present (not the missing-value code) and its quality level is one the DWD KL description file marks as quality-controlled; the quality column name and the accepted codes are read from that description file and written in `01_data/data_register.csv` before the station data are downloaded.
3. **Pixel mask:** a pixel is invalid if `QA_PIXEL` bit 0 (fill), 1 (dilated cloud), 2 (cirrus, high confidence), 3 (cloud, high confidence), 4 (cloud shadow, high confidence) or 5 (snow) is set; or cloud confidence (bits 8 to 9) is medium or high (bit 3 is implied by bits 8 to 9 = high and is listed for clarity); or `ST_B10` = 0 or outside the valid range 293 to 61,440 digital numbers, about 150.0 to 359.0 K after scaling (USGS LSDS-1619, Table 6-1, p. 12); or `ST_CDIST` or `ST_QA` equals the fill value -9999; or `ST_CDIST` × 0.01 < 1 km.
4. **Reference domain:** all 30 m pixels of the native Landsat grid (EPSG:32632, identical for both paths) whose centre lies inside the union of the 11 city polygons and of which less than 50% of the area is ESA WorldCover class 80 (area share computed by exact overlap of the 10 m classes). Path 196 does not cover the west of Duisburg, and scene edges move from date to date, so a **core reference domain** is defined. A **candidate scene** is any scene of item 1 (Landsat 8 or 9 Tier 1 L2SP, path 196 or 197, row 24, 1 June to 31 August 2018 to 2025), whatever its cloud cover or hot-day status; the list is fixed at download and recorded in `01_data/data_register.csv`. A reference-domain pixel belongs to the core if, in every candidate scene, it lies inside the image and `QA_PIXEL` bit 0 is 0; a pixel that is masked or outside the image counts as fill (in Earth Engine: `qa.bitwiseAnd(1).eq(0).unmask(0, False)`, then the minimum over all candidate scenes, always evaluated or exported with `crs='EPSG:32632'` and the `crsTransform` of the candidate scenes' `QA_PIXEL` band, because a collection composite has no native projection). The same core is used in the primary analysis and in every sensitivity analysis (S4, S6, S6b, S12, S13, the Q23 fallback). It is determined before any temperature is converted, and its share of the reference domain is reported overall and per city. A scene is used only if at least 80% of the core reference-domain pixels are valid.
5. **Anomaly:** for each used scene, pixel LST minus the median LST of the valid core reference-domain pixels of that scene (all 11 cities pooled). This removes day-to-day differences in overall temperature, with the same reference area in every scene. Pixels outside the core still receive anomalies. The number of cells per city whose observations come from one path only is reported.
6. **Composite:** per 30 m pixel (native grid, no resampling between scenes), the mean of its anomalies over all used scenes, and its number of valid observations. Pixels with fewer than 5 valid observations are set to missing. The number of used scenes per year, month, path and satellite is reported.
7. **Per cell:** census cell polygons are reprojected (as vectors) to EPSG:32632, so the raster is never resampled; the cell value is the mean of the composite over the cell, weighted by exact pixel overlap (`exactextract`), and the share of the cell covered by non-missing composite pixels is kept.

*Predictors (census, per cell):* `durchschnMieteQM` (EUR/m²), `AnteilAuslaender` (%), `AnteilUeber65` (%), `AnteilUnter18` (%).

*Covariates:*
- Elevation (m): mean of the NRW terrain model over the cell (control: higher ground is slightly cooler, and the Ruhr rises to the south).
- Log population, ln(`Bevoelkerungszahl`): density of residents (control in Models A and B).
- City: 11 levels, entered as 10 dummy variables (fixed effects).
- Tree cover (% of cell): mean of Tree Cover Density over the cell (Model B only).
- Imperviousness (% of cell): mean of Imperviousness Density over the cell (Model B only).

*Time mismatch (limitation, reported):* census 15 May 2022, imperviousness 2021, tree cover 2022 or earlier, LST summers 2018 to 2025.

**Q13. Units of analysis and expected sample size.**
Unit: one 100 m census cell. Study area: the 11 kreisfreie Städte of the Regionalverband Ruhr: Bochum, Bottrop, Dortmund, Duisburg, Essen, Gelsenkirchen, Hagen, Hamm, Herne, Mülheim an der Ruhr, Oberhausen.
Inclusion, applied in this order: (1) cell centre inside one of the 11 cities (VG250); (2) population ≥ 10; (3) less than 50% of the cell area is ESA WorldCover class 80; (4) at least 70% of the cell area covered by non-missing composite pixels (pixels with fewer than 5 valid observations already removed, Q12.6); (5) non-missing, non-bracketed values for the variables of the model.
Expected sample size: tens of thousands of cells. The exact number passing rules 1 to 3 will be counted in Step 2 from the population file and boundaries, before any other census value or any heat value is opened, and recorded in the log. Rules 4 and 5 are counted when the data are joined (Step 6). These counts do not change the analysis plan.

**Q14. Missing data and measurement error.**
Known from the description files: cells without residents or dwellings are absent; some cells may be absent because of confidentiality; values based on very small counts are bracketed. Rent exists only where rented dwellings exist, so cells of owner-occupied single-family housing are missing more often: rent is **not missing at random**.
Handling (primary): complete cases for each model; bracketed values treated as missing. We report, per city, the number of cells lost to each reason. Sensitivity: (S1) bracketed values included; (S2) Model A without the rent term (foreign, 65+ and under-18 shares entered together), fitted on all cells with those three variables.
Cell-Key perturbation adds random noise to predictors in small cells, which tends to pull coefficients toward zero; S11 (other population thresholds) shows how much this matters.

**Q15. Outliers.** No value is removed by judgement. Values leave the analysis only through the masks of Q12 and the inclusion rules of Q13. Extreme values are kept and their number is reported.

**Q16. Weights.** No sampling weights. Primary models are unweighted (each cell counts once). Sensitivity S3: models weighted by cell population (the question per resident rather than per place).

---

## Part 4. Knowledge of the data

**Q17. Earlier work on these data.** Maria Boudjelal has not published or presented anything using these datasets.

**Q18. Prior knowledge.**
- From published research (read during the novelty check, `00_setup/NOVELTY_REPORT.md`): Klopfer and Pfeiffer (2023), 275 Ruhr districts, one 2018 scene: LST to social status link "ambiguous". Chawla, Keller and Benz (2026), all of Germany on a 1 km grid with Zensus 2022: foreigners in hotter areas, older people slightly cooler, rent mixed. Anderson and Hasler (2026), Bochum's 154 districts: we saw their maps of maximum LST and of a heat risk index for Bochum. LANUK Fachbericht 171 (2026): method of the Betroffenheitsanalyse and a text describing low rents around Mülheim-Eppinghofen; we did not open their data.
- This reading may have shaped the directions of H1 and H2 (in particular Chawla et al., 2026, for H2).
- From the data themselves: only the census description files (no values), scene counts and metadata of Landsat (no temperatures), band names of two Earth Engine collections, and the DWD file list.
- Nothing has been seen that links LST to any census variable in our study area at 100 m.

---

## Part 5. Analyses

**Q19. Statistical models.**
y = cell LST anomaly (°C). Units of the predictors: rent per 1 EUR/m², foreign share per 10 percentage points, 65+ share per 10 points, under-18 share per 10 points.

- **Model A:** y = β₀ + β₁·rent + β₂·foreign + β₃·age65 + β₄·under18 + γ₁·elevation + γ₂·ln(population) + 10 city dummies + u.
- **Model B:** Model A + δ₁·tree cover + δ₂·imperviousness (same cells as Model A).
- **Spatial weights W:** queen contiguity on the 100 m grid (cells sharing an edge or a corner), row-standardised, built separately on each model's own analysis sample, crossing city borders. Cells without an included neighbour (islands) are kept with an empty row; the numbers of islands and of connected components are reported. Sensitivity S20: islands dropped.
- **Primary estimator: spatial error model (SEM)**, u = λWu + ε, estimated by GMM with standard errors robust to unequal variances: `spreg.GM_Error_Het(y, X, w=w, hard_bound=True)`, otherwise package defaults, with the city dummies as columns of X (X has no constant column: spreg adds it). Fallback, only if this call raises an error (including |λ| ≥ 0.99: spreg bounds λ to (−0.99, 0.99), and `hard_bound=True` turns a value at the bound into an error): `spreg.GM_Error_Hom(y, X, w=w, hard_bound=True)`; the trigger and message are logged. Maximum-likelihood fits (`ML_Error`, `ML_Lag`) are not used: in spreg 1.9.1 their variance step inverts the n × n matrix (I − λW) as a dense matrix (checked in the source code), which is not feasible at this n. The SEM is chosen in advance because its coefficients keep their direct meaning (°C per unit) while it allows for unmeasured influences shared by neighbouring cells.
- **Inference rule (H1, H2, RQ2):** for each of β₁ to β₄ of Model A, three two-sided p-values are computed: `GM_Error_Het`, `GM_Error_Hom`, and the OLS block bootstrap (95% percentile interval; same replicates as for H3; p = min(1, 2 × min(1 + #{β*_b ≤ 0}, 1 + #{β*_b ≥ 0}) / (B + 1)), B = 999). The largest of the three is the p-value used for Holm (Q22). SEM intervals are β ± 1.96 × SE from spreg (normal approximation). The reported 95% interval, also used in Q20, is the hull of the three intervals (lowest lower bound to highest upper bound). If the three intervals do not all lie on the same side of 0, the result is inconclusive whatever the p-values. `GM_Error_Hom` is always fitted for this rule. If either GM fit fails, the larger of the two remaining p-values and the hull of the two remaining intervals are used, and if `GM_Error_Het` fails, point estimates come from `GM_Error_Hom`; if both GM fits fail, the bootstrap p and interval alone are used; all of this is logged. An OLS coefficient outside the `GM_Error_Het` 95% CI is reported as a sign of misspecification.
- **H1, H2, RQ2:** β₁ to β₄ of Model A (point estimates from `GM_Error_Het`), with the p-values and intervals of the inference rule, Holm-adjusted across the four.
- **H3:** Δ* = sign(β_A) × (β_A − β_B) for rent and for foreign share, computed with OLS versions of Models A and B on the same cells; sign(β_A) is taken from the full-sample OLS fit and kept fixed in every replicate. **Spatial block bootstrap:** a block is the intersection of a 1 km INSPIRE grid cell (EPSG:3035) with one city (the parts of a 1 km cell lying in two cities are separate blocks, each in its own city); each 100 m cell belongs to the block containing its centre; in each city as many blocks are drawn, with replacement, as the city has; B = 999 replicates. One-sided p for Δ* = (1 + #{Δ*_b ≤ 0}) / (B + 1); Holm across the two variables; unadjusted 95% percentile intervals are reported. OLS is used because resampled blocks are duplicated, so W is not defined for a spatial refit; OLS estimates the same β under the SEM. The number of replicates in which β_B has the opposite sign to β_A is reported. R = 100 × Δ*/|β_A| is reported only as a descriptive figure, and only if the OLS block-bootstrap 95% interval of β_A excludes 0; otherwise "not defined". The SEM point value of Δ* is reported next to it. The number of blocks per city and the range of the residual correlogram are reported; the 1 km block size stays primary whatever that range, and S19 (2 km blocks) is the only alternative.
- **Before the SEM:** OLS of each model with Moran's I of residuals and the robust Lagrange multiplier tests (reported, not used to choose the model). If the robust LM-lag test has p < .05 and the robust LM-error test has p ≥ .05, the lag model S8 is discussed with the same weight as the primary model.
- **Single-variable models** (unadjusted disparities): each social variable alone, with elevation, ln(population) and city dummies, same SEM estimator, on that variable's own available cells.
- **Descriptive:** population-weighted mean LST anomaly by city-specific decile of each social variable (in the style of Hsu et al., 2021); Moran's I and LISA maps of y and of each social variable (queen W, 999 conditional permutations, local p-values adjusted with the false discovery rate at 5%; islands have no local statistic and are left out of LISA and of the FDR count). These maps are descriptive.
- **Local, descriptive: MGWR** (`mgwr`) of Model B on the **1 km** grid, because MGWR on tens of thousands of 100 m cells is not computationally feasible. Aggregation (also used for S7): population-weighted means of the census shares, rent weighted by `AnzahlWohnungen`, area means of LST anomaly, tree cover, imperviousness and elevation, ln of the summed population; 1 km cells with fewer than 5 included 100 m cells are dropped. No city dummies (the local intercept replaces them); all variables z-standardised; adaptive bisquare kernel; golden-section search with AICc; bandwidth confidence intervals (`get_bws_intervals`); local t-values corrected for multiple testing (`filter_tvals`); local condition numbers above 30 flagged as local collinearity. n at 1 km is reported.

**Q20. Effect sizes of interest.** For each social variable: effect = β × (P90 − P10), the expected difference in LST anomaly between cells at the 10th and the 90th percentile of that variable. P10 and P90 are taken from the pooled analysis sample and treated as fixed; the CI is the reported interval of Q19 (hull of the three) times the same factor. For rent, the sign is oriented so that a positive value means "hotter where rent is low". We call an association "practically negligible" if the whole 95% CI of this effect lies within ±0.3 °C. This threshold is a judgement, not derived from a model or from the literature: we consider that a difference smaller than 0.3 °C in surface temperature anomaly between cells at the 10th and the 90th percentile would not matter for planning. It is fixed here so that it cannot be chosen after seeing the results.

**Q21. Power and precision.** With tens of thousands of cells, naive standard errors would be very small, but neighbouring cells are not independent, so the effective sample size is much smaller. Uncertainty therefore comes from the spatial model and the block bootstrap (Q19). No formal power analysis is done; all estimates are reported with their intervals whatever their size.

**Q22. Inference criteria.**
- p-values are those of the inference rule of Q19 (largest of three), Holm-adjusted.
- H1 supported: β₁ < 0, Holm-adjusted p < .05, and all intervals of the Q19 inference rule lie below 0. H2 supported: β₂ > 0, Holm-adjusted p < .05, and all intervals lie above 0. Contradicted: opposite sign, Holm-adjusted p < .05, and all intervals on that opposite side of 0. Otherwise: not supported (inconclusive).
- If a result is significant but its whole P10 to P90 CI lies within ±0.3 °C, it is reported as "supported (or contradicted) but practically negligible". If it is inconclusive (not significant, or intervals not all on one side of 0) and the CI lies within ±0.3 °C, it is reported as "practically negligible".
- RQ2: positive, negative or inconclusive by the same rules.
- H3: supported for a variable if Δ* > 0 and its Holm-adjusted one-sided bootstrap p < .05 (Q19). If the full-sample OLS β_B has the opposite sign to β_A and |β_B| > |β_A|, the verdict is "sign reversal" (neither supported nor contradicted), whatever p.
- The ±0.3 °C negligibility rule applies to the P10 to P90 effects of Q20 in every analysis whose outcome is in °C (all except S15, the standardised anomaly). It is not applied to Δ* (H3).
- Tests of H1, H2 and RQ2 are two-sided, with direction from the sign of the estimate; the H3 test is one-sided as defined.

**Q23. Problems and assumption violations.**
- Non-normal or unequal residual variance: handled by the inference rule of Q19 (largest p of `GM_Error_Het`, `GM_Error_Hom` and the block bootstrap).
- Collinearity: variance inflation factors computed for the continuous predictors only (city dummies excluded); if any exceeds 10, models are still fitted as planned and the single-variable models are given the same prominence.
- Too few hot-day observations: the count of valid observations per pixel is computed first, with the full pixel mask of Q12.3 and only in hot-day scenes that pass the 80% rule of Q12.4. These steps read only the quality bands, `ST_CDIST`, `ST_QA` fill values and the `ST_B10` fill and range flag; no temperature is converted, summarised or displayed before this decision. If more than 30% of the cells passing Q13 rules 1 to 3 have less than 70% of their area covered by pixels with at least 5 valid hot-day observations, the primary analysis uses all summer scenes instead, S4 becomes the hot-day analysis, and this is written in `deviations.md` before any LST value is opened.
- Earth Engine quota exceeded: the export is split by year; no change of method.
- Native thermal resolution: TIRS data are 100 m, so a cell's LST contains some signal from neighbouring cells; coefficients are read as neighbourhood-scale, and S7 (1 km) and S17 (covariates in a window) address this.
- Emissivity: USGS reports erroneous ST "wherever NDVI has changed significantly between the ASTER and Landsat eras" (guide, known issues); this matters for Ruhr brownfields and new building sites and is reported as a limitation.
- Any other change: logged in `00_protocol/deviations.md` with date and reason, before the result of the changed analysis is seen whenever possible.

**Q24. Robustness (all reported, including results that disagree with the primary analysis).**
Each sensitivity analysis uses the estimator, fallback and inference rule of Q19 and Q20 unless stated otherwise.
- S1: bracketed census values included. S2: no rent restriction for the other variables. S3: population-weighted models.
- S4: all summer scenes (not only hot days). S5: absolute LST in °C (mean over the used scenes) instead of the anomaly; the choice of heat indicator is known to change results (Schwarz et al., 2011).
- S6: Landsat 8 only. S6b: path 196 only and path 197 only (the cells S6b loses, mainly west Duisburg for path 196, are reported).
- S7: 1 km grid (same aggregation as MGWR), Model A with the same estimator and queen W on the 1 km grid, each 1 km cell assigned to the city that contains the most of its included 100 m cells (ties: the larger summed population); bootstrap blocks are 2 km INSPIRE cells split by the assigned city of their 1 km cells (each 1 km cell belongs to the part of its 2 km cell with the same assigned city; resampling is within assigned city, as in S19); compared with Chawla et al. (2026). The comparison is approximate: they used the 90th percentile of LST 2021 to 2023 and rent per resident.
- S8: spatial lag model, `spreg.GM_Lag(y, X, w=w, robust='white', spat_impacts='power', hard_bound=True)` (if it raises an error, this is logged and S8 is reported as not estimable). Total impact = β_k / (1 − ρ) (exact only when every row of W sums to 1; with islands kept it is an approximation, and S20 gives the exact case); its 95% interval comes from 1,000 draws of (β_k, ρ) from a normal distribution with the estimated covariance matrix (`vm`, ρ is the last element), taking the 2.5th and 97.5th percentiles of β_k / (1 − ρ); draws with |ρ| ≥ 1 are discarded and counted. Direct and indirect impacts are reported as point values. S8 is judged by this interval only (same side of 0 or not; ±0.3 °C rule), without a p-value or Holm adjustment. The P10 to P90 effect uses the total impact.
- S9: weights of the 8 nearest neighbours instead of queen contiguity.
- S10: each of the 11 cities separately (within-study replication), Model A without city dummies, with the same estimator, fallback rule and queen W; reported: number of cities with the same sign as the pooled estimate.
- S11: minimum population of 3 and of 30 instead of 10.
- S12: only scenes with at least 95% valid core reference-domain pixels. S13: anomaly referenced to the median of each city (computed on the core reference domain) instead of all 11 cities.
- S14: composite as the mean of yearly mean anomalies (each year weighted equally). S15: per-scene standardised anomaly (pixel minus median, divided by the scene's interquartile range).
- S16: pixels with `ST_QA` × 0.01 > 3 K also masked (the 3 K limit is a judgement fixed here; the distribution of `ST_QA` of retained pixels is reported).
- S17: tree cover and imperviousness measured in a 300 m × 300 m window centred on the cell (the cell and its 8 neighbours).
- S18: spatial Durbin error model, `spreg.GM_Error_Het(y, X, w=w, hard_bound=True, slx_lags=1, slx_vars=[True]*4 + [False]*(k − 4))`, with the four social variables in the first four columns of X so that only they are lagged (k = number of columns of X; X has no constant column, spreg adds it).
- S19: H3 bootstrap with 2 km blocks.
- S20: cells without an included neighbour dropped and W rebuilt.

**Q25. Exploratory analyses (labelled as such in the paper).**
Interaction of rent with tree cover; vacancy rate (`Leerstandsquote`) as an extra social variable; comparison of our LST pattern with the LANUK modelled day map; ECOSTRESS afternoon LST for a sample of days.

---

## References (each checked by DOI on Crossref, or saved in `Documentation/`)
- Anderson, C. C., & Hasler, N. (2026). Urban heat and public green space: Assessing risk, equity, and the lived experiences of residents in Bochum, Germany. International Journal of Disaster Risk Reduction, 143, 106299. https://doi.org/10.1016/j.ijdrr.2026.106299
- Chakraborty, T., Hsu, A., Manya, D., & Sheriff, G. (2019). Disproportionately higher exposure to urban heat in lower-income neighborhoods: A multi-city perspective. Environmental Research Letters, 14(10), 105003. https://doi.org/10.1088/1748-9326/ab3b99
- Chawla, J., Keller, P., & Benz, S. (2026). Comparing land surface temperature and air temperature for assessing socio-demographic inequalities in urban heat exposure: Evidence from Germany. Environmental Research Letters, 21(15), 154033. https://doi.org/10.1088/1748-9326/ae929e
- Cook, M., Schott, J., Mandel, J., & Raqueno, N. (2014). Development of an operational calibration methodology for the Landsat thermal data archive and initial testing of the atmospheric compensation component of a land surface temperature (LST) product from the archive. Remote Sensing, 6(11), 11244-11266. https://doi.org/10.3390/rs61111244
- Hsu, A., Sheriff, G., Chakraborty, T., & Manya, D. (2021). Disproportionate exposure to urban heat island intensity across major US cities. Nature Communications, 12, 2721. https://doi.org/10.1038/s41467-021-22799-5
- Klopfer, F., & Pfeiffer, A. (2023). Determining spatial disparities and similarities regarding heat exposure, green provision, and social structure of urban areas: A study on the city district level in the Ruhr area, Germany. Heliyon, 9(6), e16185. https://doi.org/10.1016/j.heliyon.2023.e16185
- König, C. (2024). Neighbourhood structure and environmental quality: A fine-grained analysis of spatial inequalities in urban Germany. Urban Studies, 61(10), 1968-1989. https://doi.org/10.1177/00420980231224224
- LANUK NRW (2026). Klimaanalyse NRW 2026: Methoden- und Ergebnisüberblick. Fachbericht 171. Landesamt für Natur, Umwelt und Klima Nordrhein-Westfalen.
- Schwarz, N., Lautenbach, S., & Seppelt, R. (2011). Exploring indicators for quantifying surface urban heat islands of European cities with MODIS land surface temperatures. Remote Sensing of Environment, 115(12), 3175-3186. https://doi.org/10.1016/j.rse.2011.07.003
- U.S. Geological Survey. Landsat 8-9 Collection 2 (C2) Level 2 Science Product (L2SP) Guide, LSDS-1619, version 6.0.
- van den Akker, O. R., Weston, S., Campbell, L., Chopik, B., Damian, R., Davis-Kean, P., Hall, A., Kosie, J., Kruse, E., Olsen, J., Ritchie, S., Valentine, K., van 't Veer, A., & Bakker, M. (2021). Preregistration of secondary data analysis: A template and tutorial. Meta-Psychology, 5. https://doi.org/10.15626/MP.2020.2625
- Weston, S. J., Ritchie, S. J., Rohrer, J. M., & Przybylski, A. K. (2019). Recommendations for increasing the transparency of analysis of preexisting data sets. Advances in Methods and Practices in Psychological Science, 2(3), 214-227. https://doi.org/10.1177/2515245919848684
- Zhou, D., Xiao, J., Bonafoni, S., Berger, C., Deilami, K., Zhou, Y., Frolking, S., Yao, R., Qiao, Z., & Sobrino, J. A. (2019). Satellite remote sensing of surface urban heat islands: Progress, challenges, and perspectives. Remote Sensing, 11(1), 48. https://doi.org/10.3390/rs11010048
