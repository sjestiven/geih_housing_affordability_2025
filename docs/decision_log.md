# Current decisions

Version 1.1 — 2026-10-27. This log starts with the current design and records changes prospectively. It does not reproduce previous project histories.

| ID | Decision | Status |
| --- | --- | --- |
| D01 | Use official ingtotug as current expenditure-unit income before rental imputation. | Adopted by the user |
| D02 | Use GEIH housing and general characteristics plus official poverty households for the principal data build. | Current implementation specification |
| D03 | Keep one household-month observation; twelve cuts are not a panel. Preserve original identifiers and validate joins. | Retained |
| D04 | Compare four tenure groups and four head-education groups, retaining detailed source codes. | Retained |
| D05 | Keep effective rent/acquisition payment separate from estimated housing-service value; no observed utility amounts are available. | Retained |
| D06 | Use fex_c once as an annualized weight for the official-income matched domain. | Current implementation specification |
| D07 | Use weighted median and Q1/Q3, with proportions and represented household/person counts. | Retained |
| D08 | Describe continuous burden with weighted median and Q1/Q3. Replace 30% with the OECD HC1.2 >40% reference for narrow housing payments; retain 30% only as historical sensitivity, plus 50% and >100%. Neither the convention nor the sample median identifies needs adequacy. | Revised 2026-10-27 following the user's request to select a documented alternative |
| D09 | Use npersug for residual resources per unit member; preserve nper for all-resident counts. State household-payment allocation assumption. | Current implementation specification |
| D10 | Retain valid extremes and negative residuals; do not trim or winsorize the main analysis. | Retained |
| D11 | Keep known zero-income residuals separate from positive-income burden; never replace unmatched/missing income with zero. | Current implementation specification |
| D12 | Keep burden as the principal descriptive result and residual as a supplement; do not infer welfare sufficiency or causality. | Working analysis design |
| D13 | Add age/composition after EDA establishes coverage and cell sizes; age groups are not yet chosen. | Pending definition |
| D14 | Use nominal monthly COP and document reference periods. No automatic monthly deflation is implemented. | Working analysis design |
| D15 | Compare other countries only after aligning cost, income, populations, years, tenure and units. | Retained |
| D16 | Write Python together by stages. No analysis pipeline or environment is created in this initialization. | Confirmed by the user |
| D17 | Preserve all reading-card contents and authorship. Library copies are byte-checked against originals. | Retained |
| D18 | Distinguish observed household-month/resident counts from expanded period-average household/resident estimates for every analysis universe. Compare weighted and unweighted medians, without calling expansion a census. | Clarified 2026-10-27; independent overview aggregates checked |
| D19 | Report household total residual as well as residual per expenditure-unit member. Use the same payment-eligible universe when comparing income with residual; show the all-tenure income median separately. | Clarified 2026-10-27; independent overview aggregates checked |

The >40% reference follows OECD (2025), HC1.2 Housing costs over income, including its narrow cost definition and documented income exceptions. It improves external anchoring but remains a convention. Technical settings and the overview were aligned; older dated policy briefs retain their original threshold-specific calculations.

For a new entry record the concrete decision, reason, affected variable/output, source, status and validation needed. Do not mark a proposal implemented before code and outputs are checked.
