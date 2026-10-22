# Dojo Statistics Foundation Methods Reference (Batch A: WP1–WP5)

## 1. Scope and Governance Boundary

This document specifies the mathematical definitions, normalization rules, bootstrap resampling algorithms, sensitivity analyses, and Pareto frontier constructions implemented in `dojo/bench/records.py`, `dojo/bench/stats.py`, and `dojo/bench/frontier.py`.

- **No Implicit Publication Authority:** Every input envelope is assigned `EligibilityStatus(status="UNVERIFIED", publishable=False, development_only=True)`. Passing a non-null `registration_id` or `evidence_kind="real"` never flips `publishable` to `True`. Stage B registration and real held-out governance require a separate trusted protocol verifier.
- **No Usage/Price Inference:** Provider spend is taken strictly from validated integer `cost_nano_usd` fields ($10^{-9}\text{ USD}$). Missing cost (`null`) is never coerced to `0`, and missing token/step/wall-clock counters are never inferred from cost or from other runs.
- **Owner Learning Boundary:** This library is the reference implementation for task 9b/9g3 and does not replace the project owner's required handwritten exercise in 16c.

---

## 2. Panel Validation and Outcome Normalization (WP1)

Given an `ExpectedPlan` with ordered task list $T = (t_1, \dots, t_n)$ and declared seed tuples $S_c = (s_{c,1}, \dots, s_{c,k_c})$ for each configuration $c \in C$, a complete panel must contain **exactly one** valid record for every expected cell:

$$\mathcal{E} = \{ (c, t, s) \mid t \in T,\; c \in C,\; s \in S_c \}, \quad |\mathcal{E}| = n \sum_{c \in C} k_c$$

### Scorer Status and Evidence Validity Matrix

| `scorer_status` | Required `outcome` | Required `evidence_validity` | Additional Invariant | Effect on Headline Aggregation |
|---|---|---|---|---|
| `passed` | `solved` | `valid` | `execution_complete is True` | Included ($y_{c,t,r} = 1$) |
| `failed` | `unsolved` | `valid` | `execution_complete is True` | Included ($y_{c,t,r} = 0$) |
| `candidate_error` | `unsolved` | `valid` | `baseline_verified is True` and `execution_complete is True` | Included ($y_{c,t,r} = 0$) iff `baseline_verified=True`; otherwise **blocked** |
| `invalid_evidence` | `undetermined` | `invalid` | — | **Blocked** (`audit.status = "blocked"`) |
| `infrastructure_error` | `undetermined` | `unknown` | — | **Blocked** (`audit.status = "blocked"`) |

Any missing cell, duplicate cell, unexpected cell, mixed split (`train` mixed with `held_out`), conflicting task `family_id`, or blocker finding sets `audit.status = "blocked"` and prevents all headline metric calculations. If all cells are valid for outcomes but one or more cells have `cost_nano_usd = null`, `audit.status` is `"cost_incomplete"` (`success_only_allowed = True`, `cost_comparison_allowed = False`).

---

## 3. Primary Estimands and Cost Semantics (WP2)

Let $n = |T|$ be the number of tasks and $k_c = |S_c|$ be the declared repetition count for configuration $c$. For each task $t \in T$ and seed $r \in S_c$, let $y_{c,t,r} \in \{0, 1\}$ denote whether the run solved the task, and $\text{cost}_{c,t,r} \in \mathbb{Z}_{\ge 0}$ denote the measured cost in nano-USD.

1. **Per-task pass rate and mean single-seed cost:**
   $$p_{c,t} = \frac{1}{k_c} \sum_{r \in S_c} y_{c,t,r}, \qquad m_{c,t} = \frac{1}{k_c} \sum_{r \in S_c} \text{cost}_{c,t,r}$$

2. **Equal-task-weighted $\text{pass@1}$:**
   $$\text{pass@1}(c) = \frac{1}{n} \sum_{t \in T} p_{c,t}$$
   Unequal seed counts $k_c$ refine the per-task estimate $p_{c,t}$ without overweighting tasks or configurations. This is $\text{pass@1}$ (expected success of one randomly chosen seed), not $\text{pass@}k$.

