# Revised Sample Size and Statistical Analysis Sections

## Sample Size

The primary goal of this study is to test for interaction effects between message evidence type (statistical vs anecdotal), message source (government agency vs social media influencer), and genetic literacy. A neutral control (no message framing) is included to examine baseline responses in the absence of message framing. Interaction effects require larger samples than main effects, and a conservative approach towards sample size calculation is used.

The study is based on a 2×2 factorial design with a control group. Using G*Power 3.1 software, sample size was calculated using **linear multiple regression: fixed model, R² increase**. This approach tests whether the addition of interaction terms significantly increases the proportion of variance explained (R²) beyond the main effects model.

### Power Analysis Parameters:
- **Test family:** F tests
- **Statistical test:** Linear multiple regression: Fixed model, R² increase
- **Effect size f²:** 0.02 (small effect size for the R² increase attributable to interaction terms)
- **α error probability:** 0.05
- **Power (1-β):** 0.80
- **Number of tested predictors:** 4 (three two-way interactions + one three-way interaction)
- **Total number of predictors:** 2,323 (2 main effect predictors for message frame [evidence type, message source] + 1 genetic literacy predictor + 3 two-way interactions + 1 three-way interaction + 2,316 covariates)

The effect size f² for R² increase is calculated as:

$$f² = \frac{R²_{AB} - R²_{A}}{1 - R²_{AB}} = \frac{ΔR²}{1 - R²_{full}}$$

Where:
- R²_A = variance explained by main effects and covariates alone
- R²_AB = variance explained by full model (main effects + interactions + covariates)
- ΔR² = incremental variance explained by interaction terms

Using these parameters, the computed sample size a priori for detecting the incremental contribution of interaction terms is **n = [INSERT G*POWER OUTPUT]**. To permit adequately powered subgroup analyses by genetic literacy level (high vs low), this baseline is doubled. Accounting for a 20% attrition rate and potential exclusions due to failed manipulation checks, the adjusted total sample size is calculated accordingly. This provides sufficient power to detect whether the interaction effects of message frames and genetic literacy explain significant additional variance in the outcome variables beyond main effects alone.

When further stratified by NIPT status (NIPT vs NIPT-SGD), sample sizes per stratum should maintain adequate power for the R² increase test.

---

## Statistical Analysis

All valid responses will be exported to R v4.4 software for data analysis. Because part of the survey is conducted in paper format, missing data may occur. Missing data will be handled via multiple imputation if >5% of the data is missing. Below is a description of the analytical approach.

### 1) Preliminary Analysis

**Randomization Checks:**
Before testing hypotheses, one-way ANOVAs (for continuous variables) and chi-square tests (for categorical variables) will be conducted to verify successful randomization across the five message frame conditions. No significant differences in socio-demographic characteristics or baseline genetic literacy across groups are expected.

**Descriptive Statistics:**
Socio-demographic characteristics, outcome variables, and manipulation check items will be summarized using percentages, means, medians, standard deviations (SD), and ranges as appropriate. Relationships between categorical variables will be examined using chi-square tests. Pearson's correlation (for normally distributed continuous variables) or Spearman's correlation (for non-normal or ordinal variables) will assess associations between continuous variables.

**Manipulation Check:**
Manipulation check items using the Behaviour Identification Form (BIF) will be analyzed to verify the integrity of framing manipulations. Independent samples t-tests will compare BIF scores between participants in different message conditions. A significant difference in the expected direction will confirm successful manipulation. Participants who fail manipulation checks will be excluded from primary analyses, with sensitivity analyses conducted to assess the robustness of findings.

### 2) Hypothesis Testing: Hierarchical Multiple Linear Regression

The primary analytical approach uses **hierarchical (sequential) multiple linear regression** to test whether interaction terms explain significant additional variance (R² increase) in the dependent variables beyond main effects and covariates.

#### Model Building Strategy:

**Step 1 (Block 1) – Covariates:**
Enter socio-demographic covariates (age, educational level, income, prior experience with genetic testing, information sources, motherhood status).

**Step 2 (Block 2) – Main Effects:**
Add main effect predictors:
- Evidence type (statistical vs anecdotal; dummy coded)
- Message source (government vs influencer; dummy coded)
- Genetic literacy (continuous or dichotomized as high/low)

**Step 3 (Block 3) – Two-Way Interactions:**
Add two-way interaction terms:
- Evidence type × Message source
- Evidence type × Genetic literacy
- Message source × Genetic literacy

**Step 4 (Block 4) – Three-Way Interaction:**
Add the three-way interaction term:
- Evidence type × Message source × Genetic literacy

#### Statistical Model Specification:

The full regression model is specified as:

```
Y = β₀ + β₁(Evidence_Type) + β₂(Message_Source) + β₃(Genetic_Literacy) 
    + β₄(Evidence_Type × Message_Source) 
    + β₅(Evidence_Type × Genetic_Literacy) 
    + β₆(Message_Source × Genetic_Literacy) 
    + β₇(Evidence_Type × Message_Source × Genetic_Literacy) 
    + Σβₖ(Covariatesₖ) + ε
```

