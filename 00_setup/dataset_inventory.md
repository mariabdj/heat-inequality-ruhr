# Dataset inventory: surface heat and social inequality in the Ruhr

Project 4, setup phase. Compiled on 2 November 2026.

## How to read this file

- Every fact below comes from a web page or official file that was opened on 2 November 2026. The page is given in the "Verified on" line.
- **Status** means:
  - **VERIFIED**: the key facts (variables, resolution, licence, access) were read on an official page or official file.
  - **PARTLY**: some facts were read, others could not be confirmed (the missing ones are named).
  - **UNVERIFIED**: the page could not be read, or only secondary sources were found. Do not use the claim until checked by hand.
- Nothing large was downloaded. Only five small Zensus "dataset description" spreadsheets (about 100 KB each) were opened to read the exact column names, licence and secrecy rules.
- Several NRW and Ruhr portals refused automated connections that day (`ckan.open.nrw.de`, the Dortmund press site, `inkar.de` with a certificate error, and `opendata.ruhr` at times). These are listed in the open questions at the end, to check in Chrome.

---

## 1. Zensus 2022 grid data (Gitterzellen 100 m, 1 km, 10 km)

| Field | Content |
|---|---|
| Provider | Statistische Ämter des Bundes und der Länder (Destatis is the publisher) |
| What it measures | Census results for 15 May 2022 (Stichtag) aggregated to INSPIRE grid cells |
| Spatial resolution | 100 m, 1 km and 10 km cells. Each ZIP holds one CSV per grid size (a few files are 100 m only or 1 km only, see below) |
| Temporal resolution | One date: 15 May 2022 |
| CRS and cell ID | ETRS89-LAEA Europe, **EPSG:3035**. Cell ID format, quoted from the description file: `Gitter_ID_100m = CRS3035RES100mN4534600E5066300` (cell size plus the **lower left corner** coordinates, N then E). The CSV also gives the cell **centre** coordinates in columns `x_mp_100m`, `y_mp_100m` |
| CSV format | Semicolon separated, German decimal comma. Column `werterlaeuternde_Zeichen` holds flags (see secrecy) |
| Access | Direct ZIP download from the Destatis Zensus 2022 page, no account. Note: `www.zensus2022.de` now redirects to `https://www.destatis.de/zensus2022` |
| Account needed? | No |
| Licence | **Datenlizenz Deutschland, Namensnennung, Version 2.0 (dl-de/by-2-0)**, quoted from each dataset description file ("lizenziert unter der Datenlizenz Deutschland, Namensnennung, Version 2.0") |
| Verified on | https://www.destatis.de/zensus2022 (full list of grid files, sizes, description links); dataset description XLSX files under https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Zensus2022/Publikationen/Downloads-Publikationen/Gitterdaten/ (opened: rent, foreigners, 65+, vacancy, population) |
| Status | **VERIFIED** for the variables listed below and for licence, CRS, ID format and secrecy text |

### 1a. Variables we need, confirmed at 100 m

