# EDA Agent Brief: PSS Scalp XAUUSDm Trade Log

## 1. Objective

Run an exploratory data analysis on a backtest/live trade log from a zone-based scalping strategy on XAUUSD (gold, "m" micro/cent-style symbol). Answer four questions, in this order:

1. Is there a positive edge overall, and is it statistically distinguishable from zero?
2. Is the edge stable over time, or is it concentrated in a short period?
3. Which entry-time conditions (setup type, timeframe, session, zone quality) separate good trades from bad ones?
4. Could the exits (SL, TP, breakeven, time stop) be improved using the recorded trade-path data?

The output is a reproducible Python script, tables, charts, and a written report. Do not give trading advice. Report what the data shows, how strong the evidence is, and what should be validated out-of-sample.

## 2. Input

- File: `1792283378842_PSS_SCALP_XAUUSDm.csv` (2,368 rows, 46 columns, one row per closed trade).
- Do not modify the original file. Work on a copy in memory and save cleaned data as `outputs/clean_trades.csv`.

### Column groups

| Group | Columns |
|---|---|
| Identity | `pos_id`, `pair` |
| Setup | `signal_type`, `signal`, `direction`, `zone_timeframe`, `entry_timeframe` |
| Timing | `date`, `entry_day`, `open_time`, `close_time`, `duration_min`, `open_hour` |
| Order parameters | `entry`, `sl`, `tp`, `close_price`, `lots`, `sl_pips`, `tp_pips`, `spread_pips`, `risk_pts`, `spread_pts`, `planned_rr`, `risk_money` |
| Outcome | `net_profit`, `result_R`, `pnl_R`, `exit_reason` |
| Entry-time zone features | `zone_age`, `zone_size_pips`, `zone_touches`, `body_size_ratio`, `engulf_depth` |
| Post-trade path (hindsight only) | `MFE_R`, `MAE_R`, `max_p_b4_sl`, `max_L_b4_tp`, `excursion_flag`, `min_to_MFE`, `min_to_MAE`, `min_to_1R`, `min_to_2R`, `min_to_3R`, `min_R_after_1R`, `min_R_after_2R` |

The meaning of some columns (`max_p_b4_sl`, `max_L_b4_tp`, `excursion_flag`, `min_R_after_1R`, `min_R_after_2R`, and the difference between `result_R` and `pnl_R`) is not documented. Infer each from the data in Phase 0, state your interpretation with the evidence in the report, and flag any you could not resolve.

## 3. Ground rules

1. **Use R, not money.** Lot sizes vary, so all performance metrics use R-multiples. Decide in Phase 0 whether `result_R` or `pnl_R` is the primary outcome and use it consistently. Say which one you chose and why.
2. **No leakage.** Post-trade columns (everything in the "Outcome" and "Post-trade path" groups, plus `close_time`, `close_price`, `duration_min`) are known only after the trade ends. They may be used to describe outcomes and to test exit rules. They must never be used as predictors of entry quality or as entry filters. Entry-time features are: setup columns, `open_hour`, `entry_day`, zone features, `spread_pips`, `sl_pips`, `tp_pips`, `planned_rr`.
3. **Minimum sample size.** Do not report conclusions for any bucket with fewer than 30 trades. Show buckets with 30 to 99 trades but label them "low n". Always show `n` next to every rate or average.
4. **Uncertainty always.** Every expectancy figure for a group is accompanied by a 95% bootstrap confidence interval (5,000 resamples, fixed seed 42). A difference between groups is only called meaningful if the intervals clearly separate or a permutation test gives p < 0.05 after multiple-testing correction.
5. **Multiple comparisons.** Many slices will be examined. Apply Benjamini-Hochberg FDR correction (q = 0.10) across the family of slice tests in Phase 4 and Phase 5, and report both raw and adjusted p-values. Describe any surviving pattern as a hypothesis, not a finding.
6. **Time-aware validation.** Whenever a pattern is found, check whether it holds in both the first and second half of the data (split by time, not randomly). A pattern that appears in only one half is flagged as unstable.
7. **Do not drop trades silently.** If rows are removed or corrected, log the count and reason in the report.
8. **Reproducibility.** One script (`outputs/eda.py`) that runs top to bottom with a fixed random seed and regenerates every table and figure.

