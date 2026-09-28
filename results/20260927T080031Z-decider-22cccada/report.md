# Benchmark report: decider

- Run: `20260927T080031Z-decider-22cccada`
- Suite: `perf`
- Cases: 180 (180 valid, 0 errors)
- Accuracy: 70.00%
- Provider cost: $0.000000
- Provider cost / 1M decisions at this case mix: $0.000000
- Estimated local compute cost: $0.000000
- p50 / p95 latency: 2257.2748 / 3574.4511 ms
- Suite throughput: 1.8582 requests/s

## Primitive results

| Primitive | n | Accuracy | Macro F1 | Brier | NLL | ECE-10 | p50 ms | p95 ms | Provider cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| choice | 60 | 88.33% | 0.8481 | 0.2064 | 0.3651 | 0.0803 | 2252.5454 | 3398.5274 | $0.000000 |
| noul | 60 | 93.33% | 0.9327 | 0.0870 | 0.3151 | 0.0956 | 1718.9046 | 2644.3719 | $0.000000 |
| score | 60 | 28.33% | — | 0.7790 | 1.5415 | 0.2110 | 2462.4972 | 3748.2689 | $0.000000 |

## Domains

| Domain | n | Accuracy | p50 ms | Provider cost |
|---|---:|---:|---:|---:|
| access_governance | 12 | 75.00% | 2073.3492 | $0.000000 |
| agent_security | 12 | 58.33% | 2169.3022 | $0.000000 |
| compliance | 12 | 58.33% | 2257.8844 | $0.000000 |
| content_ops | 12 | 75.00% | 2096.5422 | $0.000000 |
| customer_support | 12 | 91.67% | 2262.2781 | $0.000000 |
| data_platform | 12 | 66.67% | 2024.4172 | $0.000000 |
| ecommerce | 12 | 58.33% | 1682.9017 | $0.000000 |
| finance_ops | 12 | 75.00% | 1906.8754 | $0.000000 |
| hr_ops | 12 | 58.33% | 2287.1211 | $0.000000 |
| it_operations | 12 | 66.67% | 2355.9851 | $0.000000 |
| logistics | 12 | 66.67% | 1798.8281 | $0.000000 |
| procurement | 12 | 75.00% | 2262.9921 | $0.000000 |
| research | 9 | 55.56% | 2268.8439 | $0.000000 |
| sales_ops | 9 | 100.00% | 2257.8840 | $0.000000 |
| software_delivery | 9 | 66.67% | 2350.8301 | $0.000000 |
| workflow_routing | 9 | 77.78% | 2257.8660 | $0.000000 |

## Score-specific metrics

- Exact accuracy: 28.33%
- Within ±1 accuracy: 83.33%
- MAE of expected score: 0.9272
- Quadratic weighted kappa: 0.6259

## Interpretation notes

Accuracy and calibration are reported separately from latency and cost. The project intentionally does not collapse them into a single winner score. Provider cost is the billed/request-reported amount when available; local models have zero provider cost. Estimated local compute cost is only populated when a machine-hour price was explicitly supplied for the run.
