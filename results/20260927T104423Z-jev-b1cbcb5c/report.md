# Benchmark report: jev

- Run: `20260927T104423Z-jev-b1cbcb5c`
- Suite: `perf`
- Cases: 180 (180 valid, 0 errors)
- Accuracy: 72.22%
- Provider cost: $0.003096
- Provider cost / 1M decisions at this case mix: $17.202500
- Estimated local compute cost: $0.000000
- p50 / p95 latency: 307.4137 / 410.8536 ms
- Suite throughput: 3.0648 requests/s

## Primitive results

| Primitive | n | Accuracy | Macro F1 | Brier | NLL | ECE-10 | p50 ms | p95 ms | Provider cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| choice | 60 | 96.67% | 0.9524 | 0.0647 | 0.1382 | 0.0595 | 307.1877 | 409.9788 | $0.001166 |
| noul | 60 | 85.00% | 0.8496 | 0.0927 | 0.3039 | 0.0772 | 307.7369 | 409.5535 | $0.000943 |
| score | 60 | 35.00% | — | 0.9384 | 3.1074 | 0.4110 | 307.3655 | 513.0417 | $0.000987 |

## Domains

| Domain | n | Accuracy | p50 ms | Provider cost |
|---|---:|---:|---:|---:|
| access_governance | 12 | 75.00% | 307.5594 | $0.000207 |
| agent_security | 12 | 91.67% | 308.0561 | $0.000228 |
| compliance | 12 | 75.00% | 308.2031 | $0.000204 |
| content_ops | 12 | 83.33% | 307.3145 | $0.000202 |
| customer_support | 12 | 91.67% | 308.1081 | $0.000210 |
| data_platform | 12 | 75.00% | 314.8234 | $0.000207 |
| ecommerce | 12 | 58.33% | 307.7059 | $0.000206 |
| finance_ops | 12 | 75.00% | 307.7076 | $0.000203 |
| hr_ops | 12 | 50.00% | 307.4137 | $0.000205 |
| it_operations | 12 | 75.00% | 306.3829 | $0.000204 |
| logistics | 12 | 66.67% | 306.3693 | $0.000203 |
| procurement | 12 | 75.00% | 307.2646 | $0.000201 |
| research | 9 | 33.33% | 306.4047 | $0.000153 |
| sales_ops | 9 | 100.00% | 307.2370 | $0.000153 |
| software_delivery | 9 | 66.67% | 307.3216 | $0.000154 |
| workflow_routing | 9 | 55.56% | 308.3441 | $0.000156 |

## Score-specific metrics

- Exact accuracy: 35.00%
- Within ±1 accuracy: 86.67%
- MAE of expected score: 0.7507
- Quadratic weighted kappa: 0.7076

## Interpretation notes

Accuracy and calibration are reported separately from latency and cost. The project intentionally does not collapse them into a single winner score. Provider cost is the billed/request-reported amount when available; local models have zero provider cost. Estimated local compute cost is only populated when a machine-hour price was explicitly supplied for the run.
