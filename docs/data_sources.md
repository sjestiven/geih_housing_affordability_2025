# Data sources and local access

Main GEIH release: https://microdatos.dane.gov.co/index.php/catalog/853

Official monetary-poverty release: https://microdatos.dane.gov.co/index.php/catalog/908

Read only these monthly GEIH CSV members for the principal workflow:

- CSV/Datos del hogar y la vivienda.CSV
- CSV/Características generales, seguridad social en salud y educación.CSV

Read Hogares/Hogares.csv from BDatos-Pobreza_Monetaria_Desigualdad-2025.zip. Personas/Personas.csv is an optional official-income audit input. CSV and SAV can represent the same release; CSV is selected for readable imports. Read identifiers as strings first; apply explicit numeric conversion to amounts and counts. The inspected GEIH CSVs use semicolons and the poverty CSV uses commas. Validate encoding on the actual files rather than assuming all ZIP member names and file contents share an encoding.

Place the twelve original monthly ZIPs in `data/raw/geih/` and the original poverty ZIP in `data/raw/monetary_poverty/`. The build reads the ZIP members directly. Use `config/data_sources.local.json` for a local path override. Relative paths resolve from the repository root.

`scripts/build_household_data.py` expects the twelve Spanish month names followed by `2025.zip`. It saves `data/processed/geih_households_2025.parquet` with all housing columns, the head's original `ORDEN`, `P6050`, `P6040`, `P3042`, `P3271` and `P3039`, and the derived `resident_count`. It stores one row per `PER`, `MES`, `DIRECTORIO`, `SECUENCIA_P` and `HOGAR`. Identifiers remain text, including leading zeros in GEIH month codes. Core amount, weight and demographic fields are numeric. The remaining housing fields retain source codes as text.

The build also saves `geih_poverty_households_2025.parquet` by left-joining the GEIH household master to `Hogares/Hogares.csv`. It normalizes `MES` and `mes` on join copies, then verifies uniqueness on both sides of the shared month, directory and sequence key. The saved identifiers are the original GEIH household key. Matched rows are checked against poverty tenure, resident count and Cali domain. Official `ingtotug`, `fex_c`, `nper` and `npersug` retain their source definitions. For fields with a case-insensitive name collision, the poverty field receives the `poverty_` prefix. `poverty_match_status` records `matched` or `unmatched`. Unmatched rows retain their GEIH fields, with missing poverty values.

`geih_persons_housing_2025.parquet` keeps all columns from the two GEIH modules at the person-month level. Its key is `PER + MES + DIRECTORIO + SECUENCIA_P + HOGAR + ORDEN`. Housing columns repeat for each person in the household. Shared identifiers appear once, and the person-side version of other shared fields receives the `person_` prefix. For example, `FEX_C18` is the housing value and `person_fex_c18` is the person-module value. Field aliases are listed in the build manifest. Aggregate household composition to the household key before attaching it to the linked household dataset or computing household statistics.

The main statistical-method reference is DANE (2025), Metodología estadísticas medidas de pobreza EMP, code DSO-EMP-MET-001, version 2, June 2025. It explains income sources, expenditure units, validation and imputation. The current 2025 dictionary identifies the actual released variable names. Neither is replaced by a historical 2002–2010 algorithm merely because that file appears in the catalog.

Published official household fields include ingtotug, ingtotarr, ingpcug, nper, npersug, fex_c and geographic domain. Keep their original names and map derived variables explicitly. Do not re-sum occupational modules into ingtotug.

National housing counts exceed matched poverty counts. Store unmatched records and audit domains; official-income results use the covered monetary-poverty universe. Country labels must state this restriction and that Cali is included.
