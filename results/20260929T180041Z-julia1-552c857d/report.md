# Benchmark report: julia1

- Run: `20260929T180041Z-julia1-552c857d`
- Suite: `perf`
- Cases: 180 (180 valid, 0 errors)
- Accuracy: 42.22%
- Provider cost: $0.000000
- Provider cost basis: `not reported`
- Provider cost / 1M decisions at this case mix: $0.000000
- Estimated local compute cost: $0.000000
- p50 / p95 latency: 27.3154 / 31.4712 ms
- Suite throughput: 36.1947 requests/s
- Input / output tokens: — / 0
- Cached input / cache-write / reasoning tokens: — / — / —

## Primitive results

| Primitive | n | Accuracy | Macro F1 | Prob. coverage | Brier | NLL | ECE-10 | p50 ms | p95 ms | Provider cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| choice | 60 | 48.33% | 0.3653 | 100.00% | 0.8186 | 2.5618 | 0.3704 | 28.6947 | 36.8578 | $0.000000 |
| noul | 60 | 60.00% | 0.5996 | 100.00% | 0.3494 | 2.0674 | 0.3504 | 25.2489 | 28.2459 | $0.000000 |
| score | 60 | 18.33% | — | 100.00% | 1.2899 | 3.7638 | 0.5935 | 27.1765 | 29.8982 | $0.000000 |

## Domains

| Domain | n | Accuracy | p50 ms | Provider cost |
|---|---:|---:|---:|---:|
| access_governance | 12 | 33.33% | 27.3114 | $0.000000 |
| agent_security | 12 | 25.00% | 30.1955 | $0.000000 |
| compliance | 12 | 41.67% | 27.6699 | $0.000000 |
| content_ops | 12 | 41.67% | 26.9060 | $0.000000 |
| customer_support | 12 | 50.00% | 27.7877 | $0.000000 |
| data_platform | 12 | 66.67% | 27.4670 | $0.000000 |
| ecommerce | 12 | 41.67% | 27.5500 | $0.000000 |
| finance_ops | 12 | 58.33% | 25.8165 | $0.000000 |
| hr_ops | 12 | 58.33% | 26.9896 | $0.000000 |
| it_operations | 12 | 58.33% | 27.1378 | $0.000000 |
| logistics | 12 | 58.33% | 26.5984 | $0.000000 |
| procurement | 12 | 25.00% | 26.4949 | $0.000000 |
| research | 9 | 22.22% | 26.7295 | $0.000000 |
| sales_ops | 9 | 55.56% | 26.8429 | $0.000000 |
| software_delivery | 9 | 11.11% | 27.7569 | $0.000000 |
| workflow_routing | 9 | 11.11% | 27.6133 | $0.000000 |

## Score-specific metrics

- Exact accuracy: 18.33%
- Within ±1 accuracy: 51.67%
- MAE of selected score: 1.5833
- MAE of expected score: 1.4107
- Quadratic weighted kappa: 0.1059

## Interpretation notes

Accuracy and calibration are reported separately from latency and cost. The project intentionally does not collapse them into a single winner score. Probability coverage states how many cases exposed a complete usable probability distribution; calibration metrics are computed only on those cases. Provider cost is provider-reported when available or computed from recorded token usage and the pricing snapshot stored in the model configuration. Local models have zero provider cost. Estimated local compute cost is only populated when a machine-hour price was explicitly supplied for the run.
