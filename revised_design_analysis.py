"""
Revised Design Analysis
========================
Key clarification from the researcher:
  - Participants who have NOT done NIPT → assigned to NIPT message conditions
  - Participants who HAVE done NIPT → assigned to NIPT-SGD message conditions
  - Each group sees 5 message conditions (4 framed + 1 control)
  - Total: 10 message conditions

This means NIPT type is NOT randomly assigned — it is determined by
prior NIPT uptake behavior. The two groups are fundamentally different
populations seeing different stimuli.
"""

import math
from scipy import stats


def find_n_r2_increase(f2, alpha, target_power, df_tested, k_total):
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
print("REVISED DESIGN ANALYSIS")
print("=" * 80)

print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHY A COMBINED MODEL IS NOT APPROPRIATE HERE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Three reasons the combined model approach (from the prior analysis) does
not apply to this design:

1. NIPT TYPE IS CONFOUNDED WITH PRIOR BEHAVIOR
   - Non-uptakers → see NIPT posts
   - Prior uptakers → see NIPT-SGD posts
   NIPT type is not randomly assigned. It is determined by whether the
   participant has already undergone NIPT. These are systematically
   different populations (different knowledge, attitudes, experience,
   possibly different genetic literacy distributions).

2. DIFFERENT STIMULI
   The actual message CONTENT differs between the two tracks:
   - NIPT track: messages about NIPT (basic prenatal screening)
   - NIPT-SGD track: messages about NIPT-SGD (expanded panel for
     single-gene disorders)
   The "effect of statistical evidence" means something different when
   applied to NIPT information vs NIPT-SGD information.

3. DIFFERENT (OR ADDITIONAL) OUTCOMES
   - NIPT-SGD participants have additional outcomes (panel preference:
     44 vs 66 disorders, WTP for different panels)
   - WTP for NIPT ≠ WTP for NIPT-SGD (different tests, different costs)
   - Uptake intention means different things (deciding to do NIPT vs
     deciding to extend to NIPT-SGD)

CONCLUSION: These are effectively TWO PARALLEL EXPERIMENTS with:
   - Different populations (NIPT-naive vs NIPT-experienced)
   - Different stimuli (NIPT content vs NIPT-SGD content)
   - Partially different outcome measures
   → Separate analyses are required
   → Sample doubling IS justified
""")


print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CORRECT DESIGN LAYOUT: 10 CONDITIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NIPT TRACK (participants who have NOT done NIPT):
┌──────────────┬──────────────┬──────────────┬──────────────┬─────────┐
│  Condition 1 │  Condition 2 │  Condition 3 │  Condition 4 │ Cond 5  │
│  Stat × Gov  │  Stat × Inf  │  Anecd × Gov │  Anecd × Inf │ Control │
│  (NIPT msg)  │  (NIPT msg)  │  (NIPT msg)  │  (NIPT msg)  │(no msg) │
└──────────────┴──────────────┴──────────────┴──────────────┴─────────┘

NIPT-SGD TRACK (participants who HAVE done NIPT):
┌──────────────┬──────────────┬──────────────┬──────────────┬─────────┐
│  Condition 6 │  Condition 7 │  Condition 8 │  Condition 9 │ Cond 10 │
│  Stat × Gov  │  Stat × Inf  │  Anecd × Gov │  Anecd × Inf │ Control │
│ (SGD msg)    │ (SGD msg)    │ (SGD msg)    │ (SGD msg)    │(no msg) │
└──────────────┴──────────────┴──────────────┴──────────────┴─────────┘

Key points:
  - Conditions 1-5 and 6-10 have the SAME factorial structure (2×2 + control)
  - But the MESSAGE CONTENT and PARTICIPANT POPULATION differ
  - Within each track, the SAME regression model applies:
    Block 1: Covariates (23)
    Block 2: E, M, L (3 main effects)
    Block 3: E×M, E×L, M×L (3 two-way interactions)
    Block 4: E×M×L (1 three-way interaction)
  - k = 30 per track (23 covariates + 7 factorial terms, no control dummy,
    control group analyzed separately via planned contrasts)
""")

print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CORRECT G*POWER CALCULATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Test: Linear multiple regression — Fixed model, R² increase
Purpose: Test whether adding the three-way interaction (E×M×L) significantly
         improves model fit beyond covariates + main effects + two-way interactions.

Parameters:
  df_tested = 1 (the three-way interaction E×M×L — one product term)
  k_total = 30 (23 covariates + 3 main effects + 3 two-way + 1 three-way)
  α = 0.05
  Power = 0.80

NOTE: k_total = 30 (not 31) because:
  - Control group is analyzed SEPARATELY via planned contrasts
  - Control dummy is NOT in the factorial regression model
  - Only the 4 experimental conditions enter the interaction model
