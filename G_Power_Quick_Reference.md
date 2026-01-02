# G*Power Quick Reference: Exact Inputs

## ✅ Step-by-Step Checklist

### 1. Open G*Power and Select Test
- [ ] Click **Test family**: Select `F tests`
- [ ] Click **Statistical test**: Select `ANOVA: Fixed effects, special, main effects and interactions`

### 2. Input Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Effect size f** | **0.224** | Calculated from f² = 0.05 (√0.05 = 0.224) |
| **α err prob** | **0.05** | Type I error rate |
| **Power (1-β err prob)** | **0.80** | 80% power |
| **Numerator df** | **1** | For three-way interaction (most conservative) |
| **Number of groups** | **5** | 2×2 factorial (4 groups) + control (1 group) |

### 3. Click "Calculate"
- G*Power will output: **Total sample size**

---

## Expected Results

### For Three-Way Interaction (df = 1):
- **Estimated total N**: ~450-550
- **Per group (5 groups)**: ~90-110
- **With 20% attrition**: **~540-660 total**

### For Two-Way Interaction (df = 1):
- **Estimated total N**: ~450-550
- **Per group**: ~90-110

### For Main Effect (df = 1):
- **Estimated total N**: ~450-550
- **Per group**: ~90-110

---

## Important Notes

### About Covariates:
- G*Power ANOVA doesn't directly include covariates
- Your 20 covariates will **increase effective power** (reduce error variance)
- The calculated sample size is **conservative** (you may need fewer participants)
- Your original calculation (n=223 baseline) already accounted for covariates

### About Genetic Literacy:
- If **continuous**: Treated as covariate (doesn't change number of groups)
- If **categorical (high/low)**: Could be included as factor, but typically treated as moderator/covariate
- For **subgroup analysis** (high vs low): Double your baseline sample size

### About Stratification (NIPT vs NIPT-SGD):
- **Run separate power analyses** for each stratum
- Or include as additional factor (becomes more complex design)
- **Recommendation**: Calculate separately, use larger sample size

---

## Alternative: Regression Approach (If You Prefer)

If you want to explicitly model covariates:

```
Test family: F tests
Statistical test: Linear multiple regression: Fixed model, R² deviation from zero

Parameters:
- Effect size f²: 0.05
- α err prob: 0.05
- Power: 0.80
- Number of predictors: 28
  (3 main + 3 two-way + 1 three-way + 1 control + 20 covariates)
```

---

## Final Sample Size Recommendation

Based on your design with **20 covariates** and **stratified conditions**:

1. **Baseline calculation** (ANOVA, three-way interaction): ~450-500
2. **Account for covariates** (reduces needed N slightly): ~420-480
3. **Double for subgroup analysis** (genetic literacy high/low): ~840-960
4. **Add 20% attrition**: **~1,008-1,152 total**
5. **Per experimental condition**: ~200-230
6. **Per stratum (NIPT/NIPT-SGD)**: ~500-575 each

**Conservative estimate**: **~1,100-1,200 total participants**

---

## Verification Steps

1. ✅ Run ANOVA calculation in G*Power
2. ✅ Run regression calculation in G*Power (cross-check)
3. ✅ Calculate separately for NIPT and NIPT-SGD strata
4. ✅ Use the larger sample size
5. ✅ Add 20% buffer for attrition/manipulation checks
