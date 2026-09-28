# Benchmark report: bosun

- Run: `20260927T063229Z-bosun-b4e7d5c4`
- Suite: `perf`
- Cases: 180 (180 valid, 0 errors)
- Accuracy: 51.11%
- Provider cost: $0.000000
- Provider cost / 1M decisions at this case mix: $0.000000
- Estimated local compute cost: $0.000000
- p50 / p95 latency: 306.0396 / 332.8069 ms
- Suite throughput: 12.9103 requests/s

## Primitive results

| Primitive | n | Accuracy | Macro F1 | Brier | NLL | ECE-10 | p50 ms | p95 ms | Provider cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| choice | 60 | 58.33% | 0.4385 | 0.5452 | 1.0958 | 0.1830 | 316.0614 | 341.7642 | $0.000000 |
| noul | 60 | 61.67% | 0.6078 | 0.2435 | 0.7235 | 0.1722 | 299.0297 | 326.1808 | $0.000000 |
| score | 60 | 33.33% | — | 0.8211 | 1.6712 | 0.2512 | 305.0195 | 333.2522 | $0.000000 |

## Domains

| Domain | n | Accuracy | p50 ms | Provider cost |
|---|---:|---:|---:|---:|
| access_governance | 12 | 75.00% | 305.0026 | $0.000000 |
| agent_security | 12 | 50.00% | 322.2153 | $0.000000 |
| compliance | 12 | 25.00% | 303.5742 | $0.000000 |
| content_ops | 12 | 50.00% | 306.0232 | $0.000000 |
| customer_support | 12 | 83.33% | 300.0672 | $0.000000 |
| data_platform | 12 | 83.33% | 300.2586 | $0.000000 |
| ecommerce | 12 | 25.00% | 309.3924 | $0.000000 |
| finance_ops | 12 | 41.67% | 305.6848 | $0.000000 |
| hr_ops | 12 | 75.00% | 304.4069 | $0.000000 |
| it_operations | 12 | 50.00% | 303.2946 | $0.000000 |
| logistics | 12 | 41.67% | 309.9859 | $0.000000 |
| procurement | 12 | 41.67% | 307.1388 | $0.000000 |
| research | 9 | 22.22% | 306.6923 | $0.000000 |
| sales_ops | 9 | 77.78% | 315.9895 | $0.000000 |
| software_delivery | 9 | 44.44% | 314.1606 | $0.000000 |
| workflow_routing | 9 | 22.22% | 306.0415 | $0.000000 |

## Score-specific metrics

- Exact accuracy: 33.33%
- Within ±1 accuracy: 66.67%
- MAE of expected score: 1.0087
- Quadratic weighted kappa: 0.3856

## Interpretation notes

Accuracy and calibration are reported separately from latency and cost. The project intentionally does not collapse them into a single winner score. Provider cost is the billed/request-reported amount when available; local models have zero provider cost. Estimated local compute cost is only populated when a machine-hour price was explicitly supplied for the run.
