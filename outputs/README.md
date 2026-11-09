# Generated research outputs

- `data/processed/analysis/` is for local household- or person-level analytical subsets, derived indicators and row-level audits. Create it when the first export needs it. Git ignores these files.
- `outputs/tables/` is for grouped summaries, such as counts, weighted proportions and quantiles. Git ignores new tables by default. Review the contents for grouped statistics and the absence of record identifiers before adding a specific table, for example `git add -f -- outputs/tables/burden_summary.csv` from the repository root.
- `outputs/figures/` is for aggregate charts. `outputs/validation/` is for local build and validation reports.

Independent verification targets and their provenance are in [data/reference/](../data/reference/README.md).
