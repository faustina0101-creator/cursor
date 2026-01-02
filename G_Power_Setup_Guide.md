# G*Power Setup Guide: ANOVA Sample Size Calculation

## Study Design Summary
- **Factorial Design**: 2×2 (Evidence Type × Message Source) + Control = 5 groups
- **Main Predictors**: 
  - Evidence type (statistical vs anecdotal) - 2 levels
  - Message source (government vs influencer) - 2 levels  
  - Genetic literacy (continuous or high/low categorical)
- **Interactions**: 
  - 3 two-way interactions
  - 1 three-way interaction
- **Covariates**: 20 covariates
- **Stratification**: NIPT vs NIPT-SGD conditions

---

## G*Power Test Selection

### Primary Test: **ANOVA: Fixed effects, special, main effects and interactions**

**Rationale**: 
- Matches your factorial design structure
- Directly tests interaction effects
- Appropriate for categorical predictors

---

## Step-by-Step G*Power Setup

### Step 1: Select Test Type
1. **Test family**: `F tests`
2. **Statistical test**: `ANOVA: Fixed effects, special, main effects and interactions`

### Step 2: Determine Effect Size

**From your original calculation:**
- f² = 0.05 (small to medium effect)
- Convert to f: **f = √0.05 = 0.2236** (use **0.224**)

**Input in G*Power**: 
- Effect size f: **0.224**

### Step 3: Set Alpha and Power
- **α err prob**: 0.05
- **Power (1-β err prob)**: 0.80

### Step 4: Determine Numerator Degrees of Freedom (df)

This depends on **which specific effect you're powering for**:

#### Option A: Powering for Three-Way Interaction (Most Conservative)
- **Effect**: Evidence Type × Message Source × Genetic Literacy
- **Numerator df**: 1 (for the 3-way interaction term)
- **Number of groups**: 5 (2×2 factorial + control)
- **Total sample size**: Will be calculated by G*Power

#### Option B: Powering for Two-Way Interaction
- **Effect**: Evidence Type × Message Source (or other 2-way)
- **Numerator df**: 1
- **Number of groups**: 5

#### Option C: Powering for Main Effect
- **Effect**: Evidence Type or Message Source
- **Numerator df**: 1 (for each main effect)
- **Number of groups**: 5

**Recommendation**: Power for the **three-way interaction** (most conservative, ensures all effects are detectable)

### Step 5: Account for Covariates

**Method 1: Adjust Error Degrees of Freedom**
- Covariates reduce error variance (increase power)
- In G*Power, covariates are accounted for by reducing the error df
- **Adjusted error df = Total N - Number of groups - Number of covariates - 1**
- However, G*Power calculates this automatically if you input covariates

**Method 2: Use ANCOVA Approach**
- Since G*Power ANOVA doesn't directly include covariates, you can:
  - Use the regression approach, OR
  - Adjust your effect size slightly upward (covariates increase power)

**Practical Approach**: 
- Use ANOVA as specified
- The 20 covariates will increase your effective power
- Your original calculation (n=223 baseline) already accounted for covariates in the predictor count

### Step 6: Calculate Number of Groups

**For ANOVA calculation:**
- **Number of groups**: 5
  - Group 1: Statistical + Government
  - Group 2: Statistical + Influencer  
  - Group 3: Anecdotal + Government
  - Group 4: Anecdotal + Influencer
  - Group 5: Control (neutral)

**Note**: Genetic literacy is typically a continuous covariate or moderator, not a grouping factor for the ANOVA structure.

---

## Complete G*Power Parameters

### For Three-Way Interaction (Recommended):

```
Test family: F tests
Statistical test: ANOVA: Fixed effects, special, main effects and interactions

Input Parameters:
├─ Effect size f: 0.224
├─ α err prob: 0.05
├─ Power (1-β err prob): 0.80
├─ Numerator df: 1
└─ Number of groups: 5

Output:
└─ Total sample size: [G*Power will calculate]
```

### Expected Sample Size Calculation:

Based on your original calculation:
- **Baseline (with 16 covariates)**: n = 223
- **With 20 covariates**: Slightly fewer needed (covariates increase power)
- **Doubled for subgroup analysis**: n = 446
- **With 20% attrition**: n = 536
- **Per condition**: n = 107

**With ANOVA approach and 20 covariates**, you may need:
- **Minimum per group**: ~90-100 (for 5 groups = 450-500 total)
- **With attrition**: ~540-600 total

---

## Handling Stratified Conditions (NIPT vs NIPT-SGD)

### Option 1: Separate Power Analyses
Run G*Power separately for:
- NIPT condition: n = [calculated]
- NIPT-SGD condition: n = [calculated]
- **Total sample**: Sum of both

### Option 2: Include as Additional Factor
If testing NIPT vs NIPT-SGD as a factor:
- **Design becomes**: 2×2×2 + Control = 9 groups (if control applies to both)
- **Or**: 2×2 factorial × 2 strata = 8 experimental groups + controls

**Recommendation**: Run separate power analyses for each stratum to ensure adequate power within each.

---

## Alternative: Linear Regression Approach (If Preferring Direct Covariate Inclusion)

If you want to explicitly include covariates in the calculation:

```
Test family: F tests
Statistical test: Linear multiple regression: Fixed model, R² deviation from zero

Input Parameters:
├─ Effect size f²: 0.05
├─ α err prob: 0.05
├─ Power (1-β err prob): 0.80
├─ Number of predictors: 28
│  ├─ Main effects: 3
│  ├─ Two-way interactions: 3
│  ├─ Three-way interaction: 1
│  ├─ Control: 1
│  └─ Covariates: 20
└─ Total sample size: [G*Power will calculate]
```

**This approach**: More directly accounts for covariates but less intuitive for factorial design.

---

## Recommended Workflow

1. **Primary calculation**: Use ANOVA approach (as specified above)
2. **Verify with regression**: Cross-check with regression approach
3. **Stratified analysis**: Calculate separately for NIPT and NIPT-SGD
4. **Final sample**: Use the larger of the two calculations, add 20% for attrition

---

## Quick Reference: G*Power Inputs

### ANOVA Approach (Recommended):
- **Test**: ANOVA: Fixed effects, special, main effects and interactions
- **f**: 0.224
- **α**: 0.05
- **Power**: 0.80
- **Numerator df**: 1 (for interaction)
- **Groups**: 5

### Expected Output:
- **Total N**: ~450-500 (before attrition)
- **Per group**: ~90-100
- **With 20% attrition**: ~540-600 total

---

## Notes

1. **Genetic Literacy**: If treated as continuous covariate, it's included in the model but doesn't change the number of groups (stays at 5).

2. **Control Group**: The neutral control is Group 5 in your ANOVA structure.

3. **Subgroup Analysis**: For high vs low genetic literacy subgroups, double your baseline sample size (as you originally did).

4. **Covariates**: The 20 covariates will increase your effective power beyond what G*Power calculates (since it doesn't directly model them in ANOVA), so the calculated sample size is conservative.