## 4. Environment and outputs

Python 3.10+ with pandas, numpy, matplotlib, seaborn, scipy, statsmodels, scikit-learn. Use `shap` only if installed; otherwise use permutation importance.

Create this structure:

```
outputs/
  eda.py
  clean_trades.csv
  report.md
  tables/      # CSV for every table in the report
  figures/     # PNG, 150 dpi, titled, axes labelled, n annotated where relevant
```

## 5. Analysis phases

Complete the phases in order. Save every table to `outputs/tables/` and every figure to `outputs/figures/`, named with the phase number (for example `p3_expectancy_by_signal.csv`).

### Phase 0: Load, validate, and understand the data

1. Load the CSV. Print shape, dtypes, and a missing-value count per column.
2. Parse `open_time` and `close_time` as datetimes. Sort by `open_time`. Report the date range, the number of trading days, and the trades per day distribution.
3. Integrity checks, reporting a count for each:
   - Duplicate `pos_id`.
   - `close_time` earlier than `open_time`.
   - `duration_min` versus `(close_time - open_time)` in minutes. Report the maximum absolute difference.
   - `open_hour` versus the hour in `open_time`.
   - `entry_day` versus the weekday in `open_time` or `date`.
   - Direction consistency: for longs, `sl < entry < tp`. For shorts, `tp < entry < sl`.
   - `planned_rr` versus `tp_pips / sl_pips`.
   - `sl_pips`, `tp_pips`, `risk_pts`, `spread_pts`, `spread_pips` consistency. Work out the units (points versus pips for XAUUSD on this broker) and state the conversion factor you infer.
   - `result_R` versus `net_profit / risk_money`. Report the correlation and the mean absolute difference.
   - `result_R` versus `pnl_R`. Report how they differ (for example, costs, spread, or partial exits). Pick the primary outcome.
   - `exit_reason` categories and their relationship to `result_R` (for example, SL exits should be near -1R).
4. Describe the unlabelled path columns by checking relationships:
   - `MFE_R >= 0` and `MAE_R` sign convention (is MAE stored as positive or negative?).
   - Is `min_to_1R` null exactly when `MFE_R < 1`? Same for 2R and 3R.
   - What do `max_p_b4_sl` and `max_L_b4_tp` represent? Check their ranges and their relationship to `MFE_R`, `MAE_R`, and `exit_reason`.
   - What values does `excursion_flag` take and how do they relate to the other columns?
   - Are `min_R_after_1R` and `min_R_after_2R` the lowest R reached after first touching 1R or 2R?
5. Timezone: look at the distribution of `open_hour` and the trade counts by hour. State whether the hours look like broker server time (often UTC+2 or UTC+3) or UTC, and note that any session labelling (Asia, London, New York) depends on this. Do not convert; label sessions as "server-hour buckets" unless the evidence is clear.
6. Output a **data dictionary table** (`p0_data_dictionary.csv`) with column, dtype, null count, min, max, and your inferred meaning.

### Phase 1: Baseline performance (full sample)

1. Trades, wins, losses, breakevens, win rate.
2. Average win (R), average loss (R), payoff ratio, expectancy (R per trade), profit factor, total R.
3. Median and standard deviation of R, plus skew. Histogram of R with the mean marked.
4. Bootstrap 95% CI for expectancy, win rate, and profit factor.
5. One-sample t-test and a sign-flip permutation test of mean R against 0.
6. Equity curve (cumulative R by trade number and by date), with the drawdown curve below it.
7. Max drawdown (R), longest drawdown duration (trades and days), longest losing streak, longest winning streak.
8. Compare expectancy by direction (long vs short) as a first check.
9. Compare to the theoretical breakeven win rate implied by `planned_rr`: `1 / (1 + planned_rr)`. Report the margin of the realised win rate above it.

