# Comprehensive Review: Sample Size Calculation and Statistical Analysis Plan

## Overview

This review thoroughly examines the methods section of the protocol, focusing on the sample size calculation and the statistical analysis plan. It compares the **original protocol version** (N=1,416) against the **revised version** produced by another AI (N=900), computationally verifying every G\*Power claim using independent Python/SciPy replication of the non-central F distribution.

All computations in this review are independently reproduced in the accompanying scripts (`sample_size_verification.py` and `verify_gpower_detailed.py`).

---

## 1. Predictor Count Verification

Both versions agree on 31 total predictors. This count is **correct**:

| Component | Count | Details |
|---|---|---|
| Main effects | 3 | Evidence type (1 dummy), Message source (1 dummy), Genetic literacy (continuous) |
| Two-way interactions | 3 | E×M, E×L, M×L |
| Three-way interaction | 1 | E×M×L |
| Covariates | 23 | Socio-demographics, prior testing, info sources, motherhood |
| Control group indicator | 1 | Dummy-coded (0 = experimental, 1 = control) |
| **Total** | **31** | |

**Verdict: k = 31 is correct.**

However, see Issue 5 below regarding whether the control group dummy should actually be in the main interaction model.

---

## 2. G\*Power Computation Verification

### 2.1 Original Version Claims: N = 295

The original states: *"f² = 0.05, alpha = 0.05, power = 0.80 ... the sample size computed a priori for the five groups where joint contribution of multiple interaction terms is to be detected, would be n=295"*

**Independent verification result: N = 295 CANNOT be reproduced with the stated parameters and k = 31.**

Using G\*Power's "Linear multiple regression: Fixed model, R² increase" with k = 31:
- df_tested = 1 (three-way interaction only): **N = 160** (not 295)
- df_tested = 4 (all interaction terms): **N = 245** (not 295)

**What actually produces N = 295:** Through systematic search, N = 295 is recovered when using:
- G\*Power test: **"R² deviation from zero"** (overall model F-test), **not** "R² increase"
- **k = 7** (only the 7 factorial terms: 3 main + 3 two-way + 1 three-way)
- f² = 0.05, alpha = 0.05, power = 0.80

This means the original calculation:
1. **Used the wrong G\*Power test** — "R² deviation from zero" tests whether the *entire model* explains significant variance, not whether a specific predictor (the three-way interaction) adds significant explanatory power
2. **Excluded the 23 covariates and control dummy from k** — despite stating they are in the model
3. The original wording "joint contribution of multiple interaction terms" is consistent with this interpretation (testing all 7 factorial terms together), but this does NOT match the study's primary hypothesis (H4), which specifically concerns the three-way interaction

### 2.2 Revised Version Claims: N = 549

The revised version states: *"G\*Power test: Linear multiple regression (fixed model, R² increase), Number of tested predictors = 1, Total predictors = 31, f² = 0.04 → N = 549"*

**Independent verification result: N = 549 CANNOT be reproduced with the stated parameters.**

Using G\*Power's "R² increase" with df_tested = 1, k = 31, f² = 0.04:
- **Correct answer: N = 199** (not 549)
- Power at N = 549 with these parameters: 0.997 (massively overpowered)

**What actually produces N ≈ 549:** Through systematic search, N = 551 is recovered when using:
- G\*Power test: **"R² deviation from zero"** (same error as the original)
- **k = 21**, f² = 0.04

The revised version also claims f² = 0.05 → N = 393 and f² = 0.08 → N = 267. Neither of these match the stated test configuration:
- f² = 0.05, df_tested = 1, k = 31 → **correct N = 160** (not 393)
- f² = 0.08, df_tested = 1, k = 31 → **correct N = 101** (not 267)

These values appear to come from "R² deviation from zero" with different k values.

### 2.3 Summary of G\*Power Errors

| Version | Claimed Test | Actual Test Used | Claimed k | Actual k | Claimed N | Correct N |
|---|---|---|---|---|---|---|
| Original | R² increase (implied) | R² deviation from zero | 31 | 7 | 295 | 160–245 |
| Revised | R² increase | R² deviation from zero (likely) | 31 | ~21 | 549 | 199 |

**Both versions appear to have used the wrong G\*Power test.** The "R² deviation from zero" tests whether the overall model explains any variance. The correct test for the three-way interaction is "R² increase" which tests whether adding the three-way interaction term significantly improves model fit beyond the model with covariates, main effects, and two-way interactions.

### 2.4 Correct G\*Power Calculation

Using the correct test — **"Linear multiple regression: Fixed model, R² increase"** — with df_tested = 1 (three-way interaction), k_total = 31:

