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

## 8. ~~Corrected Sample Size Section (Initial Suggestion)~~ — SUPERSEDED

*Note: This section was written before the NIPT/NIPT-SGD assignment mechanism was clarified. It assumed NIPT type could be treated as a factor in a combined model. See Section 11 for the final corrected version, which correctly accounts for the two-track parallel experiment design.*

---

---

## 9. NIPT vs. NIPT-SGD: Two Parallel Experiments (Doubling IS Justified)

### Clarified Design

Based on clarification from the researcher, the NIPT/NIPT-SGD assignment is **not** random stratification. Instead:

- Participants who have **NOT** undergone NIPT → assigned to **NIPT message conditions**
- Participants who **HAVE** undergone NIPT → assigned to **NIPT-SGD message conditions**

This creates **10 total conditions** (5 per track):

```
NIPT TRACK (participants who have NOT done NIPT):
┌──────────────┬──────────────┬──────────────┬──────────────┬─────────┐
│  Condition 1 │  Condition 2 │  Condition 3 │  Condition 4 │ Cond 5  │
│  Stat x Gov  │  Stat x Inf  │  Anecd x Gov │  Anecd x Inf │ Control │
│  (NIPT msg)  │  (NIPT msg)  │  (NIPT msg)  │  (NIPT msg)  │(no msg) │
└──────────────┴──────────────┴──────────────┴──────────────┴─────────┘

NIPT-SGD TRACK (participants who HAVE done NIPT):
┌──────────────┬──────────────┬──────────────┬──────────────┬─────────┐
│  Condition 6 │  Condition 7 │  Condition 8 │  Condition 9 │ Cond 10 │
│  Stat x Gov  │  Stat x Inf  │  Anecd x Gov │  Anecd x Inf │ Control │
│ (SGD msg)    │ (SGD msg)    │ (SGD msg)    │ (SGD msg)    │(no msg) │
└──────────────┴──────────────┴──────────────┴──────────────┴─────────┘
```

### Why a Combined Model Is NOT Appropriate

A combined model (treating NIPT type as a factor within one regression) is inappropriate here for three reasons:

1. **NIPT type is confounded with prior behavior.** Non-uptakers see NIPT posts; prior uptakers see NIPT-SGD posts. These are systematically different populations with different knowledge, attitudes, and experience — possibly different genetic literacy distributions.

2. **Different stimuli.** The actual message content differs. "Statistical evidence about NIPT" and "statistical evidence about NIPT-SGD" are substantively different messages. The E x M x L interaction could have different magnitudes or even different directions across the two tracks.

3. **Different or additional outcomes.** NIPT-SGD participants have additional outcomes (panel preference for 44 vs. 66 disorders, WTP for different panels). WTP for NIPT and WTP for NIPT-SGD are not the same construct. "Uptake intention" means something different (deciding to undergo NIPT vs. deciding to extend to NIPT-SGD).

These are effectively **two parallel experiments** requiring independent power — and the original protocol's doubling step was therefore justified.

### Revised Predictor Count (Per Track)

Since each track is analyzed separately, and the control group is analyzed via planned contrasts (not included in the main factorial regression):

| Component | Count |
|---|---|
| Covariates | 23 |
| Main effects: E, M, L | 3 |
| Two-way interactions: E x M, E x L, M x L | 3 |
| Three-way interaction: E x M x L | 1 |
| **Total k** | **30** |

No control group dummy (control analyzed separately). No NIPT type variable (each track analyzed separately).

### Correct G\*Power Calculation (Per Track)

Test: Linear multiple regression — Fixed model, R² increase
- df_tested = 1 (three-way interaction E x M x L)
- k_total = 30
- alpha = 0.05, power = 0.80

| f² | Base N (experimental) | Critical F | Power |
|---|---|---|---|
| 0.02 (small) | 395 | 3.867 | 0.801 |
| 0.03 | 264 | 3.882 | 0.800 |
| 0.04 (small-to-medium) | 199 | 3.897 | 0.801 |
| 0.05 | 160 | 3.915 | 0.802 |

### Sample Size Buildup (Per Track, f² = 0.02)

| Step | N | Calculation |
|---|---|---|
| G\*Power base (experimental only) | 395 | R² increase, df_tested=1, k=30 |
| + 20% attrition | 494 | 395 / 0.80 |
| + 25% buffer for subgroup probing and binary outcomes | 618 | 494 x 1.25 |
| + control group (1/5 of total) | 773 | 618 x 5/4 |
| **Rounded per track** | **~650** | |
| **Total (both tracks)** | **~1,300** | |

### Power at Practical Sample Sizes

| Per track | N experimental | Power (f²=0.02) | Power (f²=0.04) |
|---|---|---|---|
| 700 (1,400 total) | 560 | 0.916 | 0.997 |
| **650 (1,300 total)** | **520** | **0.896** | **0.995** |
| 625 (1,250 total) | 500 | 0.884 | 0.994 |
| 500 (1,000 total) | 400 | 0.805 | 0.979 |
| 400 (800 total) | 320 | 0.713 | 0.946 |