3. **Expected solved tasks (single random seed per task):**
   $$S_{\text{exp}}(c) = \sum_{t \in T} p_{c,t} = n \cdot \text{pass@1}(c)$$

4. **Expected total cost of one random-seed run per task (`expected_total_cost_nanos`):**
   $$C_{\text{exp}}(c) = \sum_{t \in T} m_{c,t}, \qquad \bar{m}(c) = \frac{1}{n} C_{\text{exp}}(c)$$

5. **Expected cost per solved task (`expected_cost_per_solved_nanos`):**
   $$\text{CPS}(c) = \begin{cases} \dfrac{C_{\text{exp}}(c)}{S_{\text{exp}}(c)} = \dfrac{\sum_{t \in T} m_{c,t}}{\sum_{t \in T} p_{c,t}} & \text{if } S_{\text{exp}}(c) > 0 \\[8pt] \text{UndefinedValue}(\texttt{"zero\_expected\_solves"}) & \text{if } S_{\text{exp}}(c) = 0 \end{cases}$$
   Measured costs of failed runs remain in the numerator $C_{\text{exp}}(c)$.

6. **Actual all-repetition spend (`actual_all_repetitions_spend_nanos`):**
   $$C_{\text{actual}}(c) = \sum_{t \in T} \sum_{r \in S_c} \text{cost}_{c,t,r}$$
   Reported separately as an exact integer; never divided by single-seed expected solves $S_{\text{exp}}(c)$.

All intermediate calculations use Python `fractions.Fraction` and exact `int` nano-USD, completely independent of floating-point rounding or ambient `decimal` context.

---

## 4. Paired Task Bootstrap (WP3)

- **Resampling unit:** Tasks $t \in \{0, \dots, n-1\}$.
- **Default replicates:** $B = 10,000$ using an isolated `random.Random(seed)` instance.
- **Pairing invariant:** In replicate $b \in \{1, \dots, B\}$, a single multiset of $n$ task indices $I^{(b)} = (i^{(b)}_1, \dots, i^{(b)}_n)$ is drawn uniformly with replacement from $\{0, \dots, n-1\}$. Every compared configuration (and future cascade policy) is evaluated on the **exact same** sampled task indices $I^{(b)}$, retaining all $k_c$ seed runs of each sampled task.
- **Quantile convention (`sorted_empirical_nearest_rank_linear_endpoints`):** Given $B$ sorted exact `Fraction` draws $x_{(0)} \le x_{(1)} \le \dots \le x_{(B-1)}$ and quantile $q \in [0, 1]$ (where $q_{\text{low}} = (1-\alpha)/2$ and $q_{\text{high}} = 1 - (1-\alpha)/2$):
  $$h = q (B - 1), \quad \ell = \lfloor h \rfloor, \quad u = \lceil h \rceil, \quad Q(q) = x_{(\ell)} + (h - \ell)\bigl(x_{(u)} - x_{(\ell)}\bigr)$$
- **Zero-solve draw rule:** For ratio metrics ($\text{CPS}(c)$ and $\Delta \text{CPS}$), if any bootstrap replicate $b$ has zero expected solves ($\sum_{j=1}^n p_{c, i^{(b)}_j} = 0$), the replicate is counted in `zero_solve_draws` and `undefined_draws`, and the unconditional confidence interval endpoints (`lower`, `upper`) are returned as `UndefinedValue(reason="unconditional_interval_blocked_by_zero_solve_draws")`. Zero-solve draws are never silently discarded to fabricate a narrower conditional interval.

---

## 5. Sensitivity Analyses (WP4)

