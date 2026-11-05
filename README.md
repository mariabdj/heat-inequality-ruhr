# Where is the surface hotter? Rent, foreign citizens and summer heat in the Ruhr

Maria Boudjelal, independent researcher, Algiers, Algeria (ORCID 0009-0002-6434-784X)

**Question.** In the 11 independent cities of the Ruhr (Germany), are the 100 m census grid cells with lower rents, more foreign citizens, more older people or more children hotter on summer days, as seen by Landsat land surface temperature, and how much of that gap goes with tree cover and sealed surfaces?

**Status (November 2026).** The analysis plan was preregistered on OSF before any data were opened: https://osf.io/cmxs2/ (DOI https://doi.org/10.17605/OSF.IO/CMXS2), registered 2 November 2026. Data processing, models, sensitivity analyses and their independent checks are done (Steps 2 to 8). The article is in preparation and will be added here with its preprint.

**Main result so far.** Cells with a higher share of foreign citizens have a hotter daytime surface, in every preregistered sensitivity analysis; for rent and age the results are inconclusive. These are results about grid cells, not people, and about surface temperature in the late morning of hot days, not the air or indoor temperature people live with. Correlation, not causation.

## How the project is organised

| Folder | What it holds |
|---|---|
| `00_setup/` | dataset inventory and the novelty search |
| `00_protocol/` | preregistration, every deviation from it (`deviations.md`), expert review log |
| `01_data/` | download and processing scripts, `data_register.csv` (source, date, licence and SHA-256 of every raw file) |
| `02_lst/` | Earth Engine scripts and scene lists for the surface temperature composite |
| `03_covariates/`, `04_grid_join/` | elevation and land cover, and the join of everything on the 100 m grid |
| `05_analysis/` | descriptive results, models, sensitivity analyses, figures; full-precision results in `results/results.json` |
| `verification/` | independent checks (other language or method) and `run_gate.py` |
| `VERIFICATION_LOG.md` | every check run, with its real output |

Raw and large files are not in the repository; `01_data/data_register.csv` says where each one comes from, and the scripts download them again.

## Data sources and licences

- Zensus 2022 grid data: © Statistische Ämter des Bundes und der Länder, Datenlizenz Deutschland Namensnennung 2.0.
- Landsat 8 and 9 Collection 2 Level 2 surface temperature: courtesy of the U.S. Geological Survey.
- Tree Cover Density 2022 and Imperviousness Density 2021: European Union, Copernicus Land Monitoring Service 2026, European Environment Agency (EEA)
- ESA WorldCover 2021 v200 (CC BY 4.0).
- Elevation: Geobasis NRW digital terrain model (dl-de/zero-2-0).
- Municipal boundaries: © BKG, VG250 (dl-de/by-2-0); 100 m grid: © GeoBasis-DE / BKG (dl-de/by-2-0).
- Weather station data: Deutscher Wetterdienst (DWD), Climate Data Center (CC BY 4.0). Hourly air temperature grids: Deutscher Wetterdienst (DWD), HOSTRADA v1.0 (GeoNutzV).
- Modelled heat map used for comparison: LANUK NRW, Klimaanalyse NRW 2026 (dl-de/zero-2-0).
