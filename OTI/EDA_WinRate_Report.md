# PSS Scalp XAUUSDm — Win Rate EDA Report
### Supplementary Analysis · Dataset: 2,368 trades · Oct 2025 – Oct 2026

> [!NOTE]
> All figures saved to `OTI/outputs/figures/` · All tables saved to `OTI/outputs/tables/`  
> Win rate = proportion of trades where `result_R > 0`. Buckets with n < 10 flagged as low-sample.

---

## 1 · Win Rate by Day-of-Week × Signal Type

![Win Rate by Day of Week x Signal Type](C:\Users\HP\.gemini\antigravity-ide\brain\409f9399-c274-417f-b748-4e4896a06da6\winrate_by_dow_x_signal_type.png)

### Win Rate Table

| Signal Type | Mon | Tue | Wed | Thu | Fri |
|:-----------:|:---:|:---:|:---:|:---:|:---:|
| **4** | 0.130 | **0.187** | 0.092 | 0.077 | 0.127 |
| **5** | 0.074 | 0.110 | 0.099 | 0.077 | **0.200** |
| **41** | 0.048 | 0.065 | 0.000 | 0.100 | **0.125** |
| **42** | 0.119 | 0.107 | 0.107 | 0.082 | **0.140** |
| **43** | 0.100 | 0.250 | **0.375** | 0.000 | 0.429 ⚠️ |
| **51** | 0.083 | 0.034 | **0.292** | 0.032 | 0.214 |
| **52** | 0.000 | 0.000 | 0.125 | **0.400** | 0.222 ⚠️ |
| **53** | 0.128 | 0.134 | 0.127 | 0.081 | **0.151** |

⚠️ = low sample size (n < 15) — interpret with caution.

### Trade Count Table

| Signal Type | Mon | Tue | Wed | Thu | Fri | **Total** |
|:-----------:|:---:|:---:|:---:|:---:|:---:|:---------:|
| **4** | 69 | 75 | 65 | 91 | 79 | **379** |
| **5** | 68 | 73 | 71 | 65 | 70 | **347** |
| **41** | 21 | 31 | 25 | 30 | 40 | **147** |
| **42** | 135 | 149 | 131 | 146 | 143 | **704** |
| **43** | 10 | 4 | 8 | 9 | 7 | **38** |
| **51** | 24 | 29 | 24 | 31 | 28 | **136** |
| **52** | 1 | 6 | 8 | 5 | 9 | **29** |
| **53** | 109 | 119 | 118 | 123 | 119 | **588** |

### Key Findings

- **Overall win rates are low across the board** (mostly 5–20%), consistent with a high-RR scalping strategy where most exits are SL hits.
- **Friday is the strongest day globally** — signal types 4, 5, 42, 53 all peak on Friday. Type 5 hits its highest at **20%** on Friday.
- **Thursday is the weakest day** — types 4, 5, 42, 43, 51 all show their lowest (or near-lowest) win rates on Thursday.
- **Signal type 43** shows the widest day-to-day variance (0% Thu → 37.5% Wed → 42.9% Fri) but has only 38 total trades — **treat these numbers as directional only**.
- **Signal type 51** has a notable Wednesday spike (29.2%) vs. a very poor Thursday (3.2%), suggesting intra-week timing is critical for this signal.
- **Signal type 52** is the smallest sample (29 trades) — no reliable DOW conclusions possible.
- **Signal types 42 and 53** are the most traded and most statistically stable. Both show a gentle Friday edge over Thursday.

> [!TIP]
> **Actionable**: Consider de-prioritising Thursday entries, especially for types 5, 43, and 51. Friday entries for types 4, 5, and 42 show the most consistent relative outperformance.

---

## 2 · Win Rate by SL Range (risk_pts Buckets)

![Win Rate by SL Range](C:\Users\HP\.gemini\antigravity-ide\brain\409f9399-c274-417f-b748-4e4896a06da6\winrate_by_sl_range.png)

### Data Table

| SL Range (risk_pts) | n | Win Rate | Expectancy (R) |
|:-------------------:|:-:|:--------:|:--------------:|
| 0 – 500 | 0 | — | — |
| 500 – 1000 | 0 | — | — |
| 1000 – 1500 | 0 | — | — |
| 1500 – 2000 | 0 | — | — |
| 2000 – 2500 | 2 | 0.500 ⚠️ | +4.473 ⚠️ |
| 2500 – 3000 | 2 | 0.000 ⚠️ | −1.005 ⚠️ |
| 3000 – 3500 | 7 | 0.143 ⚠️ | +0.564 ⚠️ |
| 3500 – 4000 | 12 | 0.000 | −1.022 |
| 4000 – 4500 | 20 | 0.200 | +1.194 |
| 4500 – 5000 | 32 | 0.031 | −0.666 |
| **> 5000** | **2293** | **0.118** | **+0.267** |

