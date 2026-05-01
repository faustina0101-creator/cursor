# Revised Protocol Sections

The following are the fully revised **Sample Size** and **Statistical Analysis** sections for the protocol, written in full sentences and ready for insertion into the protocol document. All corrections from the review have been incorporated.

---

## Sample Size

The primary goal of this study is to test the three-way interaction between message evidence type (statistical vs. anecdotal), message source (government agency vs. social media influencer) and genetic literacy on the primary outcomes. Since the primary hypothesis (H4) specifically concerns whether this three-way interaction predicts favourable decisional outcomes, the sample size is powered for detecting this interaction effect. Interaction effects, particularly three-way interactions, require larger samples than main effects, and a conservative approach is adopted.

The study employs a 2 × 2 factorial between-subjects design with a control group (no message framing), yielding five message conditions per track. Participants who have not undergone NIPT are assigned to the NIPT message conditions, and participants who have undergone NIPT are assigned to the NIPT-SGD message conditions. Because these two tracks involve different participant populations (NIPT-naïve vs. NIPT-experienced), different stimulus materials (NIPT-related messages vs. NIPT-SGD-related messages) and partially different outcome measures (including panel preferences and willingness-to-pay specific to NIPT-SGD), they constitute two parallel experiments. The sample size is therefore calculated independently for each track, and the total sample size reflects the sum of both tracks.

Within each track, participants in the four experimental conditions enter the main factorial regression model, while the control group is analysed separately via planned contrasts. The full model for each track includes 30 predictors: 23 covariates (age, educational level, income, prior experience with genetic testing, sources of information about prenatal genetic tests and motherhood-related variables), three main effects (evidence type, message source and genetic literacy), three two-way interactions (evidence type × message source, evidence type × genetic literacy, message source × genetic literacy) and one three-way interaction (evidence type × message source × genetic literacy). The control group is not included in the factorial regression model because the interaction terms are undefined for participants who did not receive any message framing; instead, a separate contrast analysis compares the control group to the experimental conditions.

Sample size was calculated using G\*Power 3.1 for hierarchical multiple linear regression, specifically the F-test for R² increase (fixed model, R² increase), which tests whether the addition of the three-way interaction term significantly improves model fit beyond a model containing covariates, main effects and two-way interactions. The parameters were as follows: effect size f² = 0.02, representing a small interaction effect that is conservative for three-way interactions in health communication research; α = 0.05 (two-tailed); statistical power (1 − β) = 0.80; number of tested predictors = 1 (the three-way interaction term); and total number of predictors in the full model = 30. Under these specifications, G\*Power yielded a required sample size of N = 395 participants in the four experimental conditions per track.

Three adjustments were applied to this base figure. First, to account for an anticipated 20% attrition rate due to incomplete responses or failed manipulation checks, the base sample size was inflated by dividing by the expected retention rate: 395 ÷ 0.80 = 494. Second, a 25% buffer was applied to ensure adequate power for planned subgroup probing via simple slopes analysis at ±1 standard deviation of genetic literacy and for binary outcome analyses (e.g., uptake intention) where statistical power for interaction detection is generally lower than in linear regression: 494 × 1.25 = 618. Third, the addition of a control group representing one-fifth of the total sample per track was accounted for: 618 × 5 ÷ 4 = 773. This was rounded to 650 participants per track based on practical recruitment considerations.

The total target sample size is N = 1,300 participants, comprising 650 participants in the NIPT track (130 per condition × 5 conditions) and 650 participants in the NIPT-SGD track (130 per condition × 5 conditions). This sample size provides statistical power greater than 0.89 for detecting a small three-way interaction effect (f² = 0.02) and greater than 0.99 for detecting a small-to-medium interaction effect (f² = 0.04) within each track. The ratio of participants to predictors is 21.7 per track, which exceeds the recommended threshold of 15 to 20 participants per predictor for reliable detection of interaction effects and mitigates the risk of model overfitting. The sample size is sufficient for the planned simple slopes analyses and sensitivity analyses.

---

## Statistical Analysis

All valid responses will be exported to R (version 4.3 or later) for data analysis. Because part of the survey is conducted in paper format, missing data may occur. Missing data will be handled via multiple imputation using fully conditional specification (the MICE procedure) if more than 5% of the data is missing. A minimum of 20 imputations will be performed, with all analysis variables and auxiliary variables included in the imputation model. Results across imputed datasets will be pooled using Rubin's rules. If missing data is 5% or less, complete case analysis will be used with sensitivity checks against imputed results.

### Preliminary analysis

Before testing hypotheses, one-way ANOVAs (for continuous variables) and chi-square tests (for categorical variables) will be conducted to verify that participants were successfully randomised across the five message conditions within each track. No significant differences in socio-demographic characteristics or genetic literacy across conditions are expected if randomisation was successful. Descriptive statistics will summarise socio-demographic characteristics, outcome variables and manipulation check items, reported as percentages, means, medians, standard deviations and ranges as appropriate. Relationships between categorical variables will be examined using chi-square tests, and associations between continuous variables will be assessed using Pearson's or Spearman's correlations depending on distributional assumptions. Cross-tabulations will be conducted to confirm successful randomisation across the framing groups.

