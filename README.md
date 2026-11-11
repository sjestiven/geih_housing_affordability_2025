# Housing affordability in Cali A.M. in 2025

This Capstone I research project examines how much of their income households in Cali–Yumbo spend on rent or home acquisition payments. It describes how housing payments, housing burden and remaining income vary by tenure and the education of the household head. The study combines twelve monthly cross-sections for 2025. The unit of analysis is the household-month, and the national reference covers the monetary poverty domain, including Cali A.M.

## Data and scope

The project combines the housing and general characteristics modules of the [DANE GEIH 2025](https://microdatos.dane.gov.co/index.php/catalog/853/get-microdata) with the household file from [DANE Monetary Poverty and Inequality 2025](https://microdatos.dane.gov.co/index.php/catalog/908/get-microdata). The linkage retains all GEIH households. The annual build contains **292,942 household-months** (10,150 in Cali A.M.) and **817,550 person-months**. The [build manifest](data/reference/geih_households_2025_manifest.json) records coverage, linkage checks and file fingerprints.

## Repository contents

| Location | Contents |
| --- | --- |
| [scripts/](scripts/README.md) | Annual GEIH build and validated linkage with the monetary poverty household file. |
| [config/](config/) | Project-relative paths and source archive member names. |
| [docs/](docs/) | [Source documentation](docs/data_sources.md) and [variable dictionary](docs/variable_dictionary.csv). |
| [data/reference/](data/reference/README.md) | Source coverage benchmark and build manifest. |

## Reproducibility

The build uses Python 3.12 and [requirements.txt](requirements.txt). Its inputs are the twelve original monthly GEIH ZIPs in `data/raw/geih/` and `BDatos-Pobreza_Monetaria_Desigualdad-2025.zip` in `data/raw/monetary_poverty/`. The [source documentation](docs/data_sources.md) describes the original modules and linkage keys. The [source configuration](config/data_sources.json) points to the project's local archives.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/build_household_data.py
```

| Generated file in `data/processed/` | Unit and contents |
| --- | --- |
| `geih_poverty_households_2025.parquet` | One row per household-month. Housing and household-head characteristics linked to official income and other monetary poverty fields. |
| `geih_persons_housing_2025.parquet` | One row per person-month. Person characteristics linked to the housing module for household composition and profiling. |
| `geih_households_2025.parquet` | One row per household-month. Housing and household-head characteristics before the poverty linkage. |

The source ZIPs and row-level datasets stay local and are excluded by [.gitignore](.gitignore). The build reads the archives directly and writes the processed datasets and validation manifest within this project. Academic documents, literature and descriptive results are managed in the adjacent Research Materials folder in the local workspace.