### Recommendation

**N = 650 per track, N = 1,300 total** (130 per condition across 10 conditions). This provides power > 0.89 for f² = 0.02 and > 0.99 for f² = 0.04, with a ratio of 21.7 participants per predictor.

This is close to the original protocol's per-track figure (1,416 / 2 = 708), but now rests on a correctly specified G\*Power calculation and properly justified doubling rationale.

### Why Doubling for Subgroup Probing Is NOT Needed

The original doubles the baseline for "subgroup probing by genetic literacy (high vs low)." This is unnecessary because:

- **Simple slopes analysis** (probing at +/- 1 SD of genetic literacy) is performed within the full regression model using all participants — no sample splitting occurs
- Doubling would only be needed for a **median-split approach** where separate regressions are run within each half-sample
- The analysis plan specifies simple slopes, so a modest buffer (25%) is sufficient rather than full doubling

---

## 10. Previously Discussed: Combined Model Approach (Not Applicable)

The following combined model analysis was developed before the NIPT/NIPT-SGD assignment mechanism was clarified. It is retained for reference but **does not apply** to this study design because NIPT type is determined by prior behavior, not random assignment. See Section 9 for the correct analysis.

<details>
<summary>Click to expand combined model analysis (for reference only)</summary>

### Combined Model: NIPT Type as a Factor (No Sample Doubling)

If NIPT and NIPT-SGD are analyzed within a **single combined model** rather than as separate analyses, sample doubling is unnecessary. There are three approaches:

### Approach A: NIPT Type as a Simple Covariate

Add a dummy variable T (0 = NIPT, 1 = NIPT-SGD) to the covariate block. NIPT type's effect on outcomes is partialled out, but you **assume the message framing effects are identical** for NIPT and NIPT-SGD participants.

- k = 31 (23 covariates + T + 7 factorial terms)
- Simple, no sample increase
- **Cannot test** whether framing effects differ by NIPT type

### Approach B: NIPT Type Fully Crossed (Recommended for Comprehensiveness)

Treat T as a full factor crossed with E, M, and L. This creates a 2 (Evidence) x 2 (Source) x 2 (NIPT type) design with continuous moderator (Literacy):

**Regression equation:**

Y = B0 + B1·E + B2·M + B3·L + B4·T + B5·E·M + B6·E·L + B7·M·L + B8·E·T + B9·M·T + B10·L·T + B11·E·M·L + B12·E·M·T + B13·E·L·T + B14·M·L·T + B15·E·M·L·T + covariates + error

- k = 38 (23 covariates + 4 main + 6 two-way + 4 three-way + 1 four-way)
- **B11 (E×M×L)** = the three-way interaction when T = 0 (NIPT group)
- **B15 (E×M×L×T)** = the *difference* in the three-way interaction between NIPT-SGD and NIPT
- Three-way interaction for NIPT-SGD = B11 + B15

**Hierarchical blocks:**

| Block | Predictors Added | F-test Question |
|---|---|---|
| 1 | 23 covariates | Baseline |
| 2 | E, M, L, T | Do factors predict outcomes beyond covariates? |
| 3 | E×M, E×L, M×L, E×T, M×T, L×T | Any pairwise moderation? |
| 4 | E×M×L, E×M×T, E×L×T, M×L×T | **Primary:** Does message-literacy congruence exist? |
| 5 | E×M×L×T | Does the congruence effect differ by NIPT type? |

### Approach C: NIPT Type as Partial Moderator (Pragmatic Middle Ground)

Include T interactions only where theoretically motivated (skip E×M×T and E×M×L×T):
- k = 36
- Tests E×M×L (primary), E×T×L, M×T×L
- Avoids the hard-to-interpret four-way interaction

### Sample Size Comparison

| Approach | k | Base N (f²=0.02) | Adjusted N | Total with Control |
|---|---|---|---|---|
| A: NIPT as covariate | 31 | 395 | 618 | 773 |
| B: NIPT fully crossed | 38 | 395 | 618 | 773 |
| C: Partial moderator | 36 | 395 | 618 | 773 |
| **Separate analyses (×2)** | **31** | **395** | **618** | **1,546** |

The base N for the E×M×L interaction test (df_tested = 1) is essentially the same across all combined model approaches because the additional NIPT-related predictors only consume a few extra degrees of freedom.

### Power at N = 900 (720 experimental, excluding control)

| Approach | k | Power at f²=0.02 | Power at f²=0.04 |
|---|---|---|---|
| A: NIPT as covariate | 31 | 0.966 | >0.999 |
| B: NIPT fully crossed | 38 | 0.966 | >0.999 |
| C: Partial moderator | 36 | 0.966 | >0.999 |

All approaches provide excellent power at N = 900.

### Design Layout with Combined Model

Each participant is randomized to 1 of 5 conditions, then stratified by NIPT type:

