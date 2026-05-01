"""
Combined Model Analysis: NIPT type as a factor within a single model
vs. separate analyses requiring sample doubling.
"""

import math
from scipy import stats


def find_n_r2_increase(f2, alpha, target_power, df_tested, k_total):
    """Find minimum N for R² increase test."""
    for n in range(k_total + 2, 5000):
        df1 = df_tested
        df2 = n - k_total - 1
        if df2 < 1:
            continue
        crit_f = stats.f.ppf(1 - alpha, df1, df2)
        ncp = f2 * n
        power = 1 - stats.ncf.cdf(crit_f, df1, df2, ncp)
        if power >= target_power:
            return n, crit_f, power
    return None, None, None


def power_at_n(f2, alpha, n, df_tested, k_total):
    df1 = df_tested
    df2 = n - k_total - 1
    if df2 < 1:
        return 0.0
    crit_f = stats.f.ppf(1 - alpha, df1, df2)
    ncp = f2 * n
    return 1 - stats.ncf.cdf(crit_f, df1, df2, ncp)


print("=" * 80)
print("COMBINED MODEL: NIPT type as a factor (no doubling needed)")
print("=" * 80)

# ============================================================================
# APPROACH A: NIPT type as a simple covariate
# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
APPROACH A: NIPT type as a covariate (simplest)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Model structure:
  Block 1: 23 covariates + NIPT type (dummy: 0=NIPT, 1=NIPT-SGD) = 24 predictors
  Block 2: Evidence type, Message source, Genetic literacy     = 3 predictors
  Block 3: E×M, E×L, M×L                                      = 3 predictors
  Block 4: E×M×L                                               = 1 predictor
  Total k = 24 + 3 + 3 + 1 = 31 (control analyzed separately)

  NIPT type is treated as a nuisance variable — its effect on the outcome
  is controlled for (partialled out), but you ASSUME the message framing
  effects are IDENTICAL for NIPT and NIPT-SGD participants.

  Pros:
    - Simplest approach, no sample doubling
    - Increases precision by reducing residual variance
    - Straightforward interpretation of the three-way interaction

  Cons:
    - Cannot test whether framing effects DIFFER between NIPT and NIPT-SGD
    - Ignores H3a/H3b which specifically concern NIPT-SGD panel preferences
    - May mask important differences in how participants respond to NIPT vs
      NIPT-SGD information
""")

k_a = 31  # 24 covariates (including NIPT type) + 7 factorial terms
print("  Sample size (R² increase, df_tested=1, testing E×M×L):")
for f2 in [0.02, 0.04]:
    n, cf, p = find_n_r2_increase(f2, 0.05, 0.80, 1, k_a)
    print(f"    f² = {f2}: base N = {n}")


# ============================================================================
# APPROACH B: NIPT type as a full moderating factor
# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
APPROACH B: NIPT type as a full crossed factor (most comprehensive)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Model structure (all participants in one model):
  NIPT type (T) is now a FACTOR crossed with all other terms.

  Main effects (4):
    Evidence (E), Source (M), Literacy (L), NIPT type (T)

  Two-way interactions (6):
    E×M, E×L, M×L, E×T, M×T, L×T

  Three-way interactions (4):
    E×M×L, E×M×T, E×L×T, M×L×T

  Four-way interaction (1):
    E×M×L×T

  Covariates: 23
  ─────────────────────────────
  Total k = 4 + 6 + 4 + 1 + 23 = 38

  Hierarchical blocks:
    Block 1: 23 covariates
    Block 2: E, M, L, T                                  (4 main effects)
    Block 3: E×M, E×L, M×L, E×T, M×T, L×T              (6 two-way)
    Block 4: E×M×L, E×M×T, E×L×T, M×L×T                (4 three-way)
    Block 5: E×M×L×T                                     (1 four-way)

  What each block tests:
    Block 2 vs 1: Do message factors and NIPT type predict outcomes?
    Block 3 vs 2: Are there any pairwise moderation effects?
    Block 4 vs 3: PRIMARY — Does E×M×L exist? Does NIPT type moderate
                  any two-way interactions?
    Block 5 vs 4: Does the three-way interaction DIFFER by NIPT type?
                  (i.e., does the message-literacy congruence effect
                  work differently for NIPT vs NIPT-SGD?)

  Pros:
    - Tests everything in a single unified model
    - No sample doubling needed
    - Can test whether E×M×L differs by NIPT type (four-way interaction)
    - Can test NIPT-type-specific effects (E×T, M×T, L×T)
    - More statistically efficient than split-sample

  Cons:
    - More complex model with more predictors (k=38 vs k=31)
    - Four-way interactions are very difficult to detect and interpret
    - Requires more participants per predictor to avoid overfitting
""")