Where Y represents each continuous dependent variable (message credibility, NIPT knowledge scores, anxiety [STAI], decisional conflict [DCS]).

#### Testing R² Increase:

At each step, the **change in R² (ΔR²)** will be tested for statistical significance using the F-test for R² change:

$$F_{change} = \frac{(R²_{new} - R²_{previous}) / (df_{new} - df_{previous})}{(1 - R²_{new}) / (N - df_{new} - 1)}$$

The primary hypothesis tests focus on:
1. **ΔR² from Step 2 to Step 3:** Tests whether two-way interactions significantly improve model fit beyond main effects
2. **ΔR² from Step 3 to Step 4:** Tests whether the three-way interaction significantly improves model fit beyond two-way interactions

An F-test with p < 0.05 indicates that the added predictors explain significant additional variance.

#### Probing Significant Interactions:

If interaction terms produce a significant R² increase:

1. **Simple slopes analysis** will probe the nature of significant two-way interactions at different levels of the moderator variable (e.g., genetic literacy at ±1 SD from the mean, or high vs low if dichotomized).

2. **Simple simple slopes analysis** will decompose significant three-way interactions by examining two-way interactions at each level of the third moderator.

3. **Johnson-Neyman technique** may be used to identify regions of significance where the effect of one predictor on the outcome is statistically significant across the range of the moderator.

### 3) Analysis for Categorical Outcomes

For categorical dependent variables (NIPT uptake intention [yes/no], dichotomized knowledge [good/poor], SURE scale):

- **Binary logistic regression** will be used with a hierarchical approach analogous to the linear regression models.
- Model comparison will use **likelihood ratio tests (LRT)** to assess whether adding interaction terms significantly improves model fit.
- Effect sizes will be reported as odds ratios (OR) with 95% confidence intervals.

For ordinal outcomes (attitude classified as positive/neutral/negative):

- **Ordinal logistic regression** (proportional odds model) will be employed.
- The proportional odds assumption will be tested using the Brant test.

### 4) Control Group Comparisons

A separate set of analyses will compare message frame conditions against the control (no message framing) condition:

1. Create a dummy variable contrasting any message frame (pooled) vs control
2. Test whether the effect of receiving any framed message (vs control) depends on genetic literacy through the interaction term: Message_Presence × Genetic_Literacy
3. If significant, conduct pairwise comparisons between each specific message condition and the control, moderated by genetic literacy

### 5) Subgroup Analyses

Stratified analyses will be conducted:
- By genetic literacy level (high vs low based on median split or predetermined cut-off)
- By NIPT status (NIPT vs NIPT-SGD)

Within each stratum, the hierarchical regression approach will be replicated to examine whether effects are consistent across subgroups.

### 6) Sensitivity Analyses

1. **Complete case analysis:** Compare results with and without multiple imputation
2. **Manipulation check failures:** Compare primary results (excluding failures) with full sample analysis
3. **Outlier analysis:** Assess influence of outliers using Cook's distance and leverage values
4. **Multicollinearity diagnostics:** Variance inflation factors (VIF) will be examined; VIF > 10 indicates problematic multicollinearity

### 7) Effect Size Reporting

- **R²** and **adjusted R²** for overall model fit
- **ΔR²** (R² change) for incremental contribution of interaction terms
- **Cohen's f²** for local effect sizes: f² = ΔR² / (1 - R²_full)
  - f² = 0.02 (small), 0.15 (medium), 0.35 (large)
- **Standardized regression coefficients (β)** for comparing relative predictor importance
- **Semi-partial correlations (sr²)** for unique variance explained by each predictor

### 8) Multiple Testing Correction

Given multiple dependent variables and numerous hypothesis tests, the following approaches will be used to control Type I error:
- **Benjamini-Hochberg procedure** to control false discovery rate (FDR) at 0.05
- Results will be reported with both unadjusted and FDR-adjusted p-values

### 9) Software and Packages

Analyses will be conducted in R v4.4 using the following packages:
- `lm()` for linear regression
- `car` package for Type III sums of squares and VIF
- `interactions` package for probing and visualizing interactions
- `emmeans` for estimated marginal means and simple slopes
- `mice` for multiple imputation
- `glm()` for logistic regression
- `MASS::polr()` for ordinal logistic regression

---

## Summary Table: Analytical Approach by Dependent Variable

| Dependent Variable | Measurement Level | Primary Analysis | R² Increase Test |
|-------------------|-------------------|------------------|------------------|
| Message credibility | Continuous | Hierarchical linear regression | F-test for ΔR² |
| NIPT knowledge | Continuous (or dichotomized) | Hierarchical linear/logistic regression | F-test or LRT |
| NIPT attitude | Ordinal | Ordinal logistic regression | LRT |
| NIPT uptake intention | Binary | Binary logistic regression | LRT |
| Anxiety (STAI) | Continuous | Hierarchical linear regression | F-test for ΔR² |
| Decisional conflict (DCS) | Continuous | Hierarchical linear regression | F-test for ΔR² |
| Decisional certainty (SURE) | Binary | Binary logistic regression | LRT |
