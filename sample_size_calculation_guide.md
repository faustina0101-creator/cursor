# Sample Size Calculation Guide for Factorial Design with Interactions

## Study Design Summary
- **Design**: 2×2 factorial design + control
- **Factors**: 
  - Message evidence type (statistical vs anecdotal)
  - Message source (government agency vs social media influencer)
  - Genetic literacy (moderator)
- **Groups**: 4 experimental conditions + 1 control = 5 groups
- **Stratification**: NIPT and NIPT-SGD conditions

---

## G*Power Statistical Test Selection

### Recommended Test: **F tests - Linear multiple regression: Fixed model, R² increase**

**Why this test?**
- You're testing the **incremental contribution of interaction terms** beyond main effects
- This is the most appropriate for factorial designs with covariates
- Allows you to specifically test the R² change due to interactions

### Alternative Test: **F tests - ANOVA: Fixed effects, special, main effects and interactions**
- Can be used for factorial ANOVA framework
- Less flexible for testing specific interaction contributions with many covariates

---

## Updated Sample Size Calculation Parameters

### Test Family: F tests
### Statistical Test: Linear multiple regression: Fixed model, R² increase

### Parameters:

#### Set A (Tested Predictors - Interaction Terms):
- 3 two-way interactions
- 1 three-way interaction
- **Total = 4 predictors tested**

#### Set B (Total Predictors in Model):
**Main Effects:**
- 2 dummy codes for evidence type (if 3 levels with control)
- 2 dummy codes for message source (if 3 levels with control)
- 1 genetic literacy (continuous or dichotomized)
- **Subtotal: 5 main effect predictors**

**OR if control is separate:**
- 1 dummy for evidence type (2 levels)
- 1 dummy for message source (2 levels)  
- 1 genetic literacy
- 1 control group indicator
- **Subtotal: 4 main effects**

**Interactions:**
- 3 two-way interactions
- 1 three-way interaction
- **Subtotal: 4 interactions**

**Covariates:**
- **20 covariates** (updated from 16)

**Stratification:**
- 1 NIPT/NIPT-SGD stratification indicator
- OR 2 indicators if also testing interaction with stratification

**Total predictors (Set B):**
- Main approach: 4 main + 4 interactions + 20 covariates + 1 stratification = **29 predictors**
- Conservative approach (if testing stratification interactions): **30-32 predictors**

### Effect Size and Power Parameters:
- **Effect size f²**: 0.05 (small to medium effect for interaction)
- **α err prob**: 0.05
- **Power (1-β err prob)**: 0.80
- **Number of tested predictors**: 4 (the interaction terms)
- **Total number of predictors**: 29-32 (depending on model specification)

---

## G*Power Input Steps

1. **Test family**: F tests
2. **Statistical test**: Linear multiple regression: Fixed model, R² increase
3. **Type of power analysis**: A priori: Compute required sample size
4. **Input Parameters**:
   - Effect size f² = 0.05
   - α err prob = 0.05
   - Power (1-β err prob) = 0.80
   - Number of tested predictors = 4
   - Total number of predictors = 29 (or 30-32 for conservative estimate)

5. **Click "Calculate"**

---

## Expected Sample Size Results

### For 29 total predictors:
- **Base sample size**: ~245-250 participants

### For 32 total predictors (conservative):
- **Base sample size**: ~260-265 participants

### Adjustments:
1. **Double for subgroup analysis by genetic literacy**: 
   - Base × 2 = ~490-530 participants

2. **Adjust for 20% attrition**:
   - Adjusted sample / 0.80 = ~610-665 participants

3. **Per condition** (5 groups):
   - Total / 5 = ~122-133 participants per condition

### Stratification Consideration:
If NIPT and NIPT-SGD are **separate strata** requiring separate analyses:
- You may need to **power each stratum separately**
- This could require: ~610-665 per stratum = **1,220-1,330 total**

If stratification is a **covariate/control variable** in a unified analysis:
- Use the single pooled sample: **610-665 total**

---

## Recommendations

1. **Clarify stratification approach**:
   - If NIPT and NIPT-SGD require separate subgroup analyses, power each separately
   - If used as a control variable, include as covariate in single analysis

2. **Use conservative total predictor count**: 
   - Include all covariates, main effects, interactions, and stratification indicators
   - Better to slightly overpower than underpower for interaction detection

3. **Consider effect size sensitivity analysis**:
   - f² = 0.05 is small-to-medium
   - For interactions, f² = 0.02-0.04 may be more realistic
   - This would require substantially larger samples

4. **Document assumptions clearly**:
   - Specify exact coding scheme for categorical predictors
   - Note whether continuous variables are centered/standardized
   - Clarify hierarchy of effects being tested

---

## Model Specification for Reference

### Regression Model:
```
Outcome = β₀ + 
          β₁(Evidence) + β₂(Source) + β₃(GenLit) + β₄(Control) +
          β₅(Evidence×Source) + β₆(Evidence×GenLit) + β₇(Source×GenLit) +
          β₈(Evidence×Source×GenLit) +
          β₉(Stratification) +
          β₁₀-₂₉(Covariates 1-20) + ε
```

### Primary Test:
- **H₀**: R² change for interactions (β₅, β₆, β₇, β₈) = 0
- **H₁**: R² change for interactions > 0

This tests whether adding the interaction terms significantly improves model fit beyond main effects and covariates.
