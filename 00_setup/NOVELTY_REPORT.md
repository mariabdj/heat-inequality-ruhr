# Novelty report (Step 0)

**Question checked:** has anyone already tested whether 100 m census grid cells in the Ruhr with lower rents, more foreign residents, more older people or more children are hotter (satellite land surface temperature over several summers), with spatial regression, and how much tree cover and sealed surfaces account for the gap?

**Date:** 2 November 2026. **Answer:** no study found that does this. Five studies come close on one or two dimensions each; they are listed below with what they did and how this project differs. This is a search result, not a proof: the search will be repeated before the preregistration is registered and again before submission.

## 1. How the search was done

| Part | What | Where it is recorded |
|---|---|---|
| Database search | 15 fixed queries (10 in English, 3 in German, 2 on methods), each run on **OpenAlex** and **Crossref** (30 searches), up to 200 records per search | `novelty_search.py` (the queries are written in the script), `novelty_search_log.csv` (query, date, hits reported, records saved), raw answers in `novelty_search/raw/` |
| Pooling | 5,142 records saved, 4,508 unique after removing duplicates (same DOI, or same title when no DOI) | `novelty_records.csv` |
| Screening rule (code) | Kept if the title or abstract mentions heat or temperature AND a social group or justice term AND Germany, the Ruhr, an NRW city or the census grid | `novelty_search.py`, regular expressions `HEAT`, `SOCIAL`, `PLACE` |
| Screening (reading) | All 139 kept titles read; abstracts of the 8 closest read; full text of the 5 closest read on the relevant pages | `novelty_candidates.csv` and section 2 below |
| Grey literature | LANUK Klimaanalyse NRW 2026, Fachbericht 171 (state agency report), pages 16 and 29 to 30 read | `novelty_search/closest/LANUK_Fachbericht_171.pdf` (private copy, not redistributed) |
| Earlier searches | The documentation search of the same day (OpenAlex, Crossref, web, English and German) found the same closest studies | `Documentation/README.md`, "Novelty check" |

The rule is deliberately wide: 139 of 4,508 records passed, and most of them are off topic (energy systems, climate models). That is the price of not missing a close study.

## 2. Closest studies and how this project differs

| Study | What they did (with page) | How this project differs |
|---|---|---|
| **Klopfer & Pfeiffer 2023**, Heliyon, doi:10.1016/j.heliyon.2023.e16185 | 8 Ruhr cities, 275 city districts; **one** Landsat 8 scene from a hot day in 2018 (p. 5); LST, NDVI and a social indicator; Moran's I, Gi*, correlations, k-means. The LST to social status link "remains ambiguous" (abstract, p. 1) | 100 m cells instead of 275 districts; composite of many summer scenes 2018 to 2025 instead of one; rent, foreign citizens, 65+ and under 18 tested separately and together; regression with spatial models, not correlations only; tree cover and imperviousness as explanations |
| **Chawla, Keller & Benz 2026**, Environmental Research Letters, doi:10.1088/1748-9326/ae929e | All of Germany on the **1 km × 1 km** INSPIRE grid (p. 3); Zensus 2022 share of foreigners, share 65+, rent per resident (p. 3); 90th percentile summer LST and air temperature 2021 to 2023 (p. 3). Foreigners live in hotter areas in most cities (abstract) | 100 m instead of 1 km (one of our cells is 1/100 of theirs, so it separates a street block from the park next to it); one region studied in depth instead of a national comparison; spatial regression with greenery as an explanation; rent per m² as published. Their result is the main one we compare with, and a 1 km sensitivity analysis lets us compare directly |
| **Anderson & Hasler 2026**, Int. J. Disaster Risk Reduction, doi:10.1016/j.ijdrr.2026.106299 | Bochum only, 154 statistical districts; heat risk **index** (hazard = maximum LST from about 60 Landsat images 2013 to 2023, exposure, vulnerability incl. migration background) plus a survey and green space cooling scores. They write that "future studies could compare tract resolution outputs with, for example, 100m census grids" (limitations section) | We do what they suggest: 100 m census grid, five cities or the whole Ruhr, a regression instead of an index, mean summer LST instead of the maximum |
| **LANUK Klimaanalyse NRW 2026**, Fachbericht 171 (state agency report, no DOI) | Modelled heat (FITNAH-3D, one simulated summer day) for all NRW; "Betroffenheitsanalyse": density of people 80+, children under 6 and average net cold rent from Zensus 2022, cut into deciles **per municipality** and overlaid with heat zones (p. 16); results as area shares (p. 29) | They map where sensitive groups live and overlay heat; they do not test whether heat is unequally distributed by social group. We use observed satellite temperature, test the gap statistically, and add the share of foreign citizens. Their modelled day map is a useful external check of our LST map (Step 4) |
| **Kühnl et al. 2026**, REAL CORP, doi:10.48494/realcorp2026.0144 | Hamm (a Ruhr city), Augsburg, Zwickau: heat model plus Zensus 2022 age data, vulnerability index | Index, not regression; one Ruhr city; no rent or foreign citizens |

Other studies seen and judged further away (method or place differs): Friesen 2026 (Bavaria, LST on the 100 m grid, access to cool spots: method example), Schlechtweg 2026 (Jena, Iasi, Turku, 100 m heat risk with rent: method example), König 2024 (243,607 German neighbourhoods, environmental quality without LST), Mashhoodi 2021 (Netherlands, LST and GWR), Hüser 2025 (Dortmund green space justice, conference abstract), Keller & Benz EGU 2025 (earlier version of Chawla 2026, 2011 census), Sandholz 2021 (Bonn), Birkmann 2021 (Ludwigsburg), Somvanshi 2025 (Darmstadt), Groth 2026 (Bremerhaven).

## 3. The angle this leaves for the project

1. **Scale:** 100 m census cells for the Ruhr (the national study uses 1 km; the Ruhr studies use districts).
2. **Heat measure:** several summers of observed Landsat surface temperature, not one scene and not a model.
3. **Test, not map:** a statistical test of the gap for rent, foreign citizens, 65+ and under 18, with spatial regression because neighbouring cells are not independent.
4. **Mechanism:** how much of the gap goes with tree cover and sealed surfaces (useful for planners: these can be changed).

## 4. What a reviewer could still say, and our answer

- "Chawla et al. already showed this for Germany." Our answer: different scale (100 m vs 1 km) and depth (spatial models, greenery as explanation, one region); we report a 1 km version to compare directly.
- "LANUK already mapped this." Our answer: LANUK overlays sensitive groups on modelled heat; it does not measure or test the gap.
- "LST is not what people feel." True; stated as a limitation (Venter et al. 2021; Chawla et al. 2026 compare both).

## 5. Pending

- [ ] **[MARIA]** confirms the angle in section 3.
- [ ] Repeat the search (same script) right before the OSF preregistration.
