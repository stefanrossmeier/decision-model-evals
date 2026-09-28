# Benchmark report: semif

- Run: `20260927T094812Z-semif-3fc2a72a`
- Suite: `perf`
- Cases: 180 (180 valid, 0 errors)
- Accuracy: 66.11%
- Provider cost: $0.000000
- Provider cost / 1M decisions at this case mix: $0.000000
- Estimated local compute cost: $0.000000
- p50 / p95 latency: 2685.8922 / 2896.5552 ms
- Suite throughput: 1.5201 requests/s

## Primitive results

| Primitive | n | Accuracy | Macro F1 | Brier | NLL | ECE-10 | p50 ms | p95 ms | Provider cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| choice | 60 | 88.33% | 0.8492 | 0.1935 | 0.4285 | 0.0540 | 2732.5643 | 2917.9126 | $0.000000 |
| noul | 60 | 78.33% | 0.7689 | 0.1500 | 0.4667 | 0.0698 | 2544.3978 | 2762.6111 | $0.000000 |
| score | 60 | 31.67% | — | 0.8504 | 1.7516 | 0.3018 | 2719.2145 | 2905.2843 | $0.000000 |

## Domains

| Domain | n | Accuracy | p50 ms | Provider cost |
|---|---:|---:|---:|---:|
| access_governance | 12 | 75.00% | 2552.2416 | $0.000000 |
| agent_security | 12 | 58.33% | 2765.0375 | $0.000000 |
| compliance | 12 | 33.33% | 2546.2354 | $0.000000 |
| content_ops | 12 | 83.33% | 2552.3091 | $0.000000 |
| customer_support | 12 | 83.33% | 2707.4127 | $0.000000 |
| data_platform | 12 | 83.33% | 2733.0827 | $0.000000 |
| ecommerce | 12 | 50.00% | 2657.2034 | $0.000000 |
| finance_ops | 12 | 66.67% | 2567.6091 | $0.000000 |
| hr_ops | 12 | 50.00% | 2714.1543 | $0.000000 |
| it_operations | 12 | 75.00% | 2589.2393 | $0.000000 |
| logistics | 12 | 58.33% | 2395.1276 | $0.000000 |
| procurement | 12 | 66.67% | 2555.2327 | $0.000000 |
| research | 9 | 44.44% | 2700.2632 | $0.000000 |
| sales_ops | 9 | 88.89% | 2728.4427 | $0.000000 |
| software_delivery | 9 | 77.78% | 2734.0343 | $0.000000 |
| workflow_routing | 9 | 66.67% | 2737.0883 | $0.000000 |

## Score-specific metrics

- Exact accuracy: 31.67%
- Within ±1 accuracy: 71.67%
- MAE of expected score: 0.9170
- Quadratic weighted kappa: 0.5951

## Interpretation notes

Accuracy and calibration are reported separately from latency and cost. The project intentionally does not collapse them into a single winner score. Provider cost is the billed/request-reported amount when available; local models have zero provider cost. Estimated local compute cost is only populated when a machine-hour price was explicitly supplied for the run.
