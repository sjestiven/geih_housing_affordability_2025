# Python work plan

The annual GEIH household and person builds and the official poverty linkage are implemented. Use the following stages to extend the analysis.

| Stage | Planned script | Observable completion evidence |
| --- | --- | --- |
| 1–2 | scripts/build_household_data.py | Annual GEIH household master, household left join with poverty and full person-level GEIH with housing. Verifies source fingerprints, keys, heads, resident counts and matched poverty fields. Cali is identified by AREA 76. |
| 3 | scripts/explore_household_data.py | Coverage and missingness by tenure/month; income and payment distributions; zero income; negative residuals; age/education cell counts and flagged anomalies. |
| 4 | scripts/analyze_housing_burden.py | Weighted medians/Q1/Q3; threshold shares; household and resident counts; explicitly separate national coverage and zero-income subgroup. |

Use `data/processed/geih_poverty_households_2025.parquet` for official income and household-level analyses. Derive household composition from `data/processed/geih_persons_housing_2025.parquet`. Stage 3 creates the analytical eligibility flags. Store row-level analytical subsets and audits in `data/processed/analysis/`, separately from the annual files.

Stage 4 writes the aggregate `coverage.csv`, `payment_summary.csv`, `burden_summary.csv`, `residual_summary.csv` and `negative_residual_summary.csv` to `outputs/tables/`. Review each summary before adding it to Git, following the [output guidelines](../outputs/README.md). One independent figure per question or indicator belongs in `outputs/figures/`. Figures and prose must identify the same definition, denominator, geography and data release.

Use the annual master as the input to exploration. Record changes to estimands or exclusion rules in `docs/decision_log.md`.

## Verification targets

data/reference/official_income_benchmark.csv contains aggregate independent starting checks for the adopted official-income definition. data/reference/source_coverage_benchmark.csv contains coverage checks. They are not frozen truths: investigate differences caused by releases, source changes, or explicit new rules rather than forcing agreement.

Priority checks include 10,150 Cali housing household-month records, full Cali poverty linkage, 58 Cali household/expense-unit size differences, and 5,758 positive-income payment-eligible Cali records. The reference above 40% is approximately 21.27% for that eligibility definition; 36.18% above 30% remains a historical sensitivity. Independent overview verification identified 46 zero-income household-months with valid payments in Cali; their residuals are computable separately and their burden is undefined. These checks must still be reproduced by the production pipeline.

The 2026-10-27 overview verification adds `overview_population_benchmark.csv`, `overview_distribution_benchmark.csv`, `overview_cdf_benchmark.csv` and `overview_benchmark_provenance.json` under `data/reference/`. They distinguish sample from represented population, all-tenure income from payment-eligible income, total residual from per-member residual, and unweighted from weighted medians. They were checked directly against immutable source ZIPs and reconciled with the earlier eligible counts, weights and threshold shares.

## Decisions to close after exploratory analysis

- Head-age bands and age-composition cutoffs; report whether counts refer to all residents or only expenditure-unit members.
- Whether any sparse subgroup can be displayed with adequate precision.
- Available survey-design information for confidence intervals and uncertainty.
- Exact cross-country comparison pairings under matched definitions.

The main current design is descriptive burden analysis with residual income as a supplementary accounting indicator. A causal or welfare-sufficiency project requires a distinct research design.