### Phase 2: Stability over time

1. Expectancy, win rate, and trade count by month and by ISO week. Plot with CIs for months.
2. Rolling expectancy (window of 100 trades and window of 250 trades) with a zero line.
3. First-half versus second-half comparison (split at the median date) for expectancy, win rate, profit factor, average spread.
4. Split into 4 equal chronological quarters and show the same metrics.
5. Test for a trend: regress `result_R` on trade index and report the slope and p-value. Also check whether `zone_age`, `zone_size_pips`, `spread_pips`, and `sl_pips` drift over time (market regime or data change).
6. State plainly whether the edge looks stable, decaying, or concentrated in a short window. If one month or one week contributes a large share of total R, quantify it (for example, total R with the top 5 trades or top 1 week removed).

### Phase 3: Outlier and concentration check

1. Share of total R from the top 1%, 5%, and 10% of trades. Total R and expectancy with those removed.
2. Look at the largest wins and the largest losses (those below -1R, if any). Investigate every trade with `result_R` below -1.2 or above `planned_rr` + 0.5 (slippage, gaps, spread widening, data errors).
3. Check for any day or session contributing outsized R.

### Phase 4: Segmentation by setup and timing

For each dimension below, produce a table with `n`, win rate, expectancy (R), CI low, CI high, profit factor, average duration, and share of total trades. Apply the minimum sample rules.

Dimensions:
- `signal`, `signal_type` (check whether these map one-to-one first; if so, use one)
- `direction`
- `zone_timeframe`
- `entry_timeframe`
- `zone_timeframe` × `entry_timeframe`
- `signal` × `direction`
- `entry_day`
- `open_hour`
- `exit_reason`
- `planned_rr` (bin if it has many unique values)

Charts: horizontal bar chart of expectancy with CI error bars for each dimension, and a day × hour heatmap of expectancy (mask cells with n < 20) plus a companion heatmap of n.

For each dimension, run a permutation test (10,000 shuffles) of the between-group difference in mean R, then apply FDR correction across all dimensions. Report which results survive.

### Phase 5: Zone-quality and entry features

Features: `zone_age`, `zone_size_pips`, `zone_touches`, `body_size_ratio`, `engulf_depth`, `sl_pips`, `tp_pips`, `spread_pips`, `planned_rr`.

1. Distribution (histogram, boxplot) and summary statistics for each, split by win and loss.
2. Spearman correlation matrix among features, with a heatmap. Flag pairs with |rho| > 0.7 (redundant features).
3. Spearman correlation of each feature with `result_R`, with p-values and FDR adjustment.
4. Quantile bins (quintiles, or fewer where the feature has few unique values such as `zone_touches`): expectancy and win rate per bin with CIs, plotted as a line or bar chart with n labelled. Look for monotonic trends versus a sweet spot.
5. Create derived entry-time features and test them the same way:
   - `spread_to_sl = spread_pips / sl_pips`
   - `zone_to_sl = zone_size_pips / sl_pips`
   - `sl_to_zone = sl_pips / zone_size_pips`
   - `touches_per_age = zone_touches / zone_age` (guard against division by zero)
6. Check interactions of the two strongest features with each other (for example, 3×3 grid of expectancy) and with `direction`.
7. Check each notable pattern in both time halves (rule 6).

### Phase 6: Cost analysis

1. Distribution of `spread_pips` and `spread_pts`, overall and by `open_hour`.
2. Spread as a fraction of risk (`spread_to_sl`), binned. Show expectancy by bin. Identify whether high-cost trades are materially worse.
3. Estimate how much R the spread consumed in total: average `spread_to_sl` times number of trades. Compare expectancy before and after this cost if `result_R` and `pnl_R` differ because of costs.
4. Determine whether a maximum-spread or minimum-SL filter would have improved expectancy, and how many trades it would remove. Present as a table of thresholds with n kept, expectancy, and total R. Remember that this is a hypothesis subject to rule 6.

