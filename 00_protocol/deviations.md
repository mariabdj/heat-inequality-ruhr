# Deviations from the preregistration

Every change to the registered plan is written here, with the date, what changed, why, and whether the result of the changed analysis had been seen. Nothing yet.

## D1. 2026-11-02: population column name (Step 2)
- **Registered text (Q5):** population value column `Bevoelkerungszahl`, as written in the official description file `datensatzbeschreibung_bevoelkerungszahlen.xlsx` (Version 2, 30.09.2024).
- **What the data file contains:** the header of `Zensus2022_Bevoelkerungszahl_100m-Gitter.csv` is `GITTER_ID_100m;x_mp_100m;y_mp_100m;Einwohner`. The value column is called `Einwohner` (inhabitants), and there is no flag column.
- **Change:** we use `Einwohner` as the population value. Same variable (number of inhabitants per cell), only the name differs between the description file and the data file.
- **Result seen before the change?** No. Only the header was read; the change does not depend on any value.
- **Effect on the analysis:** none.