| Our concept | Zensus 2022 grid file (exact title) | 100 m CSV and value column (from the description file) | Unit | Download ZIP | Description version |
|---|---|---|---|---|---|
| Population (weights, filter) | Bevölkerungszahlen in Gitterzellen | `Zensus2022_Bevoelkerungszahl_100m-Gitter.csv`, column `Bevoelkerungszahl` | persons | https://www.destatis.de/static/DE/zensus/gitterdaten/Zensus2022_Bevoelkerungszahl.zip (18 MB) | Version 2, 30.09.2024 |
| **Average net cold rent per m²** | Durchschnittliche Nettokaltmiete in Gitterzellen | `Zensus2022_Durchschn_Nettokaltmiete_100m-Gitter.csv`, column `durchschnMieteQM` | EUR per m², rented dwellings in residential buildings (no dormitories); rent-free dwellings excluded | https://www.destatis.de/static/DE/zensus/gitterdaten/Zensus2022_Durchschn_Nettokaltmiete.zip (9 MB) | Version 2, 30.09.2024 |
| Rent plus number of dwellings (useful as weight for the rent value) | Durchschnittliche Nettokaltmiete und Anzahl der Wohnungen in Gitterzellen | column names not opened | | https://www.destatis.de/static/DE/zensus/gitterdaten/Durchschnittliche_Nettokaltmiete_und_Anzahl_der_Wohnungen.zip (10.8 MB) | not opened |
| Rent by building age and dwelling size | Durchschnittliche Nettokaltmiete nach Gebäudealter und Wohnungsgröße | **100 m only** ("nur 100 m Gitter") | | http://www.destatis.de/static/DE/zensus/gitterdaten/Durchschnittliche_Nettokaltmiete_nach_Gebaeudealter_und_Wohnungsgroeße.zip (15.9 MB) | not opened |
| **Share of foreign citizens** | Ausländeranteil in Gitterzellen | `Zensus2022_Anteil_Auslaender_100m-Gitter.csv`, column `AnteilAuslaender` | % of total population | https://www.destatis.de/static/DE/zensus/gitterdaten/Auslaenderanteil_in_Gitterzellen.zip (19.63 MB) | Version 1, 07.10.2024 |
| Share of foreigners, EU and non-EU | Ausländeranteil nach EU- und nicht EU-Staatsangehörigkeit in Gitterzellen | not opened | | https://www.destatis.de/static/DE/zensus/gitterdaten/Auslaenderanteil_EU_nichtEU_Gitterzellen.zip | not opened |
| **Share aged 65+** | Anteil der ab 65-Jährigen in Gitterzellen | `Zensus2022_Anteil_ueber_65_100m-Gitter.csv`, column `AnteilUeber65` | % of total population | https://www.destatis.de/static/DE/zensus/gitterdaten/Anteil_ab_65-jaehrige_in_Gitterzellen.zip (21.06 MB) | Version 1, 07.10.2024 |
| **Share under 18** | Anteil der unter 18-Jährigen in Gitterzellen | file listed; columns not opened (description file `datensatzbeschreibung_Anteil_unter_18.xlsx`) | % (expected, same family as 65+) | https://www.destatis.de/static/DE/zensus/gitterdaten/Anteil_unter_18-jaehrige_in_Gitterzellen.zip (20.64 MB) | not opened |
| Age in 5-year groups (for under 6, 80+ etc.) | Alter in 5er-Jahresgruppen in 100 Meter-Gitter | 100 m | counts | https://www.destatis.de/static/DE/zensus/gitterdaten/Alter_5er-Jahresgruppen_100mGitter.zip | not opened |
| Other age files | Durchschnittsalter; Alter in 5 Altersklassen; Alter in 10er-Jahresgruppen; Alter in infrastrukturellen Altersgruppen | all grids | | see Destatis page | not opened |
| **Vacancy rate** | Leerstandsquote in Gitterzellen | `Zensus2022_Leerstandsquote_100m-Gitter.csv`, column `Leerstandsquote` | % of vacant dwellings among occupied plus vacant dwellings (no holiday or commercial dwellings) | https://www.destatis.de/static/DE/zensus/gitterdaten/Leerstandsquote_in_Gitterzellen.zip (12.37 MB) | **Version 2, 05.02.2025** (corrected, see caveat) |
| Market-active vacancy rate | Marktaktive Leerstandsquote in Gitterzellen | not opened | | https://www.destatis.de/static/DE/zensus/gitterdaten/Marktaktive_Leerstandsquote_in_Gitterzellen.zip | |
| **Ownership rate** | Eigentümerquote in Gitterzellen | not opened | | https://www.destatis.de/static/DE/zensus/gitterdaten/Eigentuemerquote_in_Gitterzellen.zip | |
| **Average household size** | Durchschnittliche Haushaltsgröße in Gitterzellen | not opened | | https://www.destatis.de/static/DE/zensus/gitterdaten/Durchschnittliche_Haushaltsgroesse_in_Gitterzellen.zip | |
| Household size classes | Größe des privaten Haushalts in Gitterzellen | | | https://www.destatis.de/static/DE/zensus/gitterdaten/Zensus2022_Groesse_des_privaten_Haushalts_in_Gitterzellen.zip | |
| Senior households | Seniorenstatus eines privaten Haushalts in Gitterzellen | | | https://www.destatis.de/static/DE/zensus/gitterdaten/Seniorenstatus_eines_privaten_Haushalts.zip | |
| **Living space per resident** | Durchschnittliche Wohnfläche je Bewohner in Gitterzellen | | m² | https://www.destatis.de/static/DE/zensus/gitterdaten/Durchschnittliche_Wohnflaeche_je_Bewohner_in_Gitterzellen.zip | |
| **Dwelling size** | Durchschnittliche Wohnfläche je Wohnung in Gitterzellen; Fläche der Wohnung (10m²-Intervalle); Wohnungen nach Zahl der Räume | | | see Destatis page | |
| **Building age** | Gebäude nach Baujahr (Jahrzehnte); Gebäude nach Baujahr in Mikrozensus-Klassen; Gebäude nach Baujahresklassen; Wohnungen nach Baujahresklassen in 100 Meter-Gitter; Wohnungen nach modifizierten Mikrozensusbaujahresklassen im 100 Meter-Gitter | | counts by class | see Destatis page | |
| **Heating type** | Wohnungen nach überwiegender Heizungsart; Gebäude mit Wohnraum nach überwiegender Heizungsart; Wohnungen / Gebäude nach Energieträger der Heizung | | counts by class | e.g. https://www.destatis.de/static/DE/zensus/gitterdaten/Zensus2022_Heizungsart.zip | |
| Building type, ownership form | Wohnungen nach Gebäudetyp (Größe); Gebäude mit Wohnraum nach Gebäudetyp (Größe); Gebäude nach Eigentumsform in 100 Meter-Gitter | | | see Destatis page | |
| Other population | Staatsangehörigkeit (several files); Geburtsland (Gruppen); Familienstand; Religion; family and household types | | | see Destatis page | |

The Destatis page lists 50 Zensus 2022 grid ZIP files in total. The page states: "Jedes ZIP-Archiv enthält die Daten des Themas für das 10km-, 1km- und 100m-Gitter als csv-Datei". Exceptions seen in the labels: rent by building age and size (100 m only), some "in 100 Meter-Gitter" files, and "Beheizte Gebäude nach Baujahr, Typ, Energie im 1km-Gitter" (1 km only).

**Not found at grid level:** income, unemployment, SGB II, education, migration background ("Migrationshintergrund"). The grid has citizenship and country of birth only. Rent is the only economic proxy at 100 m (this is also why LANUK uses it, see section 6e).

### 1b. Secrecy, rounding and missing cells (important for missing data)

Quoted or closely translated from the dataset description files (sheet "Erläuterungen"):

1. Secrecy uses the **Cell-Key Method (CKM)**, a "stochastic overlay": some counts are published slightly changed from the true value (Destatis page example: "+2 oder -1"). Single values therefore do not always add up to totals.
2. Ratios (shares, averages) are computed from the slightly changed counts. When the counts behind a ratio are very small, the change can be large in percent. **Such values are shown in brackets** (flag "KLAMMERN = Aussagewert eingeschränkt, da der Zahlenwert statistisch relativ unsicher ist"). In the CSV this flag is in the column `werterlaeuternde_Zeichen`.
3. A dash symbol means "Genau Null oder auf Null geändert" (exactly zero **or changed to zero** by secrecy).
4. "Gitterzellen in denen keine Personen leben oder in denen es keine Wohnungen gibt, sind nicht in der Datei enthalten. Dies kann ggf. auch durch das angewendete Geheimhaltungsverfahren bedingt sein." So: cells missing from a file are either empty, or removed by secrecy. You cannot tell which from the file alone.
5. "Leere Werte-Zellen kommen nicht vor" (no blank value cells inside the file).
6. Each address is assigned to exactly one cell by its geocoordinate (BKG is the main source of coordinates), even if the building crosses cell borders.
7. No fixed rule like "cells with fewer than X persons are suppressed" is written in the description files. **UNVERIFIED** whether such a threshold exists; the Destatis secrecy method paper (old URL `zensus2022.de/.../Methodenpapier-Geheimhaltung.pdf`) now redirects and could not be read.