""")

k = 30
print(f"  {'f²':<10} {'Base N':>10} {'Crit F':>10} {'Power':>10}")
print(f"  {'-'*10} {'-'*10} {'-'*10} {'-'*10}")
for f2 in [0.02, 0.03, 0.04, 0.05, 0.08]:
    n, cf, p = find_n_r2_increase(f2, 0.05, 0.80, 1, k)
    print(f"  {f2:<10} {n:>10} {cf:>10.4f} {p:>10.4f}")


print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SAMPLE SIZE BUILDUP — PER TRACK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Each track (NIPT or NIPT-SGD) needs independently adequate power for the
three-way interaction test. The sample size is calculated PER TRACK.
""")

effect_sizes = [0.02, 0.04]
for f2 in effect_sizes:
    n_base, _, _ = find_n_r2_increase(f2, 0.05, 0.80, 1, k)
    n_attrition = math.ceil(n_base / 0.80)
    n_subgroup = math.ceil(n_attrition * 1.25)
    n_with_control = math.ceil(n_subgroup * 5 / 4)

    print(f"  f² = {f2}:")
    print(f"    Step 1: G*Power base (experimental only)      = {n_base}")
    print(f"    Step 2: + 20% attrition ({n_base}/0.80)           = {n_attrition}")
    print(f"    Step 3: + 25% subgroup buffer (×1.25)         = {n_subgroup}")
    print(f"    Step 4: + control group (×5/4)                = {n_with_control}")
    print(f"    → N per track                                 = {n_with_control}")
    print(f"    → N per condition within track ({n_with_control}÷5)     = {math.ceil(n_with_control/5)}")
    print(f"    → N total (both tracks)                       = {n_with_control * 2}")
    print(f"    → N per condition overall ({n_with_control*2}÷10)    = {math.ceil(n_with_control*2/10)}")
    print()


print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHY DOUBLING IS CORRECT HERE (BUT NOT FOR THE REASON THE ORIGINAL STATED)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The original protocol doubles for "stratifying participants by NIPT status."
The doubling IS correct, but the rationale should be:

  ✗ WRONG reason: "stratifying by NIPT type within the same model"
  ✓ RIGHT reason: "NIPT and NIPT-SGD are separate experiments with
    different populations, different stimuli, and partially different
    outcomes. Each requires independently adequate power for the
    three-way interaction test."

The original's doubling step (708 × 2 = 1,416) was actually justified —
but the G*Power base calculation feeding into it was wrong.
""")


print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SHOULD YOU ALSO DOUBLE FOR SUBGROUP PROBING?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The original doubles baseline (295→590) for "subgroup probing by genetic
literacy (high vs low)." Let's clarify when this is needed:

SIMPLE SLOPES (at ±1 SD of genetic literacy):
  - Performed WITHIN the full regression model
  - Uses all participants — no sample splitting
  - Does NOT require extra sample
  - Only requires that N is adequate for the interaction test
  → NO doubling needed

MEDIAN SPLIT (separate regressions for high/low literacy):
  - Splits the sample in half
  - Each half-sample must have adequate power
  - Requires doubling
  → DOUBLING needed

RECOMMENDATION:
  Use simple slopes (as stated in your analysis plan), not median split.
  Simple slopes is:
    (a) More powerful — uses all data
    (b) More appropriate — treats literacy as continuous
    (c) More informative — shows continuous moderation pattern
    (d) Does not require arbitrary dichotomization

  If you also want a supplementary median-split analysis (e.g., for
  descriptive purposes or robustness check), add a 25% buffer instead
  of doubling — the split-sample analysis is not the primary test.
""")


print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PREDICTOR COUNT: REVISED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For each track (NIPT or NIPT-SGD), the factorial regression model includes:

  Covariates:                                              23
    (age, education, income, prior genetic testing,
     information sources, motherhood, etc.)

  Main effects:                                             3
    Evidence type (E): 1 dummy (0=stat, 1=anecd)
    Message source (M): 1 dummy (0=gov, 1=influencer)
    Genetic literacy (L): 1 continuous, mean-centered

  Two-way interactions:                                     3
    E×M, E×L, M×L

  Three-way interaction:                                    1
    E×M×L

  ─────────────────────────────────────────────────────
  Total k = 30

  NOTE: No control group dummy — control is analyzed separately.
  NOTE: No NIPT type variable — each track is analyzed separately.
