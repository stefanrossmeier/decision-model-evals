# Benchmark report: jev

- Run: `20260927T104522Z-jev-078238e3`
- Suite: `perf`
- Cases: 180 (180 valid, 0 errors)
- Accuracy: 72.78%
- Provider cost: $0.003096
- Provider cost / 1M decisions at this case mix: $17.202500
- Estimated local compute cost: $0.000000
- p50 / p95 latency: 291.3344 / 435.9734 ms
- Suite throughput: 12.7480 requests/s

## Primitive results

| Primitive | n | Accuracy | Macro F1 | Brier | NLL | ECE-10 | p50 ms | p95 ms | Provider cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| choice | 60 | 96.67% | 0.9524 | 0.0659 | 0.1405 | 0.0602 | 304.7151 | 473.8863 | $0.001166 |
| noul | 60 | 85.00% | 0.8496 | 0.0923 | 0.3027 | 0.0765 | 289.0437 | 346.4076 | $0.000943 |
| score | 60 | 36.67% | — | 0.9365 | 2.7058 | 0.4215 | 288.1676 | 410.5994 | $0.000987 |

## Domains

| Domain | n | Accuracy | p50 ms | Provider cost |
|---|---:|---:|---:|---:|
| access_governance | 12 | 75.00% | 300.9848 | $0.000207 |
| agent_security | 12 | 91.67% | 288.9710 | $0.000228 |
| compliance | 12 | 75.00% | 285.9558 | $0.000204 |
| content_ops | 12 | 83.33% | 255.4764 | $0.000202 |
| customer_support | 12 | 91.67% | 287.3161 | $0.000210 |
| data_platform | 12 | 75.00% | 298.6448 | $0.000207 |
| ecommerce | 12 | 58.33% | 277.1632 | $0.000206 |
| finance_ops | 12 | 75.00% | 302.2013 | $0.000203 |
| hr_ops | 12 | 58.33% | 307.5771 | $0.000205 |
| it_operations | 12 | 75.00% | 290.4973 | $0.000204 |
| logistics | 12 | 66.67% | 316.2403 | $0.000203 |
| procurement | 12 | 75.00% | 310.4251 | $0.000201 |
| research | 9 | 33.33% | 265.0612 | $0.000153 |
| sales_ops | 9 | 100.00% | 276.0608 | $0.000153 |
| software_delivery | 9 | 66.67% | 291.6504 | $0.000154 |
| workflow_routing | 9 | 55.56% | 271.7010 | $0.000156 |

## Score-specific metrics

- Exact accuracy: 36.67%
- Within ±1 accuracy: 86.67%
- MAE of expected score: 0.7480
- Quadratic weighted kappa: 0.7169

## Interpretation notes

Accuracy and calibration are reported separately from latency and cost. The project intentionally does not collapse them into a single winner score. Provider cost is the billed/request-reported amount when available; local models have zero provider cost. Estimated local compute cost is only populated when a machine-hour price was explicitly supplied for the run.
