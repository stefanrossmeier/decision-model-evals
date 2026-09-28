# Benchmark report: luna-classifier

- Run: `20260928T062221Z-luna-classifier-60e0d309`
- Suite: `full`
- Cases: 5760 (5760 valid, 0 errors)
- Accuracy: 73.14%
- Provider cost: $0.170873
- Provider cost basis: `provider_reported`
- Provider cost / 1M decisions at this case mix: $29.665417
- Estimated local compute cost: $0.000000
- p50 / p95 latency: 938.0543 / 1434.8083 ms
- Suite throughput: 0.9474 requests/s
- Input / output tokens: 1,324,728 / 76,800
- Cached input / cache-write / reasoning tokens: 0 / 0 / 0

## Primitive results

| Primitive | n | Accuracy | Macro F1 | Prob. coverage | Brier | NLL | ECE-10 | p50 ms | p95 ms | Provider cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| choice | 1920 | 95.31% | 0.9521 | 0.00% | — | — | — | 979.2192 | 1638.1819 | $0.060982 |
| noul | 1920 | 85.26% | 0.8513 | 0.00% | — | — | — | 1022.9820 | 1401.0785 | $0.052114 |
| score | 1920 | 38.85% | — | 0.00% | — | — | — | 920.2274 | 1349.9672 | $0.057778 |

## Domains

| Domain | n | Accuracy | p50 ms | Provider cost |
|---|---:|---:|---:|---:|
| access_governance | 360 | 71.39% | 921.0925 | $0.010747 |
| agent_security | 360 | 79.17% | 1022.4888 | $0.011963 |
| compliance | 360 | 67.78% | 960.0860 | $0.010456 |
| content_ops | 360 | 77.50% | 982.3406 | $0.010353 |
| customer_support | 360 | 80.28% | 1003.0245 | $0.010820 |
| data_platform | 360 | 77.78% | 983.6019 | $0.010745 |
| ecommerce | 360 | 65.28% | 926.1770 | $0.010661 |
| finance_ops | 360 | 76.94% | 944.2495 | $0.010453 |
| hr_ops | 360 | 62.22% | 920.1584 | $0.010523 |
| it_operations | 360 | 69.72% | 922.5398 | $0.010630 |
| logistics | 360 | 61.94% | 941.7828 | $0.010477 |
| procurement | 360 | 81.11% | 986.6168 | $0.010346 |
| research | 360 | 69.17% | 945.9691 | $0.010629 |
| sales_ops | 360 | 73.89% | 965.6345 | $0.010599 |
| software_delivery | 360 | 78.61% | 922.9014 | $0.010607 |
| workflow_routing | 360 | 77.50% | 942.7997 | $0.010863 |

## Score-specific metrics

- Exact accuracy: 38.85%
- Within ±1 accuracy: 86.56%
- MAE of selected score: 0.7557
- MAE of expected score: —
- Quadratic weighted kappa: 0.7111

## Interpretation notes

Accuracy and calibration are reported separately from latency and cost. The project intentionally does not collapse them into a single winner score. Probability coverage states how many cases exposed a complete usable probability distribution; calibration metrics are computed only on those cases. Provider cost is provider-reported when available or computed from recorded token usage and the pricing snapshot stored in the model configuration. Local models have zero provider cost. Estimated local compute cost is only populated when a machine-hour price was explicitly supplied for the run.
