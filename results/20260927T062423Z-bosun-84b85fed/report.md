# Benchmark report: bosun

- Run: `20260927T062423Z-bosun-84b85fed`
- Suite: `full`
- Cases: 5760 (5760 valid, 0 errors)
- Accuracy: 54.93%
- Provider cost: $0.000000
- Provider cost / 1M decisions at this case mix: $0.000000
- Estimated local compute cost: $0.000000
- p50 / p95 latency: 78.6727 / 92.6882 ms
- Suite throughput: 12.2253 requests/s

## Primitive results

| Primitive | n | Accuracy | Macro F1 | Brier | NLL | ECE-10 | p50 ms | p95 ms | Provider cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| choice | 1920 | 66.51% | 0.6457 | 0.4814 | 0.9943 | 0.1062 | 90.2724 | 102.9613 | $0.000000 |
| noul | 1920 | 64.90% | 0.6488 | 0.2410 | 0.7010 | 0.1399 | 76.0405 | 78.6002 | $0.000000 |
| score | 1920 | 33.39% | — | 0.8410 | 1.6777 | 0.2466 | 78.4507 | 85.8660 | $0.000000 |

## Domains

| Domain | n | Accuracy | p50 ms | Provider cost |
|---|---:|---:|---:|---:|
| access_governance | 360 | 56.67% | 78.8993 | $0.000000 |
| agent_security | 360 | 60.00% | 86.8305 | $0.000000 |
| compliance | 360 | 52.78% | 77.6285 | $0.000000 |
| content_ops | 360 | 62.78% | 78.1445 | $0.000000 |
| customer_support | 360 | 75.28% | 79.5321 | $0.000000 |
| data_platform | 360 | 65.00% | 79.1125 | $0.000000 |
| ecommerce | 360 | 25.00% | 78.5794 | $0.000000 |
| finance_ops | 360 | 61.94% | 77.3143 | $0.000000 |
| hr_ops | 360 | 62.50% | 77.9562 | $0.000000 |
| it_operations | 360 | 57.22% | 78.3907 | $0.000000 |
| logistics | 360 | 45.28% | 77.6706 | $0.000000 |
| procurement | 360 | 56.11% | 76.8070 | $0.000000 |
| research | 360 | 41.39% | 78.6390 | $0.000000 |
| sales_ops | 360 | 54.72% | 79.6617 | $0.000000 |
| software_delivery | 360 | 62.50% | 82.3021 | $0.000000 |
| workflow_routing | 360 | 39.72% | 83.0288 | $0.000000 |

## Score-specific metrics

- Exact accuracy: 33.39%
- Within ±1 accuracy: 65.47%
- MAE of expected score: 0.9995
- Quadratic weighted kappa: 0.3475

## Interpretation notes

Accuracy and calibration are reported separately from latency and cost. The project intentionally does not collapse them into a single winner score. Provider cost is the billed/request-reported amount when available; local models have zero provider cost. Estimated local compute cost is only populated when a machine-hour price was explicitly supplied for the run.