Caveats for our study:
- Rent exists only where there are rented dwellings, so owner-occupied single-family areas will have no or bracketed rent values. This is **not missing at random** (it is linked to wealth and building type).
- Plan: keep a flag for bracketed values, run the main model with and without them, and use a minimum population or dwelling count filter decided before seeing results.
- Vacancy, market-active vacancy and ownership rate were **corrected on 5 February 2025** (too few "zero" cells in the first version, 19 Sep 2024 to 5 Feb 2025). Download only the current version and record the version date.
- Zensus counts persons by residence on 15 May 2022. LST summers 2018 to 2025 are around this date; say this clearly in the paper.

### 1c. Zensus 2011 grid (for comparison)

| Field | Content |
|---|---|
| Files | Nine 2011 ZIPs listed on the same Destatis page, including "Bevölkerung im 100 Meter-Gitter", "Haushalte im 100 Meter-Gitter", "Wohnungen im 100 Meter-Gitter", "Gebäude im 100 Meter-Gitter", "Klassierte Werte im 1 Kilometer-Gitter", "Spitze Werte im 1 Kilometer-Gitter" (base path `http://www.destatis.de/static/DE/zensus/2011_gitterdaten/`) |
| What is comparable | According to the z22 documentation, share of foreigners, share 65+, share under 18 and vacancy share exist for 2011 **only at 1 km**; average rent is **2022 only** |
| Licence | **UNVERIFIED** for the 2011 grid files (the page states dl-de/by-2-0 only for the 2011 boundary shapefile). The page text also says 2011 datasets will be added "in Kürze", while the links are already shown |
| Verified on | https://www.destatis.de/zensus2022 ; https://jslth.github.io/z22/ |
| Status | **PARTLY** |
| Caveat | Not needed for the core question. 2011 is useful only as a robustness or change check at 1 km |

---

## 2. Tools to read the Zensus grid

### 2a. R package `z22`

| Field | Content |
|---|---|
| What it does | "Provides fast and easy access to German census grid data from the 2011 and 2022 censuses." Main function `z22_data(feature, categories, year, res, all_cells, normalize, as, update_cache)`; also `z22_features()`, `z22_categories()`, `z22_grid()`, `z22_inspire_generate()`, `z22_inspire_extract()`, `z22_decode()`, `z22_pivot_longer()` |
| Author, maintainer | Jonas Lieth (GitHub `jslth`) |
| Version | **1.1.4, published 2026-01-23 on CRAN** |
| Licence | MIT + file LICENSE (the package code). The data keep dl-de/by-2-0 |
| Resolutions and years | 2022: 100 m, 1 km, 10 km ("For Census 2022, all features are available at all resolutions"). 2011: 100 m and 1 km only |
| Relevant feature names | `rent_avg` (Average net cold rent, 2022 only), `foreigners` (Share of foreigners), `age_from_65`, `age_under_18`, `vacancies`; plus categorical features such as `dwelling_heat_type`, `building_constr_year`, `household_size_group`, `dwelling_ownership_home` |
| Data source | GitHub repository `JsLth/z22data`: the census grid files re-cut into Parquet files (`{feature}_{category}.parquet`), plus INSPIRE grids from BKG. Its README warns: "use them at your own risk and do not take the correctness of the data files for granted" |
| Missing values | By default only cells with data are returned; `all_cells = TRUE` joins to the full grid. The manual notes some shares can be above 1, "possibly due to the key-cell method". **The manual does not say how bracketed (uncertain) values are handled. UNVERIFIED** whether the bracket flag is kept |
| Output CRS | Example raster in EPSG:3035 |
| Access | `install.packages("z22")` in R 4.6 |
| Verified on | https://cloud.r-project.org/web/packages/z22/index.html ; https://ftp.fau.de/cran/web/packages/z22/refman/z22.html ; https://jslth.github.io/z22/ ; https://github.com/JsLth/z22data |
| Status | **VERIFIED** (bracket flag handling UNVERIFIED) |
| Caveat | Use `z22` only as a convenience and a cross-check. The **primary source should be the official Destatis CSVs**, because they keep the bracket flag and the version date. Compare both for a sample of cells (independent check) |

### 2b. Python equivalent

- No PyPI package for the Zensus grid was found (search on 2 Nov 2026). **UNVERIFIED** that none exists.
- Practical options: read the official CSVs with pandas (sep=";", decimal=","), or read the `z22data` Parquet files directly with pandas or pyarrow (the README only says the files are Parquet; Python use is not documented).
- `pystatis` (CorrelAid) is a Python client for GENESIS-Online, the Regionaldatenbank and the **Zensus Datenbank**. It does **not** give grid cells. Zensus database access needs credentials or an API token (page: "old credentials are no longer valid"). Verified on https://correlaid.github.io/pystatis . Status: **PARTLY** (version not shown on the page).

### 2c. BKG INSPIRE grid geometry (GeoGitter Inspire)

| Field | Content |
|---|---|
| What | Empty grid polygons for Germany, the official geometry that matches the Zensus cell IDs |
| Sizes | 100 m, 250 m, 500 m, 1 km, 5 km, 10 km, 100 km |
| Files | e.g. 100 m: CSV 390 MB https://daten.gdz.bkg.bund.de/produkte/sonstige/geogitter/aktuell/DE_Grid_ETRS89-LAEA_100m.csv.zip ; GeoPackage 2 GB https://daten.gdz.bkg.bund.de/produkte/sonstige/geogitter/aktuell/DE_Grid_ETRS89-LAEA_100m.gpkg.zip |
| CRS | ETRS89-LAEA (file names). EPSG code not printed on the page, but the Zensus description file states EPSG:3035 |
| Licence | dl-de/by-2-0; credit "© GeoBasis-DE / BKG (Jahr des letzten Datenbezugs) dl-de/by-2-0" |
| Account | No |
| Verified on | https://gdz.bkg.bund.de/index.php/default/open-data/geographische-gitter-fur-deutschland-in-lambert-projektion-geogitter-inspire.html |
| Status | **VERIFIED** |
| Caveat | Very large for all of Germany. Simpler: build the cell polygons ourselves from the Zensus cell ID (lower left corner plus 100 m), and check a sample against the BKG grid |

---

## 3. Landsat 8 and 9 Collection 2 Level 2 surface temperature