### Phase 7: Trade-path and exit analysis

This phase often gives the most actionable results. Remember the leakage rule: use it to tune exits, not entries.

1. **Excursion profiles.** Distributions of `MFE_R` and `MAE_R`, separately for winners, losers, and by `exit_reason`. Scatter of `MFE_R` versus `MAE_R` coloured by outcome.
2. **Milestone rates.** Percentage of all trades that reach +1R, +2R, +3R (non-null `min_to_*R`). For those that reach each milestone, the percentage that go on to win, and the median and 75th percentile of time to reach it in minutes.
3. **Giveback analysis.** For trades that reached 1R but did not win, and trades that reached 2R but did not win: how many, what share of those that reached the milestone, and total R lost. Use `min_R_after_1R` and `min_R_after_2R` to see how deep the retracement went.
4. **Stop placement.** Among winners, the distribution of `MAE_R` (how far winners went against the position). Report what percentage of winners had `MAE_R` worse than -0.25, -0.5, -0.75, and what would be lost if the stop were tightened to those levels. Only count a winner as stopped if its worst adverse excursion exceeded the tighter stop, and say that this ignores the fact that tighter stops would change position size and the entry/SL geometry.
5. **Alternative take-profit levels.** For each candidate TP in {0.5R, 0.75R, 1R, 1.25R, 1.5R, 2R, 2.5R, 3R, or the nearest lower value up to the current `planned_rr`}:
   - A trade is a win at that TP if `MFE_R` ≥ TP before the trade closed (the milestone timestamp exists). Otherwise it takes its actual result.
   - Report win rate, expectancy, and profit factor.
   - TP levels above `planned_rr` cannot be evaluated for trades that closed at the original TP, because the post-exit path is unknown. Say so explicitly and do not extrapolate beyond the observable data.
6. **Breakeven rule.** Simulate "move SL to breakeven after +1R" (and +0.5R, +1.5R, +2R if the data support it). Treat a trade as stopped at 0R if it reached the trigger and `min_R_after_trigger` ≤ 0. Where the trigger columns are not available (for example, 0.5R), say the test cannot be done. Compare expectancy with the baseline and report the effect on win rate.
7. **Time stop.** Using `duration_min`, `min_to_MFE`, `min_to_1R`, and `exit_reason`, test whether trades that have not reached +0.5R/+1R within N minutes (for example, N = percentile 50, 75, 90 of `min_to_1R`) end up with worse outcomes. Report the share of trades affected and expectancy for the affected group.
8. **Duration analysis.** Expectancy by duration bucket (quantiles of `duration_min`). Check whether long-duration trades are worse and whether long-duration losers cluster in certain hours.
9. **Excursion flag.** Cross-tabulate `excursion_flag` against outcome and `exit_reason`. Describe what it appears to capture and whether it is stable or useful for analysis.
10. **Exit rule comparison table.** One row per exit rule tested (baseline, each TP variant, each breakeven rule, time stops) with n, win rate, expectancy, total R, profit factor, and max drawdown in R. Plot the equity curves of the top 3 variants against the baseline.

State clearly which exit simulations are exact and which are approximations, and why.

### Phase 8: Risk and sequencing

1. Distribution of consecutive losses (run-length histogram). Compare to what a random sequence with the same win rate would give (simulation of 10,000 shuffles).
2. Test for dependence between consecutive trades (autocorrelation of `result_R` at lags 1 to 5, and win-after-win versus win-after-loss rates).
3. Monte Carlo of drawdown: resample trade R values 10,000 times in random order for the same number of trades. Report the median and 95th percentile of max drawdown (R) and the probability of a drawdown deeper than 10R, 15R, and 20R.
4. Concurrent trades: from `open_time` and `close_time`, report how many positions overlap at once and the correlation of overlapping trades' outcomes. If overlaps are common, note that the trades are not independent and that the CIs above are probably optimistic.
5. Daily R distribution and worst day, worst week.

