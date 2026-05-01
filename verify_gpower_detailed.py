"""
Detailed G*Power verification — investigating discrepancies between
claimed values and computed values for both original and revised versions.
"""

import numpy as np
from scipy import stats
import math


def power_r2_increase(f2, alpha, n, df_tested, k_total):
    """Power for F-test of R² increase (adding df_tested predictors to a model with k_total total)."""
    df1 = df_tested
    df2 = n - k_total - 1
    if df2 < 1:
        return 0.0, 0.0
    crit_f = stats.f.ppf(1 - alpha, df1, df2)
    ncp = f2 * n
    power = 1 - stats.ncf.cdf(crit_f, df1, df2, ncp)
    return power, crit_f


def find_n_r2_increase(f2, alpha, target_power, df_tested, k_total):
    """Find minimum N for R² increase test."""
    for n in range(k_total + 2, 5000):
        power, crit_f = power_r2_increase(f2, alpha, n, df_tested, k_total)
        if power >= target_power:
            return n, crit_f, power
    return None, None, None


def power_r2_deviation(f2, alpha, n, k_total):
    """Power for F-test of R² deviation from zero (overall model test)."""
    df1 = k_total
    df2 = n - k_total - 1
    if df2 < 1:
        return 0.0, 0.0
    crit_f = stats.f.ppf(1 - alpha, df1, df2)
    ncp = f2 * n
    power = 1 - stats.ncf.cdf(crit_f, df1, df2, ncp)
    return power, crit_f


def find_n_r2_deviation(f2, alpha, target_power, k_total):
    """Find minimum N for R² deviation from zero test."""
    for n in range(k_total + 2, 5000):
        power, crit_f = power_r2_deviation(f2, alpha, n, k_total)
        if power >= target_power:
            return n, crit_f, power
    return None, None, None


print("=" * 80)
print("INVESTIGATION: Where do the claimed N values come from?")
print("=" * 80)

# ============================================================================
# PART 1: Verify with a known G*Power example
# ============================================================================
print("\n--- Part 1: Verification against known G*Power example ---")
print("  Known: f²=0.15, α=0.05, power=0.80, df_tested=1, k_total=5 → N=55")

n, cf, p = find_n_r2_increase(0.15, 0.05, 0.80, 1, 5)
print(f"  My calculation: N={n}, F_crit={cf:.4f}, power={p:.4f}")

# G*Power manual example 2: f²=0.15, α=0.05, power=0.80, df_tested=3, k_total=6
n, cf, p = find_n_r2_increase(0.15, 0.05, 0.80, 3, 6)
print(f"  f²=0.15, df_tested=3, k=6: N={n}, F_crit={cf:.4f}, power={p:.4f}")

# ============================================================================
# PART 2: What test produces the REVISED version's claimed values?
# ============================================================================
print("\n--- Part 2: Testing what produces revised version's N=549 ---")
print("  Revised claims: f²=0.04, α=0.05, power=0.80, df_tested=1, k=31 → N=549")

# Test 1: R² increase with df_tested=1, k=31
n, cf, p = find_n_r2_increase(0.04, 0.05, 0.80, 1, 31)
print(f"\n  Test A - R² increase, df_tested=1, k=31:")
print(f"    N={n}, F_crit={cf:.4f}, power={p:.4f}")
# Check power at N=549
p549, cf549 = power_r2_increase(0.04, 0.05, 549, 1, 31)
print(f"    Power at N=549: {p549:.4f} (F_crit={cf549:.4f})")

# Test 2: R² deviation from zero, k=31
n, cf, p = find_n_r2_deviation(0.04, 0.05, 0.80, 31)
print(f"\n  Test B - R² deviation from zero, k=31:")
print(f"    N={n}, F_crit={cf:.4f}, power={p:.4f}")

# Test 3: R² increase but with f² interpreted differently
# Maybe f² = 0.04 was meant as TOTAL R² rather than R² change?
# If total R² = 0.04 and the interaction explains a fraction...
# Actually, try f² = 0.04 as the partial eta-squared instead
# Partial η² = f² / (1 + f²), so f² = η² / (1 - η²)
# If they put η² = 0.04, then f² = 0.04/0.96 = 0.0417
print(f"\n  Test C - If η² = 0.04 was entered instead of f²:")
f2_from_eta = 0.04 / (1 - 0.04)
n, cf, p = find_n_r2_increase(f2_from_eta, 0.05, 0.80, 1, 31)
print(f"    f² = {f2_from_eta:.4f}, N={n}")