| f² | Required N | Critical F | Power |
|---|---|---|---|
| 0.02 (small) | 395 | 3.867 | 0.801 |
| 0.03 | 264 | 3.882 | 0.800 |
| **0.04 (small-to-medium)** | **199** | **3.898** | **0.801** |
| 0.05 | 160 | 3.915 | 0.802 |
| 0.08 (medium) | 101 | 3.980 | 0.800 |

---

## 3. Review of Adjustment Factors

### 3.1 Attrition Adjustment

**Original:** 590 × 1.20 = 708

**Revised:** 549 × 1.25 = 686

**Assessment:** To account for 20% attrition, the correct formula is:

> N_adjusted = N_needed / (1 − attrition_rate) = N_needed / 0.80 = N_needed × 1.25

- The **revised version uses the correct formula** (× 1.25)
- The **original uses an incorrect formula** (× 1.20 instead of × 1.25), which underestimates the required sample by ~30 participants (708 vs. 738)

### 3.2 Subgroup Analysis Adjustment

**Original:** Doubles the baseline (295 × 2 = 590) for *"subgroup probing by genetic literacy (high vs low)"*

**Revised:** Applies a × 1.3 buffer for subgroup analyses

**Assessment:** Doubling is problematic because:
- Genetic literacy is a **continuous variable** in the regression model
- The statistical analysis plan specifies **simple slopes analysis at ±1 SD**, which does not require a separate analysis on a split sample — it is performed within the full model
- Doubling is appropriate only when running **completely separate analyses** within each subgroup (i.e., a median split and separate regressions for high vs. low literacy groups)
- If simple slopes analysis is the planned approach, a modest buffer (10–30%) is more appropriate than doubling

**Verdict:** The revised version's × 1.3 buffer is more defensible for simple slopes analysis. However, if the authors also plan a supplementary **median-split analysis** (running the full regression model separately for high and low genetic literacy groups), then a larger adjustment (up to × 2) could be justified — but this should be explicitly stated.

### 3.3 NIPT vs. NIPT-SGD Stratification

**Original:** Doubles again (708 × 2 = 1,416) for NIPT vs. NIPT-SGD stratification

**Revised:** No doubling — treats NIPT/NIPT-SGD as one sample

**Assessment:** This depends entirely on the analysis strategy:
- **If NIPT and NIPT-SGD are analyzed as completely separate experiments** with independent regression models for each → doubling is correct
- **If NIPT type is treated as a covariate or additional factor** in a combined model → no doubling needed
- The protocol states participants are *"stratified by NIPT or NIPT-SGD"* at randomization, and some hypotheses (H3a, H3b) specifically concern NIPT-SGD. If the authors want **equal power for interaction tests within each stratum**, doubling is justified

**Verdict:** Depends on the analysis strategy. The protocol should explicitly state whether NIPT-type-specific analyses are primary or secondary. If primary, doubling is warranted.

---

## 4. Recalculated Sample Sizes

Using the **correct G\*Power test** (R² increase, df_tested = 1, k_total = 31):

### Scenario A: f² = 0.04 (small-to-medium, conservative for three-way interaction)

| Step | N | Calculation |
|---|---|---|
| G\*Power base | 199 | R² increase, df_tested=1, k=31 |
| + 20% attrition | 249 | 199 / 0.80 |
| + 30% subgroup buffer | 324 | 249 × 1.30 |
| Rounded per condition | 65 | 324 / 5 conditions |
| **If NIPT/NIPT-SGD separate** | **648** | **324 × 2** |

### Scenario B: f² = 0.02 (small, very conservative)

| Step | N | Calculation |
|---|---|---|
| G\*Power base | 395 | R² increase, df_tested=1, k=31 |
| + 20% attrition | 494 | 395 / 0.80 |
| + 30% subgroup buffer | 643 | 494 × 1.30 |
| Rounded per condition | 129 | 643 / 5 conditions |
| **If NIPT/NIPT-SGD separate** | **1,286** | **643 × 2** |

### Power at Candidate Sample Sizes

The following table shows statistical power for the three-way interaction test (df_tested = 1, k = 31) at various effect sizes:

| N | f²=0.02 | f²=0.03 | f²=0.04 | f²=0.05 | f²=0.08 |
|---|---|---|---|---|---|
| 200 | 0.511 | 0.683 | **0.803** | **0.882** | **0.978** |
| 300 | 0.685 | **0.848** | **0.932** | **0.971** | **0.998** |
| 400 | **0.805** | **0.933** | **0.979** | **0.994** | 1.000 |
| 549 | **0.911** | **0.982** | **0.997** | 1.000 | 1.000 |
| 720 | **0.966** | **0.996** | 1.000 | 1.000 | 1.000 |
| 900 | **0.989** | 1.000 | 1.000 | 1.000 | 1.000 |
| 1,416 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

