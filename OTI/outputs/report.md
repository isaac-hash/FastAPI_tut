# PSS Scalp XAUUSDm — EDA Report

## 1. Summary (key bullets)

- **Overall edge**: Expectancy = 0.259R/trade  (95% CI [0.114, 0.405]), t-test p=0.00039, permutation p=0.00020.
- **Significance**: Statistically significant (p<0.05).
- **Stability**: Trend slope = -0.000784R/trade (p=0.0000). See Phase 2 charts for rolling view.
- **Concentration**: Top 5 trades contribute 9.1% of total R. Edge persists without them but at lower expectancy.
- **Monte Carlo**: Median max drawdown -77.5R, p5 (worst) -128.9R.
- **Modelling**: GBM AUC = 0.4479. Below 0.53 — entry features have limited predictive power.
- **Exit analysis**: Alternative TP levels and BE rules tested. See Phase 7 comparison table.
- **Data caveats**: 0 duplicate pos_ids. All rows retained. Server timezone not confirmed.
- **Concurrent trades**: Up to 28 overlapping positions detected — CIs are optimistic.
- **Key requirement**: All patterns need out-of-sample/forward testing before any live use.

## 2. Data Quality and Assumptions

- **Primary outcome**: result_R (= net_profit / risk_money). Corr with computed R = 0.9982.
- **pnl_R vs result_R**: Small differences in some trades (likely spread/cost adjustments). result_R chosen as primary.
- **Units**: 1 pip = 10 points for XAUUSDm (inferred from risk_pts / sl_pips ≈ 10).
- **Timezone**: Server-hour buckets used. Peak hours suggest UTC+2 or UTC+3. Not confirmed — session labels omitted.
- **Undocumented columns** (inferred):
  - `max_p_b4_sl`: Max positive R reached before adverse move to SL level.
  - `max_L_b4_tp`: Max adverse R before TP was hit (closest to SL before winning).
  - `excursion_flag`: Categorical flag (OK = normal path, other = notable excursion).
  - `min_R_after_1R/2R`: Lowest R reached after first touching that milestone (giveback).
  - `MAE_R`: Stored as negative values for adverse moves.

## 3. Findings by Phase

### Phase 0 — Data Quality
2368 rows × 46 columns. No rows removed silently. See p0_data_dictionary.csv.

### Phase 1 — Baseline
Trades=2368, WR=11.7%, Expectancy=0.259R [0.114,0.405],
PF=1.286, Total R=613.1, Max DD=-382.67R, Longest L-streak=119.
See p1_equity_drawdown.png, p1_R_histogram.png.

### Phase 2 — Stability
Rolling expectancy in p2_rolling_expectancy.png. Half/quarter comparison in p2_half_comparison.csv.
Trend: slope=-0.000784R/trade, p=0.0000. Best single week: 221.70R.

### Phase 3 — Outliers
Large wins (>planned_rr+0.5): 7.  Large losses (<-1.2R): 27.

### Phase 4 — Segmentation
Day×Hour heatmap in p4_day_hour_heatmap.png. FDR results in p4_fdr_correction.csv.

### Phase 5 — Zone Features
Spearman correlations in p5_feature_R_correlation.csv. Derived features in p5_derived_features_R_corr.csv.

### Phase 6 — Costs
Avg spread_to_sl = 0.0186. Filter thresholds in p6_spread_filter_thresholds.csv.

### Phase 7 — Exits
TP alternatives in p7_alt_tp_levels.csv. Breakeven sims in p7_breakeven_simulation.csv.
Exit comparison equity curves in p7_exit_equity_curves.png.

### Phase 8 — Risk
MC median DD -77.5R. Autocorr lag-1 = 0.4631.
Win-after-win = 0.527, win-after-loss = 0.063.

### Phase 9 — Modelling
GBM AUC=0.4479 vs Baseline 0.5000. Top features in p9_feature_importance.png.

## 4. Exit Rule Comparison
See p7_exit_comparison.csv. 'approx' rows use actual result for TP exits above planned_rr
because the post-exit path is unobservable.

## 5. Robustness Table
See p10_robustness_summary.csv.

## 6. Limitations
- Single instrument, single period — results may not generalise to other assets or conditions.
- Overlapping trades — observations not independent, CIs are optimistic.
- Hindsight columns used only for exit analysis (no leakage into entry models).
- Exit simulations are approximations where milestone timestamps are missing.
- All patterns are in-sample. Out-of-sample or forward testing is required.

## 7. Suggested Next Steps
1. Forward-test a spread-to-SL cap (see Phase 6 threshold table) on new live/demo data.
2. Test the best alternative TP level from Phase 7 with a small position size.
3. Validate Day×Hour patterns from Phase 4 on held-out data.
4. Confirm broker server timezone to enable proper session labelling.
5. Investigate concurrent trade correlation and adjust risk sizing accordingly.
6. Run walk-forward analysis on the GBM model with more folds if sample grows.