### Phase 9: Exploratory modelling (hypothesis generation only)

1. Predict a binary target (`result_R > 0`) and, separately, `result_R` as a continuous target, using **entry-time features only** (rule 2). Encode categoricals with one-hot encoding.
2. Split by time: train on the first 70% of trades chronologically, test on the last 30%. Also run an expanding-window walk-forward evaluation (at least 4 folds).
3. Models: a baseline that predicts the training win rate, logistic regression, and a shallow gradient-boosted model (max depth 3, a small number of trees, early stopping on a validation slice of the training period). Report AUC, log loss, and the Brier score on the test set against the baseline.
4. Feature importance by permutation importance on the test set, and SHAP values if available. Plot the top features and their partial dependence.
5. A shallow decision tree (max depth 3, min leaf size 50) for interpretable rules. Report each leaf's n, win rate, and expectancy in both train and test periods.
6. Filter test: take the top-scoring 50% of test trades by model score and compare their expectancy to the full test set with a CI. Only report the result as promising if the CIs separate and the effect is positive in at least most of the walk-forward folds.
7. If AUC on the test set is not clearly above 0.5 (for example, below 0.53 with a CI that includes 0.5), state that the entry features have little predictive power and do not oversell the model.

### Phase 10: Robustness summary

Build a single table of every candidate pattern or filter discovered in Phases 2 to 9, with columns: description, n affected, expectancy affected versus unaffected, raw p-value, FDR-adjusted p-value, holds in first half (Y/N), holds in second half (Y/N), holds in model walk-forward (Y/N/NA), and a verdict:

- **Robust candidate**: survives FDR correction and holds in both halves.
- **Weak candidate**: significant raw but fails FDR or only holds in one half.
- **Likely noise**: everything else.

## 6. Report (`outputs/report.md`)

Write in plain language for a trader who knows R-multiples but not statistics. Structure:

1. **Summary** (maximum 10 bullets): overall edge, stability, strongest robust candidates, exit findings, biggest risks, data caveats.
2. **Data quality and assumptions**: every issue from Phase 0, the units and timezone assumptions, the primary outcome choice, and the inferred meaning of the undocumented columns.
3. **Findings by phase**: for each phase, 1 to 3 key figures embedded by relative path, the main table, and 3 to 5 sentences of interpretation. State uncertainty (CIs, n) with every claim.
4. **Exit-rule comparison** with the approximate versus exact labels.
5. **Robustness table** from Phase 10.
6. **Limitations**: sample size, overlapping trades, regime dependence, a single instrument and period, hindsight columns, the simulation approximations, and the fact that all patterns need out-of-sample or forward testing.
7. **Suggested next steps**: specific, testable ideas (for example, "forward-test a spread-to-SL cap of X on new data"), each with the evidence behind it.

## 7. Style and quality bar

- Every chart has a title, labelled axes, units (R, minutes, pips), and `n` where relevant. Use consistent colours (green for positive, red for negative expectancy).
- Round R to 3 decimals, percentages to 1 decimal.
- Keep the code modular, with one function per phase, and comment the reasoning for any non-obvious choice.
- Do not use any column as a predictor if rule 2 forbids it, even if it improves a metric.
- Never claim causation. Use wording such as "associated with" and "in this sample".
- If a phase cannot be completed because of missing or ambiguous data, say so and move on rather than guessing.

## 8. Definition of done

- `eda.py` runs from scratch without errors and regenerates all tables and figures.
- Every phase has its tables and figures saved.
- `report.md` covers every section above, with n and CIs on every claim.
- The robustness table classifies every candidate pattern.
- The report lists all assumptions and unresolved questions about the data.