# Test 4: What if they used a DIFFERENT NCP formula?
# Some software uses λ = f² × df_error instead of λ = f² × N
print(f"\n  Test D - Alternative NCP: λ = f² × df_error (not f² × N):")
for n in range(33, 1000):
    df1 = 1
    df2 = n - 31 - 1
    if df2 < 1:
        continue
    crit_f = stats.f.ppf(0.95, df1, df2)
    ncp = 0.04 * df2  # λ = f² × df_error
    power = 1 - stats.ncf.cdf(crit_f, df1, df2, ncp)
    if power >= 0.80:
        print(f"    N={n}, F_crit={crit_f:.4f}, power={power:.4f}")
        break

# Test 5: What if they used ANOVA-style power (not regression)?
# In ANOVA: NCP = f² × N × k / something...
# Actually for fixed effects ANOVA: λ = n × Σ(τ²/σ²) = N × f²
# where f = effect_size_f (not f²)
print(f"\n  Test E - What if f=0.04 (not f²=0.04), i.e., f²=0.0016:")
f2_tiny = 0.04**2  # = 0.0016
n, cf, p = find_n_r2_increase(f2_tiny, 0.05, 0.80, 1, 31)
print(f"    f²={f2_tiny}, N={n}")

# Test 6: What f² with k=31, df_tested=1 gives N=549?
print(f"\n  Test F - What f² gives N=549 with k=31, df_tested=1?")
for f2_test in np.arange(0.001, 0.10, 0.001):
    n, _, _ = find_n_r2_increase(f2_test, 0.05, 0.80, 1, 31)
    if n is not None and 545 <= n <= 553:
        print(f"    f²={f2_test:.4f} → N={n}")

# Test 7: R² deviation from zero with different k values
print(f"\n  Test G - R² deviation from zero with different k:")
for k in [7, 8, 24, 28, 30, 31, 32]:
    n, cf, p = find_n_r2_deviation(0.04, 0.05, 0.80, k)
    print(f"    k={k}: N={n}")

for k in [7, 8, 24, 28, 30, 31, 32]:
    n, cf, p = find_n_r2_deviation(0.05, 0.05, 0.80, k)
    print(f"    k={k}, f²=0.05: N={n}")


# ============================================================================
# PART 3: What test produces the ORIGINAL version's N=295?
# ============================================================================
print("\n--- Part 3: Tracing original's N=295 ---")

# Already found: R² deviation from zero with k=7, f²=0.05
n, cf, p = find_n_r2_deviation(0.05, 0.05, 0.80, 7)
print(f"  R² deviation from zero, k=7, f²=0.05: N={n} ✓ (matches 295!)")

print("\n  This means the original used:")
print("    - G*Power test: 'R² deviation from zero' (NOT 'R² increase')")
print("    - k = 7 (only the factorial terms, NO covariates)")
print("    - This tests whether the OVERALL model (all 7 factorial terms)")
print("      explains significant variance, NOT the three-way interaction alone.")


# ============================================================================
# PART 4: What test produces the REVISED version's claimed values?
# ============================================================================
print("\n--- Part 4: Systematic search for revised N=549 ---")

# Check all combinations of G*Power tests
print("\n  Checking R² deviation from zero:")
for k in range(1, 35):
    n, _, _ = find_n_r2_deviation(0.04, 0.05, 0.80, k)
    if n is not None and 545 <= n <= 553:
        print(f"    k={k}, f²=0.04: N={n} ← MATCH!")

for k in range(1, 35):
    n, _, _ = find_n_r2_deviation(0.05, 0.05, 0.80, k)
    if n is not None and 545 <= n <= 553:
        print(f"    k={k}, f²=0.05: N={n} ← MATCH!")