### 5.1 Family-Cluster Bootstrap (`family_cluster_bootstrap`)
- **Non-primary label:** `is_primary = False`, `estimand_label = "sensitivity_family_cluster_bootstrap_task_weighted_within_resampled_clusters"`.
- **Resampling rule:** Let $F = (f_1, \dots, f_M)$ be the $M$ distinct `family_id` clusters. Each replicate draws $M$ families with replacement, includes all tasks belonging to each drawn family occurrence (retaining all seeds), and weights included task occurrences equally.
- **Sample-size variation and total-cost scaling:** When family sizes $|T_f|$ vary, the resampled task count $n^{*(b)} = \sum_{m=1}^M |T_{f^{(b)}_m}|$ varies across draws. To keep total-cost intervals comparable to the original $n$-task benchmark rather than reflecting random cluster-size fluctuations, the estimator reports:
  $$\hat{C}^{*(b)}_{\text{target-}n}(c) = n \cdot \bar{m}^{*(b)}(c) = \frac{n}{n^{*(b)}} \sum_{j=1}^{n^{*(b)}} m_{c, t^{(b)}_j}$$
  alongside `min_resampled_tasks`, `max_resampled_tasks`, and `mean_resampled_tasks`.

### 5.2 Seed-Position and Seed-Subset Sensitivity (`seed_sensitivity_analysis`)
- Evaluates predeclared ordinal seed positions (`position_0`, `position_1`, ...) and explicit caller-supplied seed subsets with full task coverage.
- When configurations have asymmetric seed lists (e.g., $S_A = (0, 1)$, $S_B = (0)$), cross-config single-seed comparisons are valid at `common_seed_positions` ($0 \dots \min_c k_c - 1$) or on `shared_exact_seeds` ($S_A \cap S_B$), whereas additional seeds in $S_A$ quantify within-config seed variance.

---

## 6. Cost-vs-Success Pareto Frontiers (WP5)

`compute_frontier` supports two explicit cost axes (minimizing cost, maximizing $\text{pass@1}$):
1. `cost_per_solved` (headline axis: $\text{CPS}(c)$ vs $\text{pass@1}(c)$)
2. `mean_task_cost` (diagnostic axis: $\bar{m}(c)$ vs $\text{pass@1}(c)$)

Configuration $A$ Pareto-dominates $B$ on cost axis $X$ iff both are defined and:
$$(X_A \le X_B \text{ and } \text{pass@1}_A \ge \text{pass@1}_B) \quad \text{and} \quad (X_A < X_B \text{ or } \text{pass@1}_A > \text{pass@1}_B)$$

- **Exact Ties:** Configurations with identical rational $(X, \text{pass@1})$ are all retained on the frontier if non-dominated and linked via a shared `tie_group_id` and `tied_with` peer tuple.
- **Undefined Points:** Any configuration with `UndefinedValue` on the chosen cost axis (such as a zero-solve configuration on `cost_per_solved`) receives `status = "undefined_cost"`, `is_on_frontier = False`, and cannot dominate or be dominated by valid configurations.

---

## 7. Known Answers on Synthetic Fixtures

1. **`valid_panel.json` (4 tasks, 1 seed each for A and B):**
   - Config A: $\text{pass@1} = 1/2$, $C_{\text{exp}} = 6,000,000\text{ nanos}$, $\bar{m} = 1,500,000\text{ nanos}$, $\text{CPS} = 3,000,000\text{ nanos}$, $C_{\text{actual}} = 6,000,000\text{ nanos}$.
   - Config B: $\text{pass@1} = 1/2$, $C_{\text{exp}} = 40,000,000\text{ nanos}$, $\bar{m} = 10,000,000\text{ nanos}$, $\text{CPS} = 20,000,000\text{ nanos}$, $C_{\text{actual}} = 40,000,000\text{ nanos}$.
   - Frontier: `A` dominates `B` on both `cost_per_solved` and `mean_task_cost`.
2. **`unequal_seed_panel.json` (1 task, A has seeds `[0, 1]`, B has seed `[0]`):**
   - Config A: $\text{pass@1} = 1/2$, $C_{\text{exp}} = 3\text{ nanos}$, $\text{CPS} = 6\text{ nanos}$, $C_{\text{actual}} = 6\text{ nanos}$.
   - Config B: $\text{pass@1} = 0$, $C_{\text{exp}} = 10\text{ nanos}$, $\text{CPS} = \text{UndefinedValue}(\texttt{"zero\_expected\_solves"})$, $C_{\text{actual}} = 10\text{ nanos}$.