| Field | Content |
|---|---|
| Provider | USGS (served in Google Earth Engine) |
| GEE IDs | `LANDSAT/LC08/C02/T1_L2` (available 2013-03-18 to 2026-10-26 at the time of reading); `LANDSAT/LC09/C02/T1_L2` (2021-10-31 to 2026-10-30) |
| What it measures | Land surface temperature (LST, skin temperature of the surface), band `ST_B10`, in kelvin |
| Scale and offset | **ST_B10 × 0.00341802 + 149.0 = kelvin**. Confirmed on the GEE pages (scale 0.00341802, offset 149) and on the USGS FAQ. USGS worked example: raw value 44,947 gives 302.6 K. Fill value 0; data type unsigned 16-bit; USGS FAQ valid range 293 to 65535 |
| Resolution | Delivered at 30 m ("Pixel size: 30 meters (all bands)" in GEE). Native TIRS resolution is 100 m: USGS EROS says the thermal bands "capture data with a minimum of 100 meter resolution" and "are registered to and delivered with the 30-meter OLI data product". So 30 m pixels are resampled, not true 30 m detail |
| Overpass | Equatorial crossing time **10:12 a.m. ± 5 minutes** (USGS Landsat 8 and Landsat 9 pages). Local time over the Ruhr is therefore late morning; the exact local clock time should be read from each scene's metadata (`DATE_ACQUIRED`, `SCENE_CENTER_TIME`, UTC) |
| Revisit | 16 days each; Landsat 9 is offset 8 days from Landsat 8, so about every 8 days together |
| QA_PIXEL bits (GEE page) | Bit 0 Fill; Bit 1 Dilated Cloud; Bit 2 Cirrus (high confidence); Bit 3 Cloud; Bit 4 Cloud Shadow; Bit 5 Snow; Bit 6 Clear; Bit 7 Water; Bits 8-9 Cloud Confidence; Bits 10-11 Cloud Shadow Confidence; Bits 12-13 Snow/Ice Confidence; Bits 14-15 Cirrus Confidence |
| Other ST bands | `ST_QA` (uncertainty of ST in K, scale 0.01); `ST_EMIS` (band 10 emissivity "estimated from ASTER GED", scale 0.0001); `ST_ATRAN`, `ST_CDIST` (distance to cloud), `ST_DRAD`, `ST_EMSD`, `ST_TRAD`, `ST_URAD` |
| Licence | Public domain: "Landsat datasets are federally created data and therefore reside in the public domain"; credit USGS |
| Account | Through GEE: a Google account plus a registered Cloud project (section 4). Direct USGS download would need a USGS EarthExplorer account (not checked) |
| Science product guide | Landsat 8-9 Collection 2 Level 2 Science Product Guide: https://www.usgs.gov/media/files/landsat-8-collection-2-level-2-science-product-guide (link given on the USGS ST page; the PDF itself was **not opened**) |
| Verified on | https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_L2 ; https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC09_C02_T1_L2 ; https://www.usgs.gov/landsat-missions/landsat-collection-2-surface-temperature ; https://www.usgs.gov/faqs/how-do-i-use-scale-factor-landsat-level-2-science-products ; https://www.usgs.gov/landsat-missions/landsat-8 ; https://www.usgs.gov/landsat-missions/landsat-9 ; https://www.usgs.gov/centers/eros/science/usgs-eros-archive-landsat-archives-landsat-8-oli-operational-land-imager-and |
| Status | **VERIFIED** (the PDF guide itself still to be read) |

Known caveats (quoted from USGS and GEE pages):
- Emissivity comes from ASTER GED, adjusted with ASTER NDVI. Where ASTER GED has gaps, ST is missing, and these gaps are "consistent through time" (static). Check whether any Ruhr pixels are affected.
- "A known error exists in the surface temperature retrievals relative to clouds and possibly cloud shadows" (use `ST_CDIST` and a cloud buffer).
- Emissivity errors where NDVI changed a lot between the ASTER era and now (new buildings, cleared land, mining sites in the Ruhr).
- "Blockiness" for small targets.
- Atmospheric inputs changed source in January 2024 (GEOS for Instrument Teams, before that FP-IT). Possible small step in the time series; check by year.
- If `PROCESSING_LEVEL` is `L2SR`, ST bands are fully masked (only surface reflectance). Filter to L2SP scenes.
- LST is not air temperature. A 10:12 overpass misses the afternoon peak and the night (the night is when heat harms health most). Say this in the paper.

---

## 4. Google Earth Engine access for noncommercial research (2026)

| Field | Content |
|---|---|
| What is needed | A Google Cloud project with the Earth Engine API enabled, **registered for noncommercial use**, and the right roles for the Google account |
| Noncommercial registration | Fill in the eligibility questionnaire in the Cloud console. No billing needed for the free tier. Projects must **reverify noncommercial status every year** |
| Quota tiers (new) | Quotas for noncommercial projects began **27 April 2026** (rolling out gradually). Community Tier: **150 EECU-hours per month**. Contributor Tier: 1,000 EECU-hours per month, **needs an active billing account** ("you won't be charged for Google Earth Engine noncommercial usage"). Partner Tier: 100,000 EECU-hours per month, separate application |
| When quota runs out | Not a hard stop: "restricted mode" with lower throughput until the monthly reset |
| Rule | Splitting work over several projects to get more quota is "quota farming" and breaks the Terms of Service (secondary source; not re-read on the official page) |
| Verified on | https://developers.google.com/earth-engine/guides/access ; https://developers.google.com/earth-engine/guides/noncommercial_tiers |
| Status | **VERIFIED** (quota farming sentence: PARTLY) |
| Caveat | 8 summers of Landsat over the Ruhr, reduced to 100 m cells, should fit in the Community Tier if we export cell means once and keep code efficient. **UNVERIFIED estimate**: measure EECU use on a test export first. Does Maria count as eligible "noncommercial" as an independent researcher? Very likely yes (research use), but the questionnaire answer is hers to give |

---

## 5. Copernicus Land Monitoring Service (CLMS) products

### 5a. Access and licence (all CLMS products)

- Registration is needed **only to download**: "It is required to register only to download data on our website" (CLMS FAQ). Catalogue records say "Download (requires authentication)". The login is EU Login according to secondary sources (**PARTLY**: the FAQ page read did not name EU Login).
- Conditions (EEA catalogue records): "full, open and free access"; users must inform the public of the source, state any modifications, and must not imply EU endorsement.
- Verified on: https://land.copernicus.eu/en/faq/general-questions ; EEA catalogue records below.

