# Benchmark report: luna-structured

- Run: `20260928T083041Z-luna-structured-9dd51ac9`
- Suite: `perf`
- Cases: 180 (180 valid, 0 errors)
- Accuracy: 71.67%
- Provider cost: $0.004927
- Provider cost basis: `provider_reported`
- Provider cost / 1M decisions at this case mix: $27.373333
- Estimated local compute cost: $0.000000
- p50 / p95 latency: 1009.9215 / 1228.1780 ms
- Suite throughput: 0.9878 requests/s
- Input / output tokens: 37,002 / 2,454
- Cached input / cache-write / reasoning tokens: 0 / 0 / 0

## Primitive results

| Primitive | n | Accuracy | Macro F1 | Prob. coverage | Brier | NLL | ECE-10 | p50 ms | p95 ms | Provider cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| choice | 60 | 90.00% | 0.8348 | 0.00% | — | — | — | 1023.8127 | 1277.7600 | $0.001853 |
| noul | 60 | 86.67% | 0.8643 | 0.00% | — | — | — | 987.4702 | 1155.0240 | $0.001509 |
| score | 60 | 38.33% | — | 0.00% | — | — | — | 977.0146 | 1137.2805 | $0.001565 |

## Domains

| Domain | n | Accuracy | p50 ms | Provider cost |
|---|---:|---:|---:|---:|
| access_governance | 12 | 83.33% | 991.7250 | $0.000331 |
| agent_security | 12 | 83.33% | 1001.4250 | $0.000381 |
| compliance | 12 | 75.00% | 1013.7666 | $0.000324 |
| content_ops | 12 | 83.33% | 1008.0432 | $0.000317 |
| customer_support | 12 | 91.67% | 1024.4805 | $0.000333 |
| data_platform | 12 | 75.00% | 957.0117 | $0.000328 |
| ecommerce | 12 | 41.67% | 916.8662 | $0.000326 |
| finance_ops | 12 | 75.00% | 1013.0343 | $0.000324 |
| hr_ops | 12 | 50.00% | 1022.2787 | $0.000327 |
| it_operations | 12 | 58.33% | 1022.0355 | $0.000320 |
| logistics | 12 | 41.67% | 1024.1898 | $0.000318 |
| procurement | 12 | 83.33% | 937.0834 | $0.000316 |
| research | 9 | 66.67% | 1022.6266 | $0.000243 |
| sales_ops | 9 | 100.00% | 922.7065 | $0.000246 |
| software_delivery | 9 | 66.67% | 1029.4816 | $0.000244 |
| workflow_routing | 9 | 77.78% | 1025.0663 | $0.000249 |

## Score-specific metrics

- Exact accuracy: 38.33%
- Within ±1 accuracy: 85.00%
- MAE of selected score: 0.7667
- MAE of expected score: —
- Quadratic weighted kappa: 0.7013

## Interpretation notes

Accuracy and calibration are reported separately from latency and cost. The project intentionally does not collapse them into a single winner score. Probability coverage states how many cases exposed a complete usable probability distribution; calibration metrics are computed only on those cases. Provider cost is provider-reported when available or computed from recorded token usage and the pricing snapshot stored in the model configuration. Local models have zero provider cost. Estimated local compute cost is only populated when a machine-hour price was explicitly supplied for the run.