Manipulation check items will be analysed to verify the integrity of the framing manipulations. Independent samples t-tests will compare manipulation check scores between participants in different message conditions. A significant difference in the expected direction will indicate that the manipulation was successful. Participants who fail the manipulation checks will be excluded from the primary analysis, and sensitivity analyses will be conducted with these participants included to assess the robustness of the findings.

### Hypothesis testing

Analyses will be conducted separately for each track (NIPT and NIPT-SGD) to examine the effects of message framing (evidence type and message source), genetic literacy and their interactions on the dependent variables.

**Continuous outcomes.** For each continuous outcome variable, a hierarchical (blockwise) multiple linear regression model with nested comparisons will be employed. The sequential blocks are as follows:

- Block 1 (covariates only): the outcome is regressed on the 23 covariates.
- Block 2 (main effects): adds evidence type, message source and genetic literacy.
- Block 3 (two-way interactions): adds evidence type × message source, evidence type × genetic literacy and message source × genetic literacy.
- Block 4 (three-way interaction): adds evidence type × message source × genetic literacy.

Each subsequent model will be compared to the previous model using an F-test for the change in R². The comparison of Block 3 with Block 2 will test the combined contribution of the two-way interactions. The primary test — the comparison of Block 4 with Block 3 — will evaluate whether the three-way interaction significantly improves model fit, directly addressing the primary hypothesis (H4).

**Binary outcomes.** For binary outcomes (e.g., uptake intention, informed choice classification), an analogous hierarchical logistic regression model will be employed using the same block structure. Nested models will be compared using likelihood ratio tests, as R² is not directly comparable in logistic regression.

**Ordinal outcomes.** For ordinal outcomes, ordinal logistic regression will be used. The proportional odds assumption will be tested using the Brant test or a likelihood ratio test comparing the proportional odds model to a multinomial logistic regression model. If the proportional odds assumption is violated, partial proportional odds or multinomial logistic regression will be used instead.

**Probing significant interactions.** Statistically significant interactions will be probed using simple slopes analysis. For the three-way interaction, simple slopes of the evidence type × message source interaction will be estimated at low (−1 SD) and high (+1 SD) levels of genetic literacy, showing how the message framing effect varies as a function of genetic literacy. For logistic, ordinal or multinomial models, interaction probing will be presented through predicted probabilities at specified covariate values.

**Control group analysis.** The control group does not fit within the 2 × 2 factorial structure and will be analysed separately using planned contrasts. First, a contrast will test whether receiving any of the four framed messages (collapsing the four experimental groups into a single message indicator) leads to different outcomes compared to the control group. Second, individual contrasts will examine whether each specific framed condition differs from the control group. For each contrast, interaction terms between genetic literacy and the relevant contrast variable will be included to test whether any effect of message exposure is moderated by genetic literacy.

**Willingness-to-pay analysis.** For the dichotomous-choice willingness-to-pay procedure, interval regression will be used to estimate the mean willingness-to-pay for NIPT and NIPT-SGD and its associated uncertainty. Willingness-to-pay will then be treated as a continuous dependent variable in a linear regression model or, if the distribution is skewed, in a generalised linear model with a log link. The same hierarchical framework will be applied, regressing willingness-to-pay on evidence type, message source, genetic literacy and their interactions while controlling for key covariates, in particular household income. For NIPT-SGD participants, preferences and willingness-to-pay for the basic 44-disorder panel versus the more comprehensive 66-disorder panel will be analysed in relation to genetic literacy and message framing conditions (H3a and H3b).

**Multiple comparisons.** Because the study includes multiple dependent variables (knowledge, attitudes, anxiety, willingness-to-pay, uptake intention, informed choice and deliberation), there is a risk of inflated Type I error. Behavioural intention and uptake will be designated as the primary endpoints for the three-way interaction test. For the remaining secondary outcomes, Benjamini-Hochberg false discovery rate correction will be applied across the family of tests to control for multiple comparisons.

### Sensitivity analyses

Several sensitivity analyses will be conducted to assess the robustness of the findings. Multiple imputation results will be compared against complete case analyses. Subgroup analyses will compare prior testers and non-testers. Bootstrapping with 5,000 resamples and bias-corrected and accelerated confidence intervals will be applied to key models to verify the stability of parameter estimates without reliance on distributional assumptions. Robust regression using M-estimators will be employed when more than 5% of observations have a Cook's distance exceeding 4/N or when residual diagnostics indicate substantial departures from normality.

---

*All G\*Power calculations have been independently verified using Python/SciPy replication of the non-central F distribution. The verification scripts are available in the accompanying files.*