k_b = 38
print("  Sample sizes for different tests within this model:")
print()

# Primary test: E×M×L (df_tested=1)
print("  (a) E×M×L three-way interaction (df_tested=1, k=38):")
for f2 in [0.02, 0.04]:
    n, cf, p = find_n_r2_increase(f2, 0.05, 0.80, 1, k_b)
    print(f"      f² = {f2}: base N = {n}")

print()

# Test whether E×M×L differs by NIPT type (four-way, df_tested=1)
print("  (b) E×M×L×T four-way interaction (df_tested=1, k=38):")
for f2 in [0.02, 0.04]:
    n, cf, p = find_n_r2_increase(f2, 0.05, 0.80, 1, k_b)
    print(f"      f² = {f2}: base N = {n}")

print()

# All three-way interactions jointly (df_tested=4)
print("  (c) All three-way interactions jointly (df_tested=4, k=38):")
for f2 in [0.02, 0.04]:
    n, cf, p = find_n_r2_increase(f2, 0.05, 0.80, 4, k_b)
    print(f"      f² = {f2}: base N = {n}")


# ============================================================================
# APPROACH C: NIPT type as a partial moderator (pragmatic middle ground)
# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
APPROACH C: NIPT type as a partial moderator (recommended pragmatic approach)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Model structure:
  Include NIPT type as a factor with interactions only where theoretically
  motivated. Since H3a/H3b concern NIPT-SGD panel preferences specifically,
  include T interactions with the message factors but skip the four-way.

  Main effects (4):
    E, M, L, T

  Two-way interactions (6):
    E×M, E×L, M×L, E×T, M×T, L×T

  Three-way interactions (3):
    E×M×L (primary), E×T×L, M×T×L
    [Omit E×M×T and E×M×L×T — not hypothesized]

  Covariates: 23
  ─────────────────────────────
  Total k = 4 + 6 + 3 + 23 = 36

  This tests:
    - E×M×L: Primary hypothesis (message-literacy congruence)
    - E×T×L: Does evidence type interact with NIPT type and literacy?
             (relevant to H3: panel preferences may differ by literacy
              and the type of evidence presented)
    - M×T×L: Does message source interact with NIPT type and literacy?

  Pros:
    - Balances comprehensiveness with parsimony
    - Tests NIPT-type moderation where theoretically relevant
    - Avoids the hard-to-interpret four-way interaction
    - k=36 is manageable

  Cons:
    - Omits some higher-order interactions (must justify theoretically)
