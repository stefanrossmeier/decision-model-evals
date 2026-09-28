# Benchmark report: decider

- Run: `20260927T075903Z-decider-a8745886`
- Suite: `perf`
- Cases: 180 (180 valid, 0 errors)
- Accuracy: 70.00%
- Provider cost: $0.000000
- Provider cost / 1M decisions at this case mix: $0.000000
- Estimated local compute cost: $0.000000
- p50 / p95 latency: 296.3427 / 938.5853 ms
- Suite throughput: 2.0457 requests/s

## Primitive results

| Primitive | n | Accuracy | Macro F1 | Brier | NLL | ECE-10 | p50 ms | p95 ms | Provider cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| choice | 60 | 88.33% | 0.8481 | 0.2065 | 0.3652 | 0.0803 | 296.3427 | 382.3766 | $0.000000 |
| noul | 60 | 93.33% | 0.9327 | 0.0869 | 0.3149 | 0.0956 | 212.8718 | 215.9317 | $0.000000 |
| score | 60 | 28.33% | — | 0.7790 | 1.5415 | 0.2110 | 937.5465 | 939.7296 | $0.000000 |

## Domains

| Domain | n | Accuracy | p50 ms | Provider cost |
|---|---:|---:|---:|---:|
| access_governance | 12 | 75.00% | 293.2812 | $0.000000 |
| agent_security | 12 | 58.33% | 383.9703 | $0.000000 |
| compliance | 12 | 58.33% | 297.3630 | $0.000000 |
| content_ops | 12 | 75.00% | 298.1039 | $0.000000 |
| customer_support | 12 | 91.67% | 298.0620 | $0.000000 |
| data_platform | 12 | 66.67% | 297.5484 | $0.000000 |
| ecommerce | 12 | 58.33% | 296.1215 | $0.000000 |
| finance_ops | 12 | 75.00% | 297.3089 | $0.000000 |
| hr_ops | 12 | 58.33% | 297.3501 | $0.000000 |
| it_operations | 12 | 66.67% | 297.1704 | $0.000000 |
| logistics | 12 | 66.67% | 293.5527 | $0.000000 |
| procurement | 12 | 75.00% | 293.2772 | $0.000000 |
| research | 9 | 55.56% | 295.3844 | $0.000000 |
| sales_ops | 9 | 100.00% | 292.0979 | $0.000000 |
| software_delivery | 9 | 66.67% | 295.0668 | $0.000000 |
| workflow_routing | 9 | 77.78% | 292.2033 | $0.000000 |

## Score-specific metrics

- Exact accuracy: 28.33%
- Within ±1 accuracy: 83.33%
- MAE of expected score: 0.9273
- Quadratic weighted kappa: 0.6259

## Interpretation notes

Accuracy and calibration are reported separately from latency and cost. The project intentionally does not collapse them into a single winner score. Provider cost is the billed/request-reported amount when available; local models have zero provider cost. Estimated local compute cost is only populated when a machine-hour price was explicitly supplied for the run.