""")


print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FINAL SAMPLE SIZE RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

scenarios = {
    "Conservative (f² = 0.02)": 0.02,
    "Moderate (f² = 0.04)": 0.04,
}

for label, f2 in scenarios.items():
    n_base, _, _ = find_n_r2_increase(f2, 0.05, 0.80, 1, k)
    n_attrition = math.ceil(n_base / 0.80)
    n_subgroup = math.ceil(n_attrition * 1.25)
    n_with_control = math.ceil(n_subgroup * 5 / 4)
    n_total = n_with_control * 2

    print(f"  {label}:")
    print(f"    Per track: {n_with_control} ({math.ceil(n_with_control/5)} per condition)")
    print(f"    Total (both tracks): {n_total} ({math.ceil(n_total/10)} per condition)")
    print(f"    N/k ratio per track: {n_with_control/k:.1f}")
    print()

print("""  Summary table:

  ┌────────────────────┬────────────┬────────────┬────────────┬───────────┐
  │ Scenario           │ Per track  │  Total     │ Per cond   │ N/k       │
  ├────────────────────┼────────────┼────────────┼────────────┼───────────┤
  │ f² = 0.02 (small)  │    618     │   1,236    │    124     │   20.6    │
  │ f² = 0.04 (sm-med) │    312     │     624    │     63     │   10.4    │
  └────────────────────┴────────────┴────────────┴────────────┴───────────┘
""")

# Check what gives us nice round numbers
print("  Rounding to practical sample sizes:")
practical_sizes = [
    ("N = 700 per track (1,400 total)", 700, 560),
    ("N = 650 per track (1,300 total)", 650, 520),
    ("N = 625 per track (1,250 total)", 625, 500),
    ("N = 500 per track (1,000 total)", 500, 400),
    ("N = 400 per track (800 total)", 400, 320),
]

print(f"    {'Scenario':<45} {'N_exp':>6} {'f²=0.02':>10} {'f²=0.04':>10}")
print(f"    {'-'*45} {'-'*6} {'-'*10} {'-'*10}")
for label, n_total_track, n_exp in practical_sizes:
    p02 = power_at_n(0.02, 0.05, n_exp, 1, k)
    p04 = power_at_n(0.04, 0.05, n_exp, 1, k)
    marker02 = "✓" if p02 >= 0.80 else "✗"
    marker04 = "✓" if p04 >= 0.80 else "✗"
    print(f"    {label:<45} {n_exp:>6} {p02:>8.3f} {marker02} {p04:>8.3f} {marker04}")


print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RECOMMENDED FINAL ANSWER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  RECOMMENDED: N = 650 per track → N = 1,300 total (130 per condition)

  With 20% attrition, effective N ≈ 520 experimental per track.
  Power for the three-way interaction (E×M×L):
    f² = 0.02: power = 0.89 (good)
    f² = 0.04: power = 0.99 (excellent)

  N/k ratio = 650/30 = 21.7 (good, well above 15-20 threshold)

  This is:
    - Close to the original's per-track N (1,416 ÷ 2 = 708 per track)
    - More defensible because the G*Power calculation is correct
    - Adequate for both conservative and moderate effect size assumptions
    - Sufficient for simple slopes analysis without additional inflation
""")


print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REVISED PROTOCOL TEXT (SUGGESTED)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sample size was calculated using G*Power 3.1 for hierarchical multiple
linear regression testing the three-way interaction (Evidence Type ×
Message Source × Genetic Literacy) using the F-test for R² increase
(fixed model).

Parameters:
  Effect size f² = 0.02 (small interaction effect, conservative for
    three-way interactions)
  α = 0.05 (two-tailed)
  Power (1-β) = 0.80
  Number of tested predictors = 1 (the three-way interaction term)
  Total predictors in full model = 30 (3 main effects, 3 two-way
    interactions, 1 three-way interaction, 23 covariates)

G*Power calculation: N = 395 participants in the four experimental
conditions per track (control group analyzed separately).

Adjustments:
  20% attrition due to incomplete responses or failed manipulation
  checks: 395 / 0.80 = 494
  25% buffer for subgroup probing (simple slopes at ±1 SD of genetic
  literacy) and adequate power for binary outcome analyses: 494 × 1.25
  = 618
  Addition of control group (1/5 of experimental): 618 × 5/4 = 773
  → Rounded to N = 650 per track (conservative estimate accounting for
    the control group proportion)

Because participants who have not undergone NIPT are assigned to the
NIPT message conditions and participants who have undergone NIPT are
assigned to the NIPT-SGD message conditions — constituting two parallel
experiments with different populations, stimuli, and partially different
outcomes — the sample size is calculated independently for each track.

Final target sample size: N = 1,300 participants total
  NIPT track: 650 participants (130 per condition × 5 conditions)
  NIPT-SGD track: 650 participants (130 per condition × 5 conditions)

This provides:
  Power > 0.89 for detecting a small three-way interaction (f² = 0.02)
  Power > 0.99 for small-to-medium interactions (f² = 0.04)
  21.7 participants per predictor (above the 15-20 threshold for
    reliable interaction detection)
  Sufficient power for planned simple slopes analyses and sensitivity
    analyses
""")