""")

k_c = 36
print("  Sample sizes (R² increase, df_tested=1, testing E×M×L):")
for f2 in [0.02, 0.04]:
    n, cf, p = find_n_r2_increase(f2, 0.05, 0.80, 1, k_c)
    print(f"    f² = {f2}: base N = {n}")


# ============================================================================
# COMPARISON TABLE
# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPARISON: Combined model vs Separate analyses
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print(f"  {'Approach':<35} {'k':>4} {'Base N':>8} {'+ Adj':>8} {'+ Ctrl':>8} {'Total':>8}")
print(f"  {'(f²=0.02, testing E×M×L)':<35} {'':>4} {'':>8} {'(×1.56)':>8} {'(×1.25)':>8}")
print(f"  {'-'*35} {'-'*4} {'-'*8} {'-'*8} {'-'*8} {'-'*8}")

approaches = [
    ("A: NIPT as covariate", 31),
    ("B: NIPT fully crossed (k=38)", 38),
    ("C: NIPT partial moderator (k=36)", 36),
]

for label, k in approaches:
    n, _, _ = find_n_r2_increase(0.02, 0.05, 0.80, 1, k)
    n_adj = math.ceil(n / 0.80 * 1.25)  # attrition + subgroup buffer
    n_ctrl = math.ceil(n_adj * 5 / 4)
    print(f"  {label:<35} {k:>4} {n:>8} {n_adj:>8} {n_ctrl:>8} {n_ctrl:>8}")

# Separate analyses (doubling)
n_sep, _, _ = find_n_r2_increase(0.02, 0.05, 0.80, 1, 31)
n_sep_adj = math.ceil(n_sep / 0.80 * 1.25)
n_sep_ctrl = math.ceil(n_sep_adj * 5 / 4)
n_sep_total = n_sep_ctrl * 2
print(f"  {'Separate NIPT + NIPT-SGD (×2)':<35} {'31':>4} {n_sep:>8} {n_sep_adj:>8} {n_sep_ctrl:>8} {n_sep_total:>8}")

print()

# ============================================================================
# Power comparison at N=900
# ============================================================================
print("  Power at N=900 (total), N=720 (experimental only, excluding control):")
print(f"  {'Approach':<35} {'k':>4} {'f²=0.02':>10} {'f²=0.04':>10}")
print(f"  {'-'*35} {'-'*4} {'-'*10} {'-'*10}")

for label, k in approaches:
    p02 = power_at_n(0.02, 0.05, 720, 1, k)
    p04 = power_at_n(0.04, 0.05, 720, 1, k)
    print(f"  {label:<35} {k:>4} {p02:>10.4f} {p04:>10.4f}")


# ============================================================================
# DETAILED MODEL SPECIFICATION: Approach B
# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DETAILED: How Approach B (full combined model) works in practice
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DESIGN LAYOUT (what each participant experiences):

  Step 1: Participant is randomized to one of 5 conditions:
          Stat×Gov, Stat×Inf, Anecd×Gov, Anecd×Inf, Control

  Step 2: Within each condition, participant is STRATIFIED to see either
          NIPT content or NIPT-SGD content.

  So the full crossing is:

  ┌──────────────┬──────────────┬──────────────┬──────────────┬─────────┐
  │ Stat × Gov   │ Stat × Inf   │ Anecd × Gov  │ Anecd × Inf  │ Control │
  ├──────┬───────┼──────┬───────┼──────┬───────┼──────┬───────┼────┬────┤
  │ NIPT │NIPT-  │ NIPT │NIPT-  │ NIPT │NIPT-  │ NIPT │NIPT-  │NIPT│NIPT│
  │      │ SGD   │      │ SGD   │      │ SGD   │      │ SGD   │    │-SGD│
  └──────┴───────┴──────┴───────┴──────┴───────┴──────┴───────┴────┴────┘

  With N=900 and equal allocation:
    900 ÷ 5 conditions = 180 per condition
    180 ÷ 2 NIPT types = 90 per cell

  In the COMBINED model, ALL 900 participants enter ONE regression.

REGRESSION EQUATION (for a continuous outcome Y):

  Y = β₀
    + β₁·E + β₂·M + β₃·L + β₄·T              ← main effects
    + β₅·E·M + β₆·E·L + β₇·M·L               ← message interactions
    + β₈·E·T + β₉·M·T + β₁₀·L·T              ← NIPT type interactions
    + β₁₁·E·M·L                                ← PRIMARY: message congruence
    + β₁₂·E·M·T + β₁₃·E·L·T + β₁₄·M·L·T     ← NIPT-moderated interactions
    + β₁₅·E·M·L·T                              ← does congruence differ by NIPT?
    + Σ βⱼ·Covⱼ                                ← 23 covariates
    + ε

  Where:
    E = Evidence type (0 = statistical, 1 = anecdotal)
    M = Message source (0 = government, 1 = influencer)
    L = Genetic literacy (continuous, mean-centered)
    T = NIPT type (0 = NIPT, 1 = NIPT-SGD)
    Covⱼ = jth covariate

INTERPRETATION OF KEY COEFFICIENTS:

  β₁₁ (E×M×L): The three-way interaction when T=0 (NIPT group).
    "Does the message-congruence effect exist for NIPT participants?"

  β₁₅ (E×M×L×T): The DIFFERENCE in the three-way interaction
    between NIPT-SGD (T=1) and NIPT (T=0).
    "Does the message-congruence effect differ for NIPT-SGD vs NIPT?"

  The three-way interaction for NIPT-SGD participants is: β₁₁ + β₁₅
    If β₁₅ is significant → the congruence effect differs by NIPT type
    If β₁₅ is not significant → the congruence effect is the same

  β₈ (E×T): Does the effect of evidence type differ by NIPT type?
  β₉ (M×T): Does the effect of message source differ by NIPT type?
  β₁₀ (L×T): Does the effect of genetic literacy differ by NIPT type?

HIERARCHICAL BLOCK TESTING (F-tests for ΔR²):

  Block 1 → Block 2: ΔR² for adding E, M, L, T
    "Do the experimental factors and NIPT type predict outcomes
     beyond covariates alone?"

  Block 2 → Block 3: ΔR² for adding all two-way interactions
    "Are there any pairwise moderation effects?"

  Block 3 → Block 4: ΔR² for adding all three-way interactions
    PRIMARY TEST: "Does E×M×L exist? Do NIPT-type-moderated
     two-way interactions exist?"

  Block 4 → Block 5: ΔR² for adding E×M×L×T
    "Does the three-way interaction differ by NIPT type?"

SIMPLE SLOPES FOLLOW-UP:

  If β₁₁ (E×M×L) is significant:
    Probe at L = mean ± 1 SD, separately for each combination of E and M.
    This shows HOW the message framing effect changes with literacy.

  If β₁₅ (E×M×L×T) is significant:
    Probe the three-way interaction separately for NIPT (T=0) and
    NIPT-SGD (T=1) groups.
    This shows WHETHER the literacy-congruence pattern differs by test type.

  If β₁₅ is NOT significant:
    Report that the E×M×L interaction does not differ by NIPT type,
    and interpret β₁₁ as the common three-way interaction.

R CODE SKELETON:

  # Combined model
  model_full <- lm(outcome ~
    cov1 + cov2 + ... + cov23 +       # Block 1: covariates
    E + M + L + T +                     # Block 2: main effects
    E:M + E:L + M:L +                   # Block 3a: message interactions
    E:T + M:T + L:T +                   # Block 3b: NIPT interactions
    E:M:L +                             # Block 4a: primary 3-way
    E:M:T + E:L:T + M:L:T +            # Block 4b: NIPT-moderated 3-ways
    E:M:L:T,                            # Block 5: 4-way interaction
    data = df_experimental)             # control group excluded

  # Test primary three-way interaction
  model_no_3way <- update(model_full, . ~ . - E:M:L - E:M:L:T)
  anova(model_no_3way, model_full)

  # Simple slopes
  library(interactions)
  sim_slopes(model_full, pred = E, modx = L, mod2 = M,
             modx.values = "plus-minus", mod2.values = "each")

ADVANTAGES OF COMBINED MODEL:

  1. STATISTICAL EFFICIENCY: All 720 experimental participants (or 900
     total) contribute to estimating EVERY coefficient. In separate
     analyses, each NIPT-type analysis would use only half the data.

  2. FORMAL TEST OF MODERATION: β₁₅ directly tests whether NIPT type
     moderates the three-way interaction. In separate analyses, you
     would need to eyeball whether the effects "look different" across
     two tables — which is not a valid statistical comparison.

  3. BORROWING STRENGTH: Error variance is estimated from ALL participants,
     giving more precise estimates and narrower confidence intervals.

  4. NO SAMPLE DOUBLING: Same total N powers both the main interaction
     test AND the NIPT-type moderation test.
""")

