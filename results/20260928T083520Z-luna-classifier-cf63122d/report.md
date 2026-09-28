# Benchmark report: luna-classifier

- Run: `20260928T083520Z-luna-classifier-cf63122d`
- Suite: `perf`
- Cases: 180 (180 valid, 0 errors)
- Accuracy: 70.56%
- Provider cost: $0.005341
- Provider cost basis: `provider_reported`
- Provider cost / 1M decisions at this case mix: $29.673889
- Estimated local compute cost: $0.000000
- p50 / p95 latency: 956.1459 / 1557.5578 ms
- Suite throughput: 0.7998 requests/s
- Input / output tokens: 41,413 / 2,400
- Cached input / cache-write / reasoning tokens: 0 / 0 / 0

## Primitive results

| Primitive | n | Accuracy | Macro F1 | Prob. coverage | Brier | NLL | ECE-10 | p50 ms | p95 ms | Provider cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| choice | 60 | 90.00% | 0.8496 | 0.00% | — | — | — | 1001.9045 | 1334.9820 | $0.001909 |
| noul | 60 | 83.33% | 0.8303 | 0.00% | — | — | — | 1023.4155 | 1974.0637 | $0.001629 |
| score | 60 | 38.33% | — | 0.00% | — | — | — | 901.6265 | 2574.1900 | $0.001803 |

## Domains

| Domain | n | Accuracy | p50 ms | Provider cost |
|---|---:|---:|---:|---:|
| access_governance | 12 | 75.00% | 955.1196 | $0.000357 |
| agent_security | 12 | 83.33% | 955.7882 | $0.000400 |
| compliance | 12 | 66.67% | 985.5516 | $0.000352 |
| content_ops | 12 | 75.00% | 920.4886 | $0.000347 |
| customer_support | 12 | 100.00% | 1023.4366 | $0.000362 |
| data_platform | 12 | 83.33% | 1023.7474 | $0.000358 |
| ecommerce | 12 | 41.67% | 1034.1486 | $0.000356 |
| finance_ops | 12 | 75.00% | 985.5107 | $0.000349 |
| hr_ops | 12 | 58.33% | 922.7810 | $0.000352 |
| it_operations | 12 | 75.00% | 956.0622 | $0.000352 |
| logistics | 12 | 33.33% | 1023.3507 | $0.000349 |
| procurement | 12 | 75.00% | 957.8809 | $0.000345 |
| research | 9 | 55.56% | 924.9820 | $0.000264 |
| sales_ops | 9 | 100.00% | 921.8647 | $0.000264 |
| software_delivery | 9 | 66.67% | 921.0240 | $0.000266 |
| workflow_routing | 9 | 66.67% | 953.6246 | $0.000271 |

## Score-specific metrics

- Exact accuracy: 38.33%
- Within ±1 accuracy: 85.00%
- MAE of selected score: 0.8000
- MAE of expected score: —
- Quadratic weighted kappa: 0.6905

## Interpretation notes

Accuracy and calibration are reported separately from latency and cost. The project intentionally does not collapse them into a single winner score. Probability coverage states how many cases exposed a complete usable probability distribution; calibration metrics are computed only on those cases. Provider cost is provider-reported when available or computed from recorded token usage and the pricing snapshot stored in the model configuration. Local models have zero provider cost. Estimated local compute cost is only populated when a machine-hour price was explicitly supplied for the run.