### 5b. Urban Atlas 2018 and 2021 (land use / land cover)

| Field | Content |
|---|---|
| What | Land use and land cover polygons for Functional Urban Areas (FUAs) |
| Years | 2006, 2012, 2018, **2021** (2021 update announced on the CLMS news page dated 02.06.2026; the 2021 Product User Manual is version 1.0.1, 5 Feb 2026) |
| MMU | 0.25 ha urban, 1 ha rural (2021 manual) |
| Classes | The 2021 manual is inconsistent (says 28 in one place, 27 in Annex 1) |
| Coverage | 790 FUAs (EEA-38 except Liechtenstein, plus UK); change 2018-2021 for 764 FUAs |
| Format, CRS | GeoPackage, EPSG:3035 |
| Access | CLMS website (login) and Copernicus Data Space Ecosystem (CDSE) |
| Verified on | https://land.copernicus.eu/en/news/urban-atlas-2021-product-update-is-now-available ; https://library.land.copernicus.eu/products/Urban_Atlas_CLMS_UA2021_LULC_PUM_v1.html ; https://sdi.eea.europa.eu/catalogue/srv/api/records/e006507d-15c8-49e6-959c-53b61facd873 |
| Status | **PARTLY** (which Ruhr FUAs exist and their exact boundaries not checked) |
| Caveat | Polygons, not rasters: we compute area shares per 100 m cell. Check that all five cities (and the whole RVR area, if used) lie inside Urban Atlas FUAs |

### 5c. Urban Atlas Street Tree Layer (STL)

| Field | 2018 | 2021 |
|---|---|---|
| Title | Urban Atlas Street Tree Layer 2018 (vector), Europe, 6-yearly, Feb. 2021 | Urban Atlas Street Tree Layer 2021 (vector), Europe, 3-yearly, Jan. 2026 |
| Published | 2020-05-06 (revised 2021-02-04) | **2026-01-31** (edition 01.00) |
| Temporal extent | 2017-01-01 to 2019-12-31 | 2020-01-01 to 2021-12-31 |
| What | Rows or patches of trees of 500 m² or more over artificial surfaces inside the FUA | same; MMU 0.05 ha (= 500 m²); the 10 m minimum width "was deemed no longer necessary" |
| Scale / imagery | 10 m resolution, min. width 10 m | 1:5,000; 2 or 4 m source imagery |
| Format | GeoPackage | FlatGeobuf |
| Access | CLMS download (authentication) | CLMS download (authentication) |
| Verified on | https://sdi.eea.europa.eu/catalogue/copernicus/api/records/205691b3-7ae9-41dd-abf1-1fbf60d72c8c | https://sdi.eea.europa.eu/catalogue/srv/api/records/ed0018c3-5ad0-4721-b5e4-0042aeaf9d00 |
| Status | **VERIFIED** | **VERIFIED** |

Caveat: STL misses single trees and small groups below 500 m², and trees in gardens may be in other classes. Good as a "street and urban tree" covariate, not a full canopy map.

### 5d. High Resolution Layer Tree Cover Density (TCD)

| Field | Content |
|---|---|
| Title | Tree Cover Density 2018 - Present (raster 10m), Europe, yearly, Nov. 2024 |
| Published | 2024-12-01, edition 01.00 |
| Years | Yearly from 2018 (open-ended temporal extent) |
| Resolution, values | 10 m; 0 to 100 % tree crown cover per pixel |
| CRS, format | EPSG:3035 (plus overseas UTM codes); GeoTIFF |
| Access | CLMS download (authentication). WEkEO names (secondary source): `clms_vlcc_tree-cover-density_europe_10m_yearly_v1` and a confidence layer |
| Note | The product page `high-resolution-layer-tree-cover-density` now redirects to `high-resolution-layer-forests-and-tree-cover` |
| Verified on | https://sdi.eea.europa.eu/catalogue/srv/api/records/e677441e-fb94-431c-b4f9-304f10e4dfd8 |
| Status | **PARTLY**: which exact years (2021? 2022? 2023? 2024?) are already published is **UNVERIFIED** |
| Caveat | Pick the year closest to the LST period middle and to 2022 (census). Check the confidence layer |

### 5e. High Resolution Layer Imperviousness Density

| Field | Content |
|---|---|
| Versions | **2021** (news dated 19 Sep 2025): 10 m Imperviousness Density, Impervious Built-Up, new Built-Up Change 2018-2021. **2024** (news dated 11.06.2026): 10 m Imperviousness Density and Impervious Built-Up; input is Sentinel-2 Collection 1; interannual calibration refined; validation reports planned Q3 2026 |
| Values | 0 to 100 % sealing per pixel |
| Coverage | EEA38 plus UK |
| Also | EEA service "HarmonisedImperviousnessLayer2024v2026" (100 m harmonised series 2006 to 2024, secondary source only) |
| Verified on | https://land.copernicus.eu/en/news/product-update-high-resolution-layer-imperviousness-2021 ; https://land.copernicus.eu/en/news/product-update-high-resolution-layer-imperviousness-2024 |
| Status | **PARTLY** (licence and download page for the 2024 layer not opened; assumed same CLMS conditions) |
| Caveat | Imperviousness and tree cover are strongly negatively correlated. Watch for collinearity (VIF) in the models |

---

## 6. Other heat data

### 6a. ECOSTRESS LST (ISS)