# ============================================================================
# Special: WTP and panel preference for NIPT-SGD
# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SPECIAL CASE: WTP and panel preferences for NIPT-SGD (H3a, H3b)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

H3a and H3b concern panel preferences (44 vs 66 disorders) and WTP
specifically for NIPT-SGD participants. These outcomes are only
measured for the NIPT-SGD stratum.

For these analyses:
  - Only NIPT-SGD participants are included (N = 450 if N_total = 900)
  - The model reverts to the original structure (no T factor):
    E, M, L, E×M, E×L, M×L, E×M×L + 23 covariates
  - k = 30 (no control, no NIPT type)
  - This is effectively the "separate analysis for NIPT-SGD" approach,
    but ONLY for the NIPT-SGD-specific outcomes

Power for NIPT-SGD-specific outcomes (k=30, N=360 experimental):
""")

for f2 in [0.02, 0.04]:
    p = power_at_n(f2, 0.05, 360, 1, 30)
    n_needed, _, _ = find_n_r2_increase(f2, 0.05, 0.80, 1, 30)
    sufficient = "✓ adequate" if p >= 0.80 else "✗ underpowered"
    print(f"  f² = {f2}: power = {p:.4f} (need N={n_needed} for 80%) → {sufficient}")

print("""
  For f² = 0.02, N=360 is underpowered for NIPT-SGD-specific analyses.
  For f² = 0.04, N=360 is adequate.

  If NIPT-SGD-specific analyses (H3) are SECONDARY:
    → Accept lower power, report as exploratory
  If H3 analyses are equally important as H4:
    → Need N ≈ 500 NIPT-SGD participants → total N ≈ 1,250
""")


# ============================================================================
# Final recommendation
# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FINAL RECOMMENDATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For the primary hypothesis (H4: E×M×L three-way interaction):
  → Use Approach B or C (combined model with NIPT type as factor)
  → No sample doubling needed
  → N = 900 provides power > 0.95 for f² = 0.02 across all approaches

For NIPT-SGD-specific hypotheses (H3a, H3b: panel preferences, WTP):
  → These inherently use only half the sample (NIPT-SGD stratum)
  → With N = 900 total, ~360 NIPT-SGD experimental participants
  → Adequate for f² ≥ 0.04, underpowered for f² = 0.02
  → If these are secondary/exploratory: N = 900 is sufficient
  → If these are co-primary: increase to N ≈ 1,250

Overall: N = 900 with a combined model is well-justified for the primary
hypothesis and adequate for secondary NIPT-SGD-specific analyses assuming
at least a small-to-medium interaction effect (f² ≥ 0.04).
""")
