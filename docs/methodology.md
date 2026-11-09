# Current methodological specification

Version 1.1 — 2026-10-27. The annual GEIH datasets and the official poverty linkage are implemented. This specification also covers the subsequent burden analysis.

## Question and estimand

Describe the distribution of effective housing payments relative to current expenditure-unit income among Cali–Yumbo households in 2025, comparing tenure groups and household-head education. The principal estimand is a survey-weighted distribution of household ratios, not the ratio of aggregate payments to aggregate income. Retain a covered-country reference including Cali.

## Sources and observation

Combine monthly GEIH housing and general-characteristics modules with the annual DANE Monetary Poverty and Inequality 2025 household file. Poverty measurement is a statistical operation based on GEIH with an official income-processing methodology; it is not an independent interview survey of unrelated households.

The observation is a household-month. Preserve year, month, DIRECTORIO, SECUENCIA_P and HOGAR in GEIH; add ORDEN for persons. Poverty has directorio, secuencia_p and mes. A crosswalk must prove the reduced shared key is unique in each file, preserve HOGAR from GEIH and check identity through tenure, resident count and domain. Never silently drop a key component or use an unchecked many-to-many merge.

Keep all housing records in a master with match flags. Income-based national estimates use matched poverty coverage; report unmatched records by geography. Do not set unmatched income to zero or substitute a different income definition for them. Twelve cuts do not establish a panel.

## Official income and statistical units

`household_income = ingtotug`: total current income of the expenditure unit before imputing the owner/usufruct dwelling's rental service. Do not use ingtotarr or ingpcug as direct replacements and do not add personal income components on top of this aggregate.

Income can contain in-kind resources and statistical imputations of missing income. Rental imputation and income-response imputation are different. The aggregate is not certified liquid cash, income received entirely in one calendar month, or post-tax disposable income. Use the official 2025 dictionary together with DANE's poverty methodology; historical algorithms linked in the catalog are not automatically a literal recipe for the 2025 release.

`household_size = nper`, reconciled with the number of GEIH resident records and P6008 if available. `expenditure_unit_size = npersug`; do not force equality. The expenditure unit excludes domestic service and relatives, pensionistas, and other resident workers under DANE's membership rules. Pensionista does not mean a retired member receiving a pension.

## Housing payment and rental-service valuation

For P5090=2, use P5100, the reported acquisition installment including principal and interest. For P5090=3, use P5140, the reported rental measure. Interpret anticresis and other questionnaire-specific cases using the manual rather than assuming every response is a conventional cash rent.

For fully paid owners and other tenures, keep effective_payment unavailable for the principal comparable burden/residual analysis. Absence of rent or mortgage does not imply zero total housing cost. Retain all four groups for tenure and income characterization.

P5130 may support a separately labeled rental-equivalent or service-value analysis. It must not be deducted as a cash payment. Payment coverage excludes separately observed monetary amounts for utilities, administration, maintenance and property taxes. Availability of utilities is not an expenditure amount.

## Indicators

Let Y_h=ingtotug, G_h=observed rent/installment, u_h=npersug and w_h=fex_c.

$$B_h=100G_h/Y_h$$

Burden requires matched income, Y_h>0, known tenure 2 or 3 and a valid nonnegative payment. A genuine zero payment remains flagged for review, not automatically deleted. Describe the continuous distribution primarily through weighted median and Q1/Q3. Use >40% as the institutional reference from OECD HC1.2 for a narrow rent/acquisition-payment definition; <=40% is its complement. Retain >30% only for historical sensitivity, plus >50% and >100%. This operational convention is not a universal welfare threshold, and a sample median must not become an adequacy cutoff. Nested groups must not be added. International comparability still requires reconciling income and other definitions.

$$R_h=Y_h-G_h$$

$$R_h^{pc}=R_h/u_h$$

Report total household residual and per-expenditure-unit-member residual separately. Compare their medians with income over the same eligible population; the difference between two medians is not generally the median of within-household differences. Report all-tenure income medians separately from payment-eligible medians, with known zero incomes retained in the all-tenure income distribution.

The main residual comparison uses the same positive-income population as burden. Known zero-income units with a valid payment and positive u_h may have a computable residual but no finite burden; report them separately. Unknown income yields an unknown residual. Preserve valid negative residuals and display them explicitly without an editorial materiality cutoff.

Residuals use the expenditure-unit denominator and assume that unit bears the recorded household payment. Payments shared with residents outside the unit are an allocation limitation. The result is remaining current resources per unit member, not a sufficiency or unspent-cash measure.

$$S_t=100\frac{\sum_h w_h I(B_h>t)}{\sum_h w_h}$$

Weights apply over the eligible population in each statistic. fex_c is annualized: sum once, without dividing by twelve. Household counts sum w_h; full residents sum w_h*nper; expenditure-unit members sum w_h*npersug. Do not multiply each household's income or payment by its weight before forming its ratio. Retain FEX_C18 for reconciliation only unless an explicitly separate universe requires it.

Use weighted median and Q1/Q3. A weighted inverse-CDF convention must be documented when coded. Q1/Q3 describe dispersion, not confidence intervals. Survey expansion does not create a census; do not claim significance from point differences. Survey-design-based uncertainty requires appropriate design information and a separate implementation.

## Stratification and period

Retain four analytical tenure groups while preserving all seven source codes. The head is P6050=1 and must be unique. Education from P3042 uses codes 1–3, 4–7, 8–10, 11–13. These represent highest level reached, not necessarily a completed diploma. Unknown education remains missing.

Head age P6040 and resident/expense-unit age composition are planned extensions. Keep exact ages initially, including valid heads under 18. Age bands and dependent-member cutoffs are not yet set. Distinguish sex at birth P3271 and gender identity P3039; they are not substitutes. Sparse cells need sample and uncertainty checks, not an automatic claim of reliability above an arbitrary count.

Amounts are nominal monthly COP. Annual reference components already handled in official income are not divided by twelve a second time. Do not sum income across months as if following the same household. International comparisons require aligned income, cost coverage, tenure, denominator, year and threshold; adopting 40% alone is insufficient.

## Missingness, anomalies and scope

Preserve original responses. Apply 98/99 to the documented payment/rental questions only, with reason flags. Do not apply raw-response codes to ingtotug or numeric fields such as age or geography. Investigate other extreme/sentinel-like values against the questionnaire; do not declare a universal 999... rule without question-specific evidence.

Keep valid extremes. Do not trim or winsorize the main distribution. Duplicate keys or inconsistent joins stop processing; economically unusual but internally consistent responses are reviewed and retained with flags. A source match confirms processing provenance, not respondent truth.

The project supports descriptive diagnosis and evaluation priorities. It does not identify causal effects, optimal subsidies, free tenure preferences, total housing expenditure, or Stone-style residual-income adequacy without a local needs budget.