**Key observations:**
- At N = 900, the study is powered > 0.99 even for f² = 0.02 (very small interaction)
- At N = 400, the study has adequate power (≥ 0.80) for f² ≥ 0.02
- The effective analytic N for the interaction model is 4/5 of total N if control participants are excluded (see Issue 5), so N = 900 total → N = 720 analytic

---

## 5. Methodological Issues in the Statistical Analysis Plan

### Issue 1: Control Group in the Main Regression Model

**Problem:** Both versions include a control group dummy as a predictor in the main interaction model (k = 31). However:
- The control group receives **no message framing**, so the factorial terms (Evidence × Source × Literacy) are **undefined** for control participants
- The analysis plan correctly states the control group will be analyzed separately using planned contrasts
- Including the control dummy in the main factorial model is conceptually problematic — the interaction terms have no meaning for control group participants

**Recommendation:** The main factorial analysis (Blocks 1–4) should include only the 4 experimental conditions (n = 4/5 of total). The control group should be compared separately via planned contrasts as described. This means:
- k_total for the interaction model = 30 (not 31)
- Effective analytic N = 4/5 of total recruited N
- Account for this when calculating sample size

### Issue 2: Multiple Dependent Variables and Type I Error

**Problem:** The study has at least 6 dependent variables: knowledge, attitudes, anxiety (STAI), WTP, uptake intention, and informed choice (with deliberation subscale). Running the full hierarchical regression for each outcome without correction creates a substantial Type I error inflation risk.

**Recommendations:**
- Designate a **primary endpoint** (likely behavioral intention or uptake, given H4)
- Apply **Benjamini-Hochberg FDR correction** across the family of tests for secondary outcomes
- Alternatively, specify the primary analysis as a MANOVA if outcomes are conceptually related, followed by univariate follow-ups
- At minimum, acknowledge the multiple testing issue and state the correction method in the protocol

### Issue 3: Power for Binary and Ordinal Outcomes

**Problem:** The sample size calculation is based entirely on linear regression (continuous outcomes). However, several outcomes are binary (uptake: yes/no; informed choice: deliberated/not) or ordinal. Power for detecting interactions in logistic regression is **substantially lower** than in linear regression for the same N.

**Recommendation:** Conduct a supplementary power analysis for the primary binary outcome (e.g., uptake intention) using simulation or the method of Hsieh et al. (1998) for logistic regression interaction effects. If uptake is the primary endpoint and it is analyzed as binary, the linear regression-based sample size may be insufficient.

### Issue 4: Missing Data Handling Specification

