# Benchmark report: luna-classifier

- Run: `20260928T083905Z-luna-classifier-7c844df3`
- Suite: `perf`
- Cases: 180 (180 valid, 0 errors)
- Accuracy: 72.78%
- Provider cost: $0.005341
- Provider cost basis: `provider_reported`
- Provider cost / 1M decisions at this case mix: $29.673889
- Estimated local compute cost: $0.000000
- p50 / p95 latency: 889.3769 / 1123.1384 ms
- Suite throughput: 4.2965 requests/s
- Input / output tokens: 41,413 / 2,400
- Cached input / cache-write / reasoning tokens: 0 / 0 / 0

## Primitive results

| Primitive | n | Accuracy | Macro F1 | Prob. coverage | Brier | NLL | ECE-10 | p50 ms | p95 ms | Provider cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| choice | 60 | 91.67% | 0.8629 | 0.00% | — | — | — | 905.3325 | 1109.7459 | $0.001909 |
| noul | 60 | 86.67% | 0.8629 | 0.00% | — | — | — | 934.4593 | 1284.1141 | $0.001629 |
| score | 60 | 40.00% | — | 0.00% | — | — | — | 833.9849 | 1037.4694 | $0.001803 |

## Domains

| Domain | n | Accuracy | p50 ms | Provider cost |
|---|---:|---:|---:|---:|
| access_governance | 12 | 75.00% | 896.5340 | $0.000357 |
| agent_security | 12 | 83.33% | 873.7133 | $0.000400 |
| compliance | 12 | 66.67% | 885.6454 | $0.000352 |
| content_ops | 12 | 83.33% | 888.4303 | $0.000347 |
| customer_support | 12 | 91.67% | 884.1057 | $0.000362 |
| data_platform | 12 | 91.67% | 868.3534 | $0.000358 |
| ecommerce | 12 | 50.00% | 843.5090 | $0.000356 |
| finance_ops | 12 | 75.00% | 972.1557 | $0.000349 |
| hr_ops | 12 | 58.33% | 884.8848 | $0.000352 |
| it_operations | 12 | 75.00% | 883.5425 | $0.000352 |
| logistics | 12 | 33.33% | 907.0410 | $0.000349 |
| procurement | 12 | 83.33% | 886.5507 | $0.000345 |
| research | 9 | 55.56% | 927.4407 | $0.000264 |
| sales_ops | 9 | 100.00% | 845.7843 | $0.000264 |
| software_delivery | 9 | 66.67% | 886.0450 | $0.000266 |
| workflow_routing | 9 | 77.78% | 978.0669 | $0.000271 |

## Score-specific metrics

- Exact accuracy: 40.00%
- Within ±1 accuracy: 88.33%
- MAE of selected score: 0.7333
- MAE of expected score: —
- Quadratic weighted kappa: 0.7376

## Interpretation notes

Accuracy and calibration are reported separately from latency and cost. The project intentionally does not collapse them into a single winner score. Probability coverage states how many cases exposed a complete usable probability distribution; calibration metrics are computed only on those cases. Provider cost is provider-reported when available or computed from recorded token usage and the pricing snapshot stored in the model configuration. Local models have zero provider cost. Estimated local compute cost is only populated when a machine-hour price was explicitly supplied for the run.