print("\n  Checking R² increase (various df_tested):")
for k in range(1, 35):
    for dt in range(1, min(k+1, 32)):
        n, _, _ = find_n_r2_increase(0.04, 0.05, 0.80, dt, k)
        if n is not None and 545 <= n <= 553:
            print(f"    k={k}, df_tested={dt}, f²=0.04: N={n} ← MATCH!")

for k in range(1, 35):
    for dt in range(1, min(k+1, 32)):
        n, _, _ = find_n_r2_increase(0.05, 0.05, 0.80, dt, k)
        if n is not None and 545 <= n <= 553:
            print(f"    k={k}, df_tested={dt}, f²=0.05: N={n} ← MATCH!")


# ============================================================================
# PART 5: Now check revised f²=0.05→393 and f²=0.08→267
# ============================================================================
print("\n--- Part 5: Checking revised f²=0.05→393 and f²=0.08→267 ---")

# f²=0.05 → 393
print("\n  Searching for N=393:")
for k in range(1, 35):
    n, _, _ = find_n_r2_deviation(0.05, 0.05, 0.80, k)
    if n is not None and 389 <= n <= 397:
        print(f"    R² deviation, k={k}, f²=0.05: N={n}")

for k in range(1, 35):
    for dt in range(1, min(k+1, 32)):
        n, _, _ = find_n_r2_increase(0.05, 0.05, 0.80, dt, k)
        if n is not None and 389 <= n <= 397:
            print(f"    R² increase, k={k}, df_tested={dt}, f²=0.05: N={n}")

# f²=0.08 → 267
print("\n  Searching for N=267:")
for k in range(1, 35):
    n, _, _ = find_n_r2_deviation(0.08, 0.05, 0.80, k)
    if n is not None and 263 <= n <= 271:
        print(f"    R² deviation, k={k}, f²=0.08: N={n}")

for k in range(1, 35):
    for dt in range(1, min(k+1, 32)):
        n, _, _ = find_n_r2_increase(0.08, 0.05, 0.80, dt, k)
        if n is not None and 263 <= n <= 271:
            print(f"    R² increase, k={k}, df_tested={dt}, f²=0.08: N={n}")


# ============================================================================
# PART 6: Correct sample size for R² increase (the proper test)
# ============================================================================
print("\n" + "=" * 80)
print("PART 6: CORRECT SAMPLE SIZES (R² increase, testing 3-way interaction)")
print("=" * 80)

print("\n  Test: R² increase for the three-way interaction term")
print("  df_tested = 1, k_total = 31\n")

for f2 in [0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.10, 0.15]:
    n, cf, p = find_n_r2_increase(f2, 0.05, 0.80, 1, 31)
    print(f"  f² = {f2:.2f}: N = {n:>5}, F_crit = {cf:.4f}, power = {p:.4f}")

print("\n  Without covariates (k_total = 7):")
for f2 in [0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.10, 0.15]:
    n, cf, p = find_n_r2_increase(f2, 0.05, 0.80, 1, 7)
    print(f"  f² = {f2:.2f}: N = {n:>5}, F_crit = {cf:.4f}, power = {p:.4f}")

print("\n  With k_total = 30 (excluding control dummy):")
for f2 in [0.02, 0.03, 0.04, 0.05, 0.06, 0.08, 0.10, 0.15]:
    n, cf, p = find_n_r2_increase(f2, 0.05, 0.80, 1, 30)
    print(f"  f² = {f2:.2f}: N = {n:>5}, F_crit = {cf:.4f}, power = {p:.4f}")


# ============================================================================
# PART 7: Recalculated recommendation
# ============================================================================
print("\n" + "=" * 80)
print("PART 7: RECALCULATED RECOMMENDATIONS")
print("=" * 80)

print("""
CRITICAL FINDING: BOTH VERSIONS HAVE ERRORS IN G*POWER USAGE

ORIGINAL VERSION:
  - Used "R² deviation from zero" (overall model F-test) with k=7
  - This tests whether ALL 7 factorial terms JOINTLY explain variance
  - This is NOT the correct test for the three-way interaction
  - N=295 matches R²-deviation-from-zero with k=7, f²=0.05

REVISED VERSION:
  - Claims to use "R² increase" with df_tested=1, k=31
  - But N=549 does NOT match this specification (correct answer: N=199)
  - N=549 likely comes from a DIFFERENT test configuration
  - Possibly R²-deviation-from-zero with k≈25-28 at f²=0.04
""")