| Field | Content |
|---|---|
| Product | ECO_L2T_LSTE V002, "ECOSTRESS Tiled Land Surface Temperature and Emissivity Instantaneous L2 Global 70 m" |
| GEE ID | `NASA/ECOSTRESS/L2T_LSTE/V2` (available 2018-07-09 to 2026-10-31 at the time of reading) |
| Resolution | 70 m (GEE: "70 meters (all bands)"); instrument nadir pixel 38 m × 69 m |
| Bands | `LST` (K), LST error, `QC`, emissivity, cloud mask (bit 0), water mask, view zenith angle |
| Time of day | Varies, because of the ISS orbit; the mission page says it allows "diurnal coverage". No fixed overpass time. Coverage 52° N to 52° S (NASA Earthdata page): the Ruhr (about 51.4 to 51.6° N) is just inside |
| Licence | "openly shared, without restriction"; cite Hook and Hulley, DOI 10.5067/ECOSTRESS/ECO_L2T_LSTE.002 |
| Account | Through GEE: same as Landsat. Direct download from NASA: Earthdata Login is likely needed (**UNVERIFIED**, the page did not say) |
| Verified on | https://developers.google.com/earth-engine/datasets/catalog/NASA_ECOSTRESS_L2T_LSTE_V2 ; https://www.earthdata.nasa.gov/data/catalog/lpcloud-eco-l2t-lste-002 ; https://ecostress.jpl.nasa.gov/mission |
| Status | **VERIFIED** (how many clear summer afternoon and night scenes exist over the Ruhr is **UNVERIFIED**) |
| Caveat | Very useful as a sensitivity check at other times of day (afternoon, night). Scenes are irregular; a "summer composite" mixes times of day. Count scenes per hour band before using |

### 6b. Sentinel-3 SLSTR LST

| Field | Content |
|---|---|
| Product | SL_2_LST (Level 2 land surface temperature), 1 km grid, NRT and NTC versions |
| Availability | Sentinel-3A since July 2017, Sentinel-3B since November 2018 (from a peer-reviewed validation study, doi 10.3390/rs16183403) |
| Access | Copernicus Data Space Ecosystem (STAC collections `sentinel-3-sl-2-lst-ntc`, `-nrt`) |
| Verified on | https://cis2.eea.europa.eu/product/480 ; https://fedeo.ceos.org/series/eo:organisationName/ESA@ESRIN/sentinel-3-sl-2-lst-ntc/2026/07 (search results only, pages not fully opened) |
| Status | **UNVERIFIED** (only search summaries read) |
| Caveat | 1 km is far too coarse for 100 m cells. Only for a regional day and night context. Not recommended for the core |

### 6c. DWD Climate Data Center (air temperature stations)

| Field | Content |
|---|---|
| What | Station observations, e.g. hourly air temperature at 2 m |
| Path | https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/air_temperature/ (folders `historical/`, `recent/`; English description PDF in that folder) |
| Ruhr stations (hourly temperature, from the station list read on 2 Nov 2026) | 00555 Bochum (from 2008-01-01); 01303 Essen-Bredeney (from 1951-01-01); 13670 Duisburg-Baerl (from 2007-06-01); 13696 Waltrop-Abdinghof (from 2007-12-01). All active to 2026-11-01 |
| Licence | **CC BY 4.0** ("Terms of use for data on the CDC-OpenData area", status May 2024) |
| Account | No |
| Verified on | the folder above; station list `.../recent/TU_Stundenwerte_Beschreibung_Stationen.txt`; https://opendata.dwd.de/climate_environment/CDC/Terms_of_use.pdf |
| Status | **VERIFIED** |
| Caveat | Too few stations for cell-level analysis. Use to pick hot clear days (air temperature at overpass time) and to describe each summer |

### 6d. City measurement networks

**Dortmund Klimamessnetz (Data2Resilience)**

| Field | Content |
|---|---|
| What | 105 sensors at 76 sites; air temperature, humidity, wind, radiation, precipitation, plus black globe sensors. Measurements every 5 minutes. Built in the Data2Resilience project with Ruhr-Universität Bochum and Leibniz Universität Hannover |
| Datasets | `klimasensoren-historie` (history, about 12 million records, **from 2025-07-01**), `klimasensoren-standorte` (locations), `klimasensoren-messdaten`, `klimasensoren-aktuelle-messungen` |
| Field for air temperature | `data_air_temperature` ("Lufttemperatur"); sensor types SHT35 and ATM41 measure air temperature directly; Black Globe values include radiation and are not comparable |
| Licence | Datenlizenz Deutschland, Zero, Version 2.0 |
| Access | Opendatasoft API, e.g. https://open-data.dortmund.de/api/explore/v2.1/catalog/datasets/klimasensoren-historie ; no account |
| Verified on | Dortmund open data catalogue API (read 2 Nov 2026) |
| Status | **VERIFIED** |
| Caveat | Starts July 2025: covers only the summer of 2025 (and 2026). Useful to check LST against air temperature in one city for one summer, not for 2018 to 2024 |

**Bochum, Ruhr-Universität, Klimastation Rudolf Geiger**

| Field | Content |
|---|---|
| What | One station, run since 1990 by the Geography Institute of RUB, built to DWD standards. Tags include temperature, humidity, radiation, albedo, surface temperature |
| Open data period | 2024-01-01 to 2026-10-31 (one CSV `bochum_rub_bucl_rgs.csv`) |
| Licence | CC0 |
| Verified on | https://bochum.opendata.ruhr/dataset/bochum-rub-bucl-rgs |
| Status | **PARTLY** (columns and time step not seen) |

**Bochum city-wide network, Essen, Duisburg, Gelsenkirchen networks**: **UNVERIFIED**. No open city-wide sensor network was found for these cities.

### 6e. LANUK Klimaanalyse NRW 2026 (Klimaatlas NRW) and its Betroffenheitsanalyse