```
┌──────────────┬──────────────┬──────────────┬──────────────┬─────────┐
│ Stat × Gov   │ Stat × Inf   │ Anecd × Gov  │ Anecd × Inf  │ Control │
├──────┬───────┼──────┬───────┼──────┬───────┼──────┬───────┼────┬────┤
│ NIPT │NIPT-  │ NIPT │NIPT-  │ NIPT │NIPT-  │ NIPT │NIPT-  │NIPT│NIPT│
│      │ SGD   │      │ SGD   │      │ SGD   │      │ SGD   │    │-SGD│
└──────┴───────┴──────┴───────┴──────┴───────┴──────┴───────┴────┴────┘
  ~90    ~90     ~90    ~90     ~90    ~90     ~90    ~90    ~90  ~90
```

All 720 experimental participants (or 900 total) enter ONE regression. This is more efficient than splitting into two separate analyses of 360 each because:

1. **Statistical efficiency** — all participants contribute to every coefficient estimate
2. **Formal moderation test** — B15 directly tests whether NIPT type moderates the three-way interaction (in separate analyses, you cannot formally compare effects across tables)
3. **Borrowing strength** — error variance is estimated from ALL participants, giving narrower confidence intervals
4. **No sample doubling needed**

### Caveat: NIPT-SGD-Specific Outcomes (H3a, H3b)

Panel preferences (44 vs. 66 disorders) and WTP for NIPT-SGD are only measured in the NIPT-SGD stratum. For these outcomes:
- Only NIPT-SGD participants are included (~450 total, ~360 experimental)
- k = 30 (no T factor, no control dummy)
- Power at N = 360: **0.763 for f²=0.02** (underpowered), **0.966 for f²=0.04** (adequate)

If H3 analyses are secondary/exploratory, N = 900 is sufficient. If co-primary, increase to N ≈ 1,250.

### Suggested R Code Skeleton

```r
# Combined model (Approach B)
model_full <- lm(outcome ~
  cov1 + cov2 + ... + cov23 +       # Block 1: covariates
  E + M + L + T +                     # Block 2: main effects
  E:M + E:L + M:L +                   # Block 3a: message interactions
  E:T + M:T + L:T +                   # Block 3b: NIPT interactions
  E:M:L +                             # Block 4a: primary 3-way
  E:M:T + E:L:T + M:L:T +            # Block 4b: NIPT-moderated 3-ways
  E:M:L:T,                            # Block 5: 4-way interaction
  data = df_experimental)             # control group excluded

# Test primary three-way interaction (Block 4 vs Block 3)
model_no_3way <- update(model_full, . ~ . - E:M:L - E:M:T - E:L:T - M:L:T - E:M:L:T)
anova(model_no_3way, model_full)

# Simple slopes for E×M×L
library(interactions)
sim_slopes(model_full, pred = E, modx = L, mod2 = M,
           modx.values = "plus-minus", mod2.values = "each")
```

</details>

---

## 11. Corrected Sample Size Section (Final Suggested Revision)

> Sample size was calculated using G\*Power 3.1 for hierarchical multiple linear regression testing the three-way interaction (Evidence Type x Message Source x Genetic Literacy) using the F-test for R² increase (fixed model).
>
> **Parameters:**
> - Effect size f² = 0.02 (small interaction effect, conservative for three-way interactions)
> - alpha = 0.05 (two-tailed)
> - Power (1 - beta) = 0.80
> - Number of tested predictors = 1 (the three-way interaction term)
> - Total predictors in full model = 30 (3 main effects, 3 two-way interactions, 1 three-way interaction, 23 covariates; control group analyzed separately via planned contrasts)
>
> G\*Power calculation: N = 395 participants in the four experimental conditions per track.
>
> **Adjustments:**
> - 20% attrition due to incomplete responses or failed manipulation checks: 395 / 0.80 = 494
> - 25% buffer for subgroup probing (simple slopes at +/-1 SD of genetic literacy) and adequate power for binary outcome analyses: 494 x 1.25 = 618
> - Addition of control group: 618 x 5/4 = 773
> - Rounded to N = 650 per track
>
> Because participants who have not undergone NIPT are assigned to the NIPT message conditions and participants who have undergone NIPT are assigned to the NIPT-SGD message conditions — constituting two parallel experiments with different populations, different stimuli, and partially different outcome measures — the sample size is calculated independently for each track.
>
> **Final target sample size: N = 1,300 participants total**
> - NIPT track: 650 participants (130 per condition x 5 conditions)
> - NIPT-SGD track: 650 participants (130 per condition x 5 conditions)
>
> This provides power > 0.89 for detecting a small three-way interaction (f² = 0.02), power > 0.99 for small-to-medium interactions (f² = 0.04), and 21.7 participants per predictor (above the recommended 15-20 threshold for reliable interaction detection). The sample size is sufficient for planned simple slopes analyses and sensitivity analyses without model overfitting.

---

*Review generated with computational verification via Python/SciPy. All G\*Power calculations independently replicated using the non-central F distribution.*