**Problem:** The protocol states *"Multiple imputation if >5% of the data is missing"* but does not specify:
- The number of imputations (m)
- Which variables are included in the imputation model
- The method of imputation (e.g., MICE, predictive mean matching)
- How imputed datasets are pooled (Rubin's rules)

**Recommendation:** Specify m ≥ 20 imputations if missing data exceeds 10%. Include all analysis variables and auxiliary variables in the imputation model. Use fully conditional specification (MICE) with appropriate methods per variable type. Pool results using Rubin's rules.

### Issue 5: Proportional Odds Assumption

**Problem:** The protocol mentions ordinal logistic regression but does not address the proportional odds assumption.

**Recommendation:** State that the proportional odds assumption will be tested (Brant test or likelihood ratio test comparing proportional odds to multinomial model). If violated, use partial proportional odds or multinomial logistic regression as specified.

### Issue 6: Bootstrap Specification

**Problem:** Bootstrapping is mentioned for sensitivity analyses but the number of iterations is unspecified.

**Recommendation:** Specify 5,000 bootstrap resamples with bias-corrected and accelerated (BCa) confidence intervals.

### Issue 7: WTP Model Specification

**Observation:** The WTP analysis uses interval regression for dichotomous-choice data, which is appropriate. The hierarchical framework for WTP predictors is sound. Controlling for household income is essential and is mentioned.

**Minor recommendation:** Specify whether WTP will be log-transformed before analysis (common for economic valuation data that is right-skewed) or whether a log-link GLM will be used.

### Issue 8: Robust Regression Specification

**Problem:** The protocol mentions robust regression (M-estimator or S-estimator) for outliers but does not specify when it will be used.

**Recommendation:** Specify criteria for switching to robust regression, e.g., when ≥ 5% of observations have Cook's distance > 4/N, or when Shapiro-Wilk test rejects normality of residuals at alpha = 0.01.

---

## 6. Summary: Which Version Is Correct?

**Neither version's G\*Power calculation is fully correct.** Both appear to have used the wrong G\*Power test ("R² deviation from zero" instead of "R² increase") and/or incorrect predictor counts.

However, the **revised version is substantially more defensible** for the following reasons:

| Criterion | Original | Revised | Assessment |
|---|---|---|---|
| G\*Power test specification | Wrong test, wrong k | Wrong test (likely), but states correct test name | Revised is clearer |
| Attrition formula | Incorrect (× 1.20) | Correct (× 1.25) | Revised is correct |
| Subgroup adjustment | Doubling (unjustified for simple slopes) | × 1.3 buffer | Revised is more defensible |
| NIPT stratification | Doubling (may be justified) | No doubling | Depends on analysis plan |
| Effect size | f² = 0.05 | f² = 0.04 | Revised is more conservative/appropriate |
| Final N | 1,416 | 900 | See below |
| N/k ratio at base | 9.5 (high overfitting risk) | 17.7 (acceptable) | Revised is safer |
| N/k ratio at final | 45.7 (excellent) | 29.0 (excellent) | Both adequate |

### Recommended Final Sample Size

**If NIPT and NIPT-SGD are analyzed in a combined model:**
- Use the **correct** G\*Power calculation: R² increase, df_tested = 1, k = 30, f² = 0.02 → base N = 395
- + 20% attrition → 494
- + 25% buffer for subgroup probing and binary outcome power → 618
- + Control group (add 1/4 for separate contrast analysis) → 773
- **Recommended: N = 800** (160 per condition)

**If NIPT and NIPT-SGD require separate analyses:**
- Double the experimental group portion → 800 × 2 = 1,600
- But control group need not be doubled → ~1,400
- **Recommended: N = 1,400** (analogous to original's N = 1,416)

**If adopting the revised version's parameters (f² = 0.04):**
- The final N = 900 provides power > 0.99 for f² = 0.04 and power ≈ 0.97 for f² = 0.02
- While technically overpowered for the stated effect size, **N = 900 is a reasonable and defensible sample size** given the uncertainties in effect size estimation, the need for power across multiple outcomes (including binary), and the multiple comparison burden

---

## 7. Recommendations for the Protocol

1. **Correct the G\*Power calculation** to use "R² increase" (not "R² deviation from zero") with df_tested = 1 and clearly state the correct base N
2. **Clarify whether the control group** is excluded from the main factorial analysis model (it should be)
3. **State whether NIPT/NIPT-SGD stratification** requires doubling or is handled within a combined model
4. **Specify a primary endpoint** and correction method for multiple comparisons
5. **Add a supplementary power analysis** for the primary binary outcome
6. **Specify missing data details**: number of imputations, method, pooling rules
7. **Specify bootstrap iterations** (recommend 5,000) and confidence interval type (BCa)
8. **Add proportional odds assumption test** for ordinal logistic regression
9. **Specify robust regression criteria** for when it replaces OLS
10. **Clarify WTP distributional assumptions** and transformation/link function

---

## 8. Corrected Sample Size Section (Suggested Revision)

> Sample size was calculated using G\*Power 3.1 for hierarchical multiple linear regression, specifically the F-test for R² increase (fixed model), testing the three-way interaction (Evidence Type × Message Source × Genetic Literacy).
>
> **Parameters:**
> - Effect size f² = 0.02 (small interaction effect, conservative for three-way interactions based on prior health communication studies)
> - α = 0.05 (two-tailed)
> - Power (1−β) = 0.80
> - Number of tested predictors = 1 (the three-way interaction term)
> - Total predictors in full model = 30 (3 main effects, 3 two-way interactions, 1 three-way interaction, 23 covariates; control group analyzed separately)
>
> G\*Power calculation: N = 395 participants for the factorial conditions.
>
> **Adjustments:**
> - 20% attrition due to incomplete responses or failed manipulation checks: 395 / 0.80 = 494
> - 25% additional buffer for adequate power in subgroup analyses (simple slopes at ±1 SD) and binary outcome analyses: 494 × 1.25 = 618
> - Addition of a control group (1/5 of total): 618 × 5/4 = 773
>
> **Final target sample size: N = 800 participants** (rounded up), approximately 160 participants per condition (4 experimental + 1 control). [If NIPT and NIPT-SGD analyses are conducted separately, double the experimental conditions to N ≈ 1,400 total.]
>
> This sample size provides power > 0.96 for detecting a small three-way interaction (f² = 0.02), achieves 29 participants per predictor (well above the recommended 15–20), and is sufficient for planned sensitivity analyses and multiple comparisons.

---

*Review generated with computational verification via Python/SciPy. All G\*Power calculations independently replicated using the non-central F distribution.*
