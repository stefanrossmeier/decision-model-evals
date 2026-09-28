# Benchmark report: jev

- Run: `20260927T104536Z-jev-a5668f4b`
- Suite: `perf`
- Cases: 180 (180 valid, 0 errors)
- Accuracy: 71.67%
- Provider cost: $0.003096
- Provider cost / 1M decisions at this case mix: $17.202500
- Estimated local compute cost: $0.000000
- p50 / p95 latency: 286.4887 / 853.1746 ms
- Suite throughput: 44.3334 requests/s

## Primitive results

| Primitive | n | Accuracy | Macro F1 | Brier | NLL | ECE-10 | p50 ms | p95 ms | Provider cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| choice | 60 | 96.67% | 0.9524 | 0.0667 | 0.1422 | 0.0612 | 285.6529 | 870.5244 | $0.001166 |
| noul | 60 | 83.33% | 0.8326 | 0.0926 | 0.3030 | 0.0955 | 284.6638 | 823.3155 | $0.000943 |
| score | 60 | 35.00% | — | 0.9471 | 2.7251 | 0.4398 | 288.9310 | 766.9060 | $0.000987 |

## Domains

| Domain | n | Accuracy | p50 ms | Provider cost |
|---|---:|---:|---:|---:|
| access_governance | 12 | 75.00% | 276.2165 | $0.000207 |
| agent_security | 12 | 91.67% | 292.5981 | $0.000228 |
| compliance | 12 | 75.00% | 260.4189 | $0.000204 |
| content_ops | 12 | 83.33% | 280.9016 | $0.000202 |
| customer_support | 12 | 83.33% | 288.4604 | $0.000210 |
| data_platform | 12 | 75.00% | 331.5978 | $0.000207 |
| ecommerce | 12 | 58.33% | 281.9474 | $0.000206 |
| finance_ops | 12 | 75.00% | 316.8803 | $0.000203 |
| hr_ops | 12 | 58.33% | 281.6714 | $0.000205 |
| it_operations | 12 | 75.00% | 275.5184 | $0.000204 |
| logistics | 12 | 58.33% | 301.0634 | $0.000203 |
| procurement | 12 | 75.00% | 269.0626 | $0.000201 |
| research | 9 | 33.33% | 293.7131 | $0.000153 |
| sales_ops | 9 | 100.00% | 305.3554 | $0.000153 |
| software_delivery | 9 | 66.67% | 278.2868 | $0.000154 |
| workflow_routing | 9 | 55.56% | 271.0671 | $0.000156 |

## Score-specific metrics

- Exact accuracy: 35.00%
- Within ±1 accuracy: 86.67%
- MAE of expected score: 0.7605
- Quadratic weighted kappa: 0.7125

## Interpretation notes

Accuracy and calibration are reported separately from latency and cost. The project intentionally does not collapse them into a single winner score. Provider cost is the billed/request-reported amount when available; local models have zero provider cost. Estimated local compute cost is only populated when a machine-hour price was explicitly supplied for the run.
