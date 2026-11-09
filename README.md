# Housing affordability in Cali A.M. in 2025

This Capstone I research project examines how much of their income households in Cali–Yumbo spend on rent or home acquisition payments. It describes how housing payments, housing burden and remaining income vary by tenure and the education of the household head. The study combines twelve monthly cross-sections for 2025. The unit of analysis is the household-month, and the national reference covers the monetary poverty domain, including Cali A.M.

## Data and scope

The project combines the housing and general characteristics modules of the [DANE GEIH 2025](https://microdatos.dane.gov.co/index.php/catalog/853/get-microdata) with the household file from [DANE Monetary Poverty and Inequality 2025](https://microdatos.dane.gov.co/index.php/catalog/908/get-microdata). The linkage retains all GEIH households. The annual build contains **292,942 household-months** (10,150 in Cali A.M.) and **817,550 person-months**. The [build manifest](data/reference/geih_households_2025_manifest.json) records coverage, linkage checks and file fingerprints.

The main burden indicator divides the reported monthly rent or acquisition installment by `ingtotug`, the official current income of the expenditure unit before rental imputation. It is estimated for renters and owners still paying for their homes with valid payment data and positive income. Tenure and income profiles cover all four tenure groups. Residual income measures the resources remaining after the recorded housing payment and is reported both in total and per expenditure-unit member.

The analysis plan specifies weighted medians and quartiles for the burden distribution and the OECD HC1.2 threshold of over 40% as a reference. The payment measure covers rent or acquisition installments, with separate utility, maintenance and tax amounts outside its scope. The [methodology](docs/methodology.md) documents eligibility, expansion weights, negative residuals and the limits of the descriptive design.

## Repository contents

| Location | Contents |
| --- | --- |
| [scripts/](scripts/README.md) | Implemented annual GEIH build and validated linkage with the monetary poverty household file. |
| [config/](config/) | Analysis settings and a source-path configuration example. |
| [docs/](docs/) | [Methodology](docs/methodology.md), [variable dictionary](docs/variable_dictionary.csv), [decision log](docs/decision_log.md) and [analysis plan](docs/analysis_plan.md). |
| [data/reference/](data/reference/README.md) | Aggregate benchmarks, source coverage and build fingerprints. |
| [references/](references/README.md) | Bibliography, evidence matrix and reference registers. |
| [outputs/](outputs/README.md) | Locations for aggregate tables, figures and local validation reports. |

The data build is implemented. Household profiling and the production analysis of burden and residual income are planned in the [analysis plan](docs/analysis_plan.md). The aggregate benchmarks are available for verification.

## Reproducibility

The build uses Python 3.12 and [requirements.txt](requirements.txt). Its inputs are the twelve original monthly GEIH ZIPs in `data/raw/geih/` and `BDatos-Pobreza_Monetaria_Desigualdad-2025.zip` in `data/raw/monetary_poverty/`. The [source documentation](docs/data_sources.md) describes the original modules and linkage keys. [The configuration example](config/data_sources.example.json) defines the default paths.

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

The source ZIPs and row-level datasets are local files excluded by [.gitignore](.gitignore). Row-level analytical exports belong in `data/processed/analysis/`. Reviewed aggregate summaries belong in `outputs/tables/`. See the [output guidelines](outputs/README.md).