| Field | Content |
|---|---|
| Provider | LANUK NRW (Landesamt für Natur, Umwelt und Klima, formerly LANUV) |
| What | Model-based climate analysis with FITNAH-3D at **25 m × 25 m** (previous 2018 analysis: 100 m). Two scenarios: "typischer Sommertag" and "extremer Sommertag" (radiation weather, cloudless, simulation day 21 June). Maps: Klimatopkarte, Klimaanalysekarte Tag, Klimaanalysekarte Nacht, Planungshinweiskarte, Regionalkarte, **Betroffenheitsanalyse** |
| Betroffenheitsanalyse | Combines heat load with **density of very old people (80+), density of small children (under 6) and average net cold rent** from **Zensus 2022**, evaluated on building blocks (Baublöcke). Each indicator is cut into deciles per municipality; low rent gets decile 10 (most sensitive) as a poverty-risk proxy, "da für NRW keine räumlich ausreichend" fine poverty data exist (Fachbericht 171, p. 15 to 16 and section 3.6 p. 29) |
| Download | OpenGeodata.NRW folder https://www.opengeodata.nrw.de/produkte/umwelt_klima/klima/klimaanalyse/ : day map TIFF (246 MB) and GeoPackage, night map TIFF (364 MB) and GeoPackage, Betroffenheitsanalyse GeoPackage (2.97 GB), metadata ZIP (13 MB). File dates April 2026. All in EPSG:25832 |
| Licence | **Datenlizenz Deutschland, Zero, Version 2.0** ("Jede Nutzung ist ohne Einschränkungen oder Bedingungen zulässig"), shown on the OpenGeodata.NRW folder page |
| Account | No |
| Verified on | https://www.opengeodata.nrw.de/produkte/umwelt_klima/klima/klimaanalyse/ (and `index.json` in each subfolder) ; https://www.lanuk.nrw.de/fileadmin/lanuvpubl/3_fachberichte/Fachbericht_171.pdf (pages 5, 6, 7, 15, 16, 29 read) ; https://www.land.nrw/pressemitteilung/nordrhein-westfalen-staerkt-die-kommunen-beim-schutz-vor-klimarisiken-wie-hitze (24 April 2026) |
| Status | **VERIFIED** |
| Caveat | **Very important for our novelty claim.** The state already published, in April 2026, a map that overlaps modelled heat with elderly, children and Zensus 2022 rent in all NRW cities. Our study must be clearly different: (1) observed satellite LST over 8 summers instead of one modelled day; (2) formal inequality statistics and spatial regression instead of a decile overlay; (3) foreign citizens share; (4) how much green and tree cover explain the gap. It must cite Fachbericht 171. The modelled day and night maps are also a useful **external check** of our LST pattern (and give a night view that Landsat cannot) |

---

## 7. Boundaries

### 7a. RVR (Regionalverband Ruhr) boundary

| Field | Content |
|---|---|
| Datasets | "WMS der Verwaltungsgrenzen - Verbandsgrenze" (Geoportal Ruhr), licence **dl-zero-de/2.0** on the resources, modified 2026-09-30; and "Netzplan - Verbandsgrenze RVR", licence dl-by-de/2.0, modified 2026-10-09 |
| Download | WFS, e.g. `https://geodaten.metropoleruhr.de/verwaltungsgrenzen/grenzen?service=WFS&version=2.0.0&request=GetFeature&typeNames=verbandsgrenze&outputFormat=geopackage` (also geojson, csv, shapezip) |
| Account | No |
| Verified on | CKAN API of https://opendata.ruhr (package search "verbandsgrenze", read 2 Nov 2026) |
| Status | **PARTLY** (the WFS link itself was not opened; one search summary claimed a "non_open" flag on the open.nrw copy, while the resources carry dl-zero-de/2.0. Check in Chrome) |

### 7b. BKG VG250 municipalities

| Field | Content |
|---|---|
| Product | Verwaltungsgebiete 1:250 000 Stand 01.01. (VG250 01.01.), Aktualitätsstand 01.01.2026, yearly |
| Formats, CRS | Shapefile (GK3, TM32, UTM32s), GeoPackage (UTM32s), Excel |
| Example link | https://daten.gdz.bkg.bund.de/produkte/vg/vg250_ebenen_0101/aktuell/vg250_01-01.utm32s.gpkg.ebenen.zip (69 MB) |
| Licence | dl-de/by-2-0; credit "© BKG (Jahr des letzten Datenbezugs) dl-de/by-2-0, Datenquellen: ..." |
| Verified on | https://gdz.bkg.bund.de/index.php/default/verwaltungsgebiete-1-250-000-stand-01-01-vg250-01-01.html |
| Status | **VERIFIED** |
| Caveat | 1:250,000 is generalised. Fine for city membership of 100 m cells near the centre, but cells on city borders may be misassigned. The Zensus page also offers a municipal boundary shapefile at census day (15 May 2022, UTM32): https://www.destatis.de/static/DE/zensus/gitterdaten/Shapefile_Zensus2022.zip (dl-de/by-2-0) |

### 7c. City districts

| City | Dataset | Licence | Status |
|---|---|---|---|
| Bochum | "Bochum - Stadtgebiet - Stadtgliederung (komplett)": GeoPackage with 4 layers (Stadtgrenze, Stadtbezirke, Statistische Bezirke, Statistische Viertel), modified 2026-07-16. File: https://bochum.opendata.ruhr/dataset/ef58bb30-b681-4d70-ab1f-832e885c08c2/resource/418483ee-3f6d-4e06-8382-4c67e18dd3d6/download/stadtgliederung_bochum.gpkg | dl-zero-de/2.0 (dataset), cc-zero (resource) | **VERIFIED** (via opendata.ruhr API) |
| Dortmund | "Statistische Bezirke" (`fb62-statistischebezirke`, 62 records, modified 2026-10-30) on open-data.dortmund.de | Datenlizenz Deutschland Zero 2.0 | **VERIFIED** (via catalogue API) |
| Essen | not searched successfully | | **UNVERIFIED** |
| Duisburg | not searched successfully | | **UNVERIFIED** |
| Gelsenkirchen | not searched successfully | | **UNVERIFIED** |

---

## 8. Other socio-economic data

| Dataset | What we found | Licence | Verified on | Status |
|---|---|---|---|---|
| Dortmund small-area statistics | SGB II share of working-age population by **Stadtbezirk** (12 districts) for 2018 to 2022; unemployment in % by Stadtbezirk (2018, 2019, 2021...); population by sex and migration background in "Bezirken" 2023 (77 records, so probably statistical districts; 5-rounding for secrecy) | Datenlizenz Deutschland Namensnennung 2.0 | open-data.dortmund.de catalogue API | **VERIFIED** |
| Other four cities' small-area statistics | not checked | | | **UNVERIFIED** |
| Zensusdatenbank (ergebnisse.zensus2022.de) | Tables for Bund, Länder, Kreise, Gemeinden; has an API; **no grid cells**. Needs credentials or token for API (pystatis page) | not stated on page | https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Zensus2022/Datenbank/_inhalt.html | **PARTLY** |
| INKAR (BBSR) | Indicator atlas for Kreise and Gemeinden; R package `bonn` reads it (secondary source). Site refused automated access (certificate error). Latest edition seen in a citation: "Ausgabe 2024" | **UNVERIFIED** | https://www.inkar.de/ (not readable) | **UNVERIFIED** |
| BORIS NRW Bodenrichtwerte (standard land values) | Shape files for all NRW: current (`BRW_EPSG25832_Shape.zip`, 184 MB, updated 2026-11-02) and historical years 2011 to 2025 (about 150 to 220 MB each); data model PDF | **Datenlizenz Deutschland Zero 2.0** | https://www.opengeodata.nrw.de/produkte/infrastruktur_bauen_wohnen/boris/BRW/ (and `index.json`) | **VERIFIED** |
| OpenStreetMap, NRW extract (Geofabrik) | `nordrhein-westfalen-latest.osm.pbf` 874 MB (data to 2026-11-01); sub-regions Arnsberg 186 MB, Düsseldorf 207 MB, Münster 134 MB (the Ruhr spans these three) | ODbL 1.0 | https://download.geofabrik.de/europe/germany/nordrhein-westfalen.html | **VERIFIED** |

