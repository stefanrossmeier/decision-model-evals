# Benchmark report: julia1

- Run: `20260929T180046Z-julia1-03ca558c`
- Suite: `perf`
- Cases: 180 (180 valid, 0 errors)
- Accuracy: 42.22%
- Provider cost: $0.000000
- Provider cost basis: `not reported`
- Provider cost / 1M decisions at this case mix: $0.000000
- Estimated local compute cost: $0.000000
- p50 / p95 latency: 106.4277 / 115.3455 ms
- Suite throughput: 37.2173 requests/s
- Input / output tokens: — / 0
- Cached input / cache-write / reasoning tokens: — / — / —

## Primitive results

| Primitive | n | Accuracy | Macro F1 | Prob. coverage | Brier | NLL | ECE-10 | p50 ms | p95 ms | Provider cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| choice | 60 | 48.33% | 0.3653 | 100.00% | 0.8186 | 2.5618 | 0.3704 | 107.2296 | 116.5250 | $0.000000 |
| noul | 60 | 60.00% | 0.5996 | 100.00% | 0.3494 | 2.0674 | 0.3504 | 104.4115 | 113.6695 | $0.000000 |
| score | 60 | 18.33% | — | 100.00% | 1.2899 | 3.7638 | 0.5935 | 106.7077 | 113.0986 | $0.000000 |

## Domains

| Domain | n | Accuracy | p50 ms | Provider cost |
|---|---:|---:|---:|---:|
| access_governance | 12 | 33.33% | 105.1998 | $0.000000 |
| agent_security | 12 | 25.00% | 111.7612 | $0.000000 |
| compliance | 12 | 41.67% | 104.8184 | $0.000000 |
| content_ops | 12 | 41.67% | 104.6186 | $0.000000 |
| customer_support | 12 | 50.00% | 107.3812 | $0.000000 |
| data_platform | 12 | 66.67% | 109.8962 | $0.000000 |
| ecommerce | 12 | 41.67% | 107.8599 | $0.000000 |
| finance_ops | 12 | 58.33% | 104.6429 | $0.000000 |
| hr_ops | 12 | 58.33% | 106.4156 | $0.000000 |
| it_operations | 12 | 58.33% | 107.5469 | $0.000000 |
| logistics | 12 | 58.33% | 103.7640 | $0.000000 |
| procurement | 12 | 25.00% | 105.0564 | $0.000000 |
| research | 9 | 22.22% | 105.4475 | $0.000000 |
| sales_ops | 9 | 55.56% | 107.0601 | $0.000000 |
| software_delivery | 9 | 11.11% | 112.3096 | $0.000000 |
| workflow_routing | 9 | 11.11% | 106.0077 | $0.000000 |

## Score-specific metrics

- Exact accuracy: 18.33%
- Within ±1 accuracy: 51.67%
- MAE of selected score: 1.5833
- MAE of expected score: 1.4107
- Quadratic weighted kappa: 0.1059

## Interpretation notes

Accuracy and calibration are reported separately from latency and cost. The project intentionally does not collapse them into a single winner score. Probability coverage states how many cases exposed a complete usable probability distribution; calibration metrics are computed only on those cases. Provider cost is provider-reported when available or computed from recorded token usage and the pricing snapshot stored in the model configuration. Local models have zero provider cost. Estimated local compute cost is only populated when a machine-hour price was explicitly supplied for the run.
