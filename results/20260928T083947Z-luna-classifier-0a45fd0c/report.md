# Benchmark report: luna-classifier

- Run: `20260928T083947Z-luna-classifier-0a45fd0c`
- Suite: `perf`
- Cases: 180 (180 valid, 0 errors)
- Accuracy: 71.67%
- Provider cost: $0.005341
- Provider cost basis: `provider_reported`
- Provider cost / 1M decisions at this case mix: $29.673889
- Estimated local compute cost: $0.000000
- p50 / p95 latency: 925.6677 / 2190.0607 ms
- Suite throughput: 5.5168 requests/s
- Input / output tokens: 41,413 / 2,400
- Cached input / cache-write / reasoning tokens: 0 / 0 / 0

## Primitive results

| Primitive | n | Accuracy | Macro F1 | Prob. coverage | Brier | NLL | ECE-10 | p50 ms | p95 ms | Provider cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| choice | 60 | 91.67% | 0.8620 | 0.00% | — | — | — | 964.4417 | 2463.7764 | $0.001909 |
| noul | 60 | 83.33% | 0.8286 | 0.00% | — | — | — | 974.3219 | 1348.1320 | $0.001629 |
| score | 60 | 40.00% | — | 0.00% | — | — | — | 817.1398 | 1433.1132 | $0.001803 |

## Domains

| Domain | n | Accuracy | p50 ms | Provider cost |
|---|---:|---:|---:|---:|
| access_governance | 12 | 75.00% | 943.7762 | $0.000357 |
| agent_security | 12 | 83.33% | 953.5967 | $0.000400 |
| compliance | 12 | 66.67% | 950.2332 | $0.000352 |
| content_ops | 12 | 91.67% | 883.2285 | $0.000347 |
| customer_support | 12 | 83.33% | 975.6899 | $0.000362 |
| data_platform | 12 | 91.67% | 938.7486 | $0.000358 |
| ecommerce | 12 | 41.67% | 895.9514 | $0.000356 |
| finance_ops | 12 | 66.67% | 916.7190 | $0.000349 |
| hr_ops | 12 | 58.33% | 947.8660 | $0.000352 |
| it_operations | 12 | 75.00% | 906.2662 | $0.000352 |
| logistics | 12 | 41.67% | 874.8108 | $0.000349 |
| procurement | 12 | 75.00% | 1023.4086 | $0.000345 |
| research | 9 | 55.56% | 921.2542 | $0.000264 |
| sales_ops | 9 | 100.00% | 1052.9827 | $0.000264 |
| software_delivery | 9 | 66.67% | 891.6177 | $0.000266 |
| workflow_routing | 9 | 77.78% | 901.5893 | $0.000271 |

## Score-specific metrics

- Exact accuracy: 40.00%
- Within ±1 accuracy: 85.00%
- MAE of selected score: 0.7667
- MAE of expected score: —
- Quadratic weighted kappa: 0.7193

## Interpretation notes

Accuracy and calibration are reported separately from latency and cost. The project intentionally does not collapse them into a single winner score. Probability coverage states how many cases exposed a complete usable probability distribution; calibration metrics are computed only on those cases. Provider cost is provider-reported when available or computed from recorded token usage and the pricing snapshot stored in the model configuration. Local models have zero provider cost. Estimated local compute cost is only populated when a machine-hour price was explicitly supplied for the run.