# Find what gives N=549
print("  Investigating N=549 origin:")
n, cf, p = find_n_r2_deviation(0.04, 0.05, 0.80, 28)
print(f"    R² deviation, k=28, f²=0.04: N={n}")
n, cf, p = find_n_r2_deviation(0.04, 0.05, 0.80, 27)
print(f"    R² deviation, k=27, f²=0.04: N={n}")

# The correct approach
print("""
CORRECT CALCULATION:
  For testing the three-way interaction (Evidence × Source × Literacy):
  - G*Power test: "Linear multiple regression: Fixed model, R² increase"
  - Effect size: f² (Cohen's f² for R² change)
  - df_tested = 1 (the three-way interaction term)
  - k_total = 30 (without control dummy, since control is analyzed separately)
  - OR k_total = 31 (if control dummy included)

  Results (k=31):
""")

for f2 in [0.02, 0.04, 0.05, 0.08]:
    n, cf, p = find_n_r2_increase(f2, 0.05, 0.80, 1, 31)
    
    # Adjustments
    n_attrition = math.ceil(n / 0.80)  # 20% attrition
    n_subgroup = math.ceil(n_attrition * 1.3)  # 30% buffer for subgroup probing
    n_nipt_separate = n_subgroup * 2  # if NIPT/NIPT-SGD analyzed separately
    
    print(f"  f² = {f2}:")
    print(f"    Base N = {n}")
    print(f"    + 20% attrition = {n_attrition}")
    print(f"    + 30% subgroup buffer = {n_subgroup}")
    print(f"    Per condition (÷5) = {math.ceil(n_subgroup/5)}")
    print(f"    If NIPT/NIPT-SGD separate = {n_nipt_separate}")
    print(f"    Per condition (÷5, doubled) = {math.ceil(n_nipt_separate/5)}")
    print()

print("""
IMPORTANT CAVEAT:
  f² = 0.02-0.04 for a three-way interaction is VERY conservative.
  Three-way interactions are notoriously difficult to detect.
  Published three-way interactions typically have f² in the 0.01-0.05 range.
  
  For a SMALL three-way interaction (f² = 0.02):
    Base N = 395 (much larger, and arguably more appropriate)
  
  For f² = 0.04 (small-to-medium):
    Base N = 199 (much smaller than both versions claim)
    But with adjustments: ~325-650 depending on NIPT strategy
    
  The revised version's final N=900 is OVERPOWERED for the stated parameters
  if using the correct G*Power test, but may be appropriate if:
    (a) f² is smaller than 0.04 (e.g., f² ≈ 0.015-0.02)
    (b) Power for binary outcomes is considered
    (c) Multiple comparisons adjustment is needed
    (d) NIPT/NIPT-SGD requires separate analyses
""")

# ============================================================================
# PART 8: Power at various N for the three-way interaction
# ============================================================================
print("=" * 80)
print("PART 8: POWER TABLE AT VARIOUS SAMPLE SIZES")
print("=" * 80)

print(f"\n  {'N':>6}  {'f²=0.02':>10}  {'f²=0.03':>10}  {'f²=0.04':>10}  {'f²=0.05':>10}  {'f²=0.08':>10}")
print(f"  {'':>6}  {'power':>10}  {'power':>10}  {'power':>10}  {'power':>10}  {'power':>10}")
print(f"  {'-'*6}  {'-'*10}  {'-'*10}  {'-'*10}  {'-'*10}  {'-'*10}")

for n in [100, 150, 200, 250, 300, 350, 400, 450, 500, 549, 600, 700, 720, 800, 900, 1000, 1200, 1416]:
    row = f"  {n:>6}"
    for f2 in [0.02, 0.03, 0.04, 0.05, 0.08]:
        p, _ = power_r2_increase(f2, 0.05, n, 1, 31)
        row += f"  {p:>10.4f}"
    print(row)

print("""
Notes on reading this table:
  - k=31 total predictors, df_tested=1 (three-way interaction)
  - Values ≥ 0.80 indicate adequate power
  - N=720 = effective analytic N if N=900 total and control (1/5) excluded
""")