Caveats:
- Bodenrichtwerte are land values per zone (not rents) and reflect location value. Possible robustness covariate; zones do not match grid cells.
- District-level SGB II data can only be used at district level (ecological, very coarse). Not for the 100 m model; possibly a validation of the rent proxy (does low Zensus rent go with high SGB II share across districts?).
- OSM: useful for water bodies, parks, rail and industry masks, but completeness varies.

---

## (a) Recommended core datasets

1. **Zensus 2022 100 m grid, official Destatis CSVs** (dl-de/by-2-0): population, average net cold rent (plus the file with number of dwellings), share of foreigners, share 65+, share under 18, vacancy rate (version 05.02.2025), ownership rate, average household size, living space per resident, building age classes, heating type. Read with our own code; cross-check with R `z22` 1.1.4.
2. **Landsat 8 and 9 C2 L2 surface temperature** in GEE (`LANDSAT/LC08/C02/T1_L2`, `LANDSAT/LC09/C02/T1_L2`), summers 2018 to 2025, QA_PIXEL cloud, shadow, cirrus and dilated-cloud masking plus `ST_CDIST`, converted with × 0.00341802 + 149.0 then minus 273.15 for °C.
3. **Copernicus HRL Tree Cover Density 10 m** (year closest to 2022) and **HRL Imperviousness Density 10 m** (2021, and 2024 as a check), plus **Urban Atlas 2021** and **Street Tree Layer 2021**.
4. **Boundaries**: BKG VG250 (01.01.2026) or the Zensus 2022 municipal shapefile for city membership; RVR Verbandsgrenze (WFS) if the whole region is used; BKG GeoGitter or self-built cells from the cell IDs.
5. **Context and checks**: DWD hourly air temperature (Bochum 00555, Essen-Bredeney 01303, Duisburg-Baerl 13670) to select hot clear days; LANUK Klimaanalyse NRW 2026 day and night maps as an external comparison (and as related work to cite); ECOSTRESS 70 m as a time-of-day sensitivity analysis.

## (b) Open questions to check by hand (in Chrome)

1. Zensus: open the "Anteil unter 18", "Eigentümerquote", "Durchschnittliche Haushaltsgröße" and "Nettokaltmiete und Anzahl der Wohnungen" description files and note the exact column names and version dates.
2. Zensus secrecy: is there any hard minimum (persons or dwellings) below which a ratio is not published at 100 m? Look for the Destatis secrecy page (old link `zensus2022.de/DE/Zensusdatenbank/Geheimhaltung.html` redirects now) or the Destatis WISTA article "Geheimhaltung mit der Cell-Key-Methode im Zensus 2022" (https://ideas.repec.org/a/zbw/wistat/309502.html).
3. Zensus-Atlas: find its current address (old zensus2022.de links redirect to destatis.de).
4. Zensus 2011 grid files: licence, and whether they really are online (page says "in Kürze").
5. `z22`: does `z22_data()` keep the bracket flag, or drop it? Read the package source or ask by GitHub issue.
6. USGS Landsat 8-9 C2 L2 Science Product Guide (PDF): read the ST section (algorithm, accuracy, `ST_CDIST`, recommended QA use) and record its version number.
7. GEE: register the Cloud project as noncommercial, choose Community Tier, and check the EECU cost of one test export.
8. CLMS: confirm that login is EU Login; check which TCD years (2021 to 2024) are downloadable; check the licence page for HRL Imperviousness 2024.
9. Urban Atlas: list which FUAs cover Bochum, Dortmund, Essen, Duisburg, Gelsenkirchen (and the RVR area); check for gaps.
10. Open.NRW CKAN (`ckan.open.nrw.de`) was refusing connections: check the RVR boundary licence there ("non_open" flag claim) and the LANUK Klimaanalyse metadata on Geoportal.NRW.
11. City districts and small-area statistics for Essen, Duisburg, Gelsenkirchen (and Bochum SGB II by district).
12. INKAR (inkar.de): current edition and licence (site gave a certificate error to automated tools).
13. ECOSTRESS: count clear scenes over the Ruhr in June to August 2018 to 2025 by local hour (in GEE), and check whether Earthdata Login is needed outside GEE.
14. Sentinel-3 SLSTR: only if needed; read the CDSE product page.
15. Dortmund press release on the climate network (dortmund.de refused automated access) for the official start date.

## (c) Accounts Maria must create

| Account | Needed for | Required? |
|---|---|---|
| Google account plus a **Google Cloud project registered for noncommercial Earth Engine use** (Community Tier, no billing) | Landsat and ECOSTRESS in GEE | **Yes** (core) |
| **CLMS login (EU Login)** on land.copernicus.eu | Tree Cover Density, Imperviousness, Urban Atlas, Street Tree Layer downloads | **Yes** (core) |
| Copernicus Data Space Ecosystem account | Only if Urban Atlas or Sentinel-3 are taken from CDSE instead of the CLMS site | Optional (**UNVERIFIED** whether needed) |
| NASA Earthdata Login | Only for ECOSTRESS outside GEE | Optional |
| Zensus database API token | Only for municipal tables through the API (not for grid files) | Optional |
| USGS EarthExplorer account | Only for Landsat outside GEE | Optional (not checked) |

No account is needed for: Zensus grid CSVs, R `z22`, BKG grids and VG250, DWD CDC, OpenGeodata.NRW (Klimaanalyse, BORIS), Dortmund and Bochum open data, Geofabrik OSM.