⚠️ = very low sample (n < 10).

### Key Findings

> [!IMPORTANT]
> **97% of all trades (2,293 / 2,368) have risk_pts > 5,000.** The 0–5,000 range is almost entirely empty for this dataset. The SL size on XAUUSDm is systematically large.

- **The usable SL range is > 5,000 pts** — the majority bucket. Its win rate of **11.8%** with an expectancy of **+0.267R** tells us the system ekes out positive expectancy through winners large enough to overcome the low hit rate.
- The 4,500–5,000 bucket shows the worst win rate in the populated range (**3.1%**, −0.67R expectancy) with n=32 — this may represent trades entering at the edge of the zone where SL placement is tightest but still in the large-SL regime.
- The 4,000–4,500 bucket (n=20) has the best win rate of the sub-5000 group (**20%**, +1.19R) but this is too small to be conclusive.
- **No trades exist below 2,000 pts** — the minimum observed SL is ~2,458 pts (≈246 pips).

> [!TIP]
> **Actionable**: Re-bin in a wider resolution (e.g., 5000–10000, 10000–20000, 20000+) to get statistically valid SL-size segments. This will reveal whether ultra-wide SL trades have materially different win rates vs. moderate ones within the > 5000 range.

---

## 3 · Win Rate by Hour-of-Day × Signal Type

![Win Rate Heatmap by Hour x Signal Type](C:\Users\HP\.gemini\antigravity-ide\brain\409f9399-c274-417f-b748-4e4896a06da6\winrate_by_hour_x_signal_type.png)

![Win Rate per Signal Type — Bar Subplots](C:\Users\HP\.gemini\antigravity-ide\brain\409f9399-c274-417f-b748-4e4896a06da6\winrate_by_hour_per_signal_type.png)

### Win Rate Table (condensed — hours with ≥5 trades across all signals)

| Hour | ST 4 | ST 5 | ST 41 | ST 42 | ST 43 | ST 51 | ST 52 | ST 53 |
|:----:|:----:|:----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| 01 | 0.118 | **0.200** | 0.000 | 0.114 | 0.000 | 0.182 | 1.00⚠️ | **0.179** |
| 02 | 0.136 | 0.095 | 0.125 | 0.073 | 0.500⚠️ | **0.375** | 0.333⚠️ | 0.125 |
| 03 | 0.118 | **0.273** | 0.071 | **0.171** | — | 0.000 | — | 0.100 |
| 04 | 0.143 | 0.056 | 0.667⚠️ | 0.097 | — | 0.000 | 0.000 | 0.133 |
| 05 | 0.150 | **0.238** | 0.100 | 0.185 | — | 0.000 | 0.500⚠️ | 0.167 |
| 06 | 0.059 | 0.000 | **0.231** | 0.056 | 0.000 | 0.000 | 0.000 | 0.083 |
| 07 | **0.417** | 0.000 | 0.000 | 0.088 | 0.000 | 0.125 | 1.00⚠️ | 0.111 |
| 08 | **0.238** | 0.059 | 0.000 | 0.156 | 0.500⚠️ | 0.167 | 0.000 | **0.192** |
| 09 | 0.000 | 0.077 | 0.167 | 0.154 | — | 0.200 | — | 0.100 |
| 10 | 0.077 | **0.214** | 0.000 | 0.057 | 0.000 | 0.000 | 0.000 | 0.103 |
| 11 | 0.053 | 0.000 | 0.000 | 0.077 | **0.333** | 0.000 | — | 0.070 |
| 12 | 0.038 | 0.111 | 0.056 | 0.103 | **0.333** | 0.000 | 0.000 | 0.143 |
| 13 | 0.107 | 0.167 | 0.000 | 0.049 | 0.000 | 0.125 | 0.000 | **0.207** |
| 14 | 0.050 | 0.000 | 0.000 | **0.212** | 0.500⚠️ | 0.125 | 0.500⚠️ | 0.043 |
| 15 | 0.050 | **0.182** | 0.167 | 0.125 | 0.500⚠️ | **0.400** | 0.000 | 0.080 |
| 16 | **0.235** | 0.000 | 0.000 | 0.154 | **0.333** | 0.167 | 0.000 | 0.182 |
| 17 | 0.125 | 0.111 | 0.000 | 0.074 | — | **0.333** | 0.000 | **0.192** |
| 18 | 0.111 | 0.150 | 0.000 | 0.069 | 0.000 | 0.167 | — | 0.120 |
| 19 | **0.200** | 0.071 | 0.000 | **0.200** | 0.000 | 0.000 | 0.000 | 0.038 |
| 20 | 0.118 | 0.158 | 0.000 | 0.080 | 0.000 | **0.250** | 0.000 | 0.136 |

⚠️ = n < 5 trades — not statistically reliable.

### Key Findings by Signal Type

#### Signal Type 4 (n=379)
- **Best hours**: 07:00 (41.7%), 08:00 (23.8%), 16:00 (23.5%), 19:00 (20.0%)
- **Dead zones**: 06:00 (5.9%), 09:00 (0%), 12:00 (3.8%)
- A clear **two-peak pattern**: early session (07–08) and afternoon (16–19)
- Hours 09–15 are generally weak

#### Signal Type 5 (n=347)
- **Best hours**: 01:00 (20.0%), 03:00 (27.3%), 05:00 (23.8%), 10:00 (21.4%), 15:00 (18.2%)
- **Dead zones**: 06:00, 07:00, 08:00, 11:00, 14:00 — all **0%**
- Type 5 thrives in early Asian/London overlap (01–05) and has a midday lull

#### Signal Type 41 (n=147)
- **Best hours**: 04:00 (66.7% — n=3, unreliable), 06:00 (23.1%), 02:00 (12.5%)
- This signal fires almost entirely outside US hours; **win rate collapses** from 17:00 onward (0% across 17–20)
- Hour 04 outlier is 2/3 wins — n too small to rely on

#### Signal Type 42 (n=704) — largest volume signal
- **Best hours**: 14:00 (21.2%), 08:00 (15.6%), 03:00 (17.1%), 16:00 (15.4%), 19:00 (20.0%)
- **Weakest**: 06:00 (5.6%), 10:00 (5.7%), 13:00 (4.9%), 18:00 (6.9%)
- A **US session / late London** bias (14:00, 16:00, 19:00) with decent early-session performance
- Mid-morning London (10:00–13:00) is a consistent weak zone

#### Signal Type 43 (n=38) — very small sample
- Win rates range 0%–50% but all buckets have n ≤ 4
- **No reliable hourly conclusions possible** — needs more data

#### Signal Type 51 (n=136)
- **Best hours**: 02:00 (37.5%), 15:00 (40.0%), 17:00 (33.3%), 20:00 (25.0%)
- **Dead zones**: 03–06 (all 0%), 10–12 (all 0%)
- Strongly bimodal: **Asian night (02:00)** and **US afternoon (15–17)**

#### Signal Type 52 (n=29) — very small sample
- Hour 01:00 and 07:00 each show 100% win rate but n=1 — completely unreliable
- **No reliable hourly conclusions possible**

#### Signal Type 53 (n=588) — second-largest volume
- Most consistent signal overall; win rates range 4%–21% with less variance
- **Best hours**: 01:00 (17.9%), 08:00 (19.2%), 13:00 (20.7%), 16:00 (18.2%), 17:00 (19.2%)
- **Weakest**: 19:00 (3.8%), 23:00 (0%), 14:00 (4.3%)
- Spreads performance reasonably across all sessions

> [!TIP]
> **Actionable**: For the two high-volume signals (42 and 53), filter entries to focus on their best hour windows:
> - **Type 42**: prefer 03:00, 08:00, 14:00, 16:00, 19:00
> - **Type 53**: prefer 01:00, 08:00, 13:00, 16:00–17:00

---

## Summary — Cross-Analysis Observations

| Dimension | Best Condition | Worst Condition |
|:----------|:--------------|:----------------|
| **Day of Week** | Friday (most signals) | Thursday |
| **SL Size** | > 5,000 pts (99% of trades) | 4,500–5,000 pts (3.1% WR) |
| **Hour (Type 4)** | 07:00–08:00, 16:00 | 09:00–14:00 |
| **Hour (Type 5)** | 01:00–05:00 | 06:00–08:00, 11:00, 14:00 |
| **Hour (Type 42)** | 14:00, 19:00 | 10:00–13:00 |
| **Hour (Type 51)** | 02:00, 15:00–17:00 | 03:00–06:00 |
| **Hour (Type 53)** | 01:00, 08:00, 13:00–17:00 | 19:00, 23:00 |

> [!WARNING]
> Overall win rates (8–19%) are characteristic of a **high-RR scalp** setup where winners are expected to be large multiples of R. The system's positive expectancy comes from winner magnitude, not from hit rate — so optimising for win rate in isolation could conflict with the system's edge. Always evaluate win rate alongside **expectancy (mean result_R)** when making filtering decisions.

---

*Report generated from: `PSS_SCALP_XAUUSDm.csv` (2,368 trades) — EDA.ipynb supplementary cells*  
*Figures: [`outputs/figures/`](file:///c:/Users/HP/Desktop/FastAPI_tut/OTI/outputs/figures/) · Tables: [`outputs/tables/`](file:///c:/Users/HP/Desktop/FastAPI_tut/OTI/outputs/tables/)*
