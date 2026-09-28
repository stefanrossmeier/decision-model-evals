# Benchmark report: decider

- Run: `20260927T080208Z-decider-996ff5f3`
- Suite: `perf`
- Cases: 180 (180 valid, 0 errors)
- Accuracy: 70.00%
- Provider cost: $0.000000
- Provider cost / 1M decisions at this case mix: $0.000000
- Estimated local compute cost: $0.000000
- p50 / p95 latency: 7584.3209 / 10999.6210 ms
- Suite throughput: 2.0938 requests/s

## Primitive results

| Primitive | n | Accuracy | Macro F1 | Brier | NLL | ECE-10 | p50 ms | p95 ms | Provider cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| choice | 60 | 88.33% | 0.8481 | 0.2063 | 0.3650 | 0.0804 | 4756.1371 | 7882.2386 | $0.000000 |
| noul | 60 | 93.33% | 0.9327 | 0.0869 | 0.3151 | 0.0956 | 8336.0345 | 10307.9971 | $0.000000 |
| score | 60 | 28.33% | — | 0.7790 | 1.5415 | 0.2110 | 8793.5106 | 11042.8013 | $0.000000 |

## Domains

| Domain | n | Accuracy | p50 ms | Provider cost |
|---|---:|---:|---:|---:|
| access_governance | 12 | 75.00% | 7111.8221 | $0.000000 |
| agent_security | 12 | 58.33% | 6797.3312 | $0.000000 |
| compliance | 12 | 58.33% | 6322.5526 | $0.000000 |
| content_ops | 12 | 75.00% | 7067.8122 | $0.000000 |
| customer_support | 12 | 91.67% | 8080.1883 | $0.000000 |
| data_platform | 12 | 66.67% | 7585.2660 | $0.000000 |
| ecommerce | 12 | 58.33% | 7042.6024 | $0.000000 |
| finance_ops | 12 | 75.00% | 7313.6577 | $0.000000 |
| hr_ops | 12 | 58.33% | 7265.6729 | $0.000000 |
| it_operations | 12 | 66.67% | 8080.3362 | $0.000000 |
| logistics | 12 | 66.67% | 7313.5983 | $0.000000 |
| procurement | 12 | 75.00% | 8568.2073 | $0.000000 |
| research | 9 | 55.56% | 8422.3745 | $0.000000 |
| sales_ops | 9 | 100.00% | 8870.8510 | $0.000000 |
| software_delivery | 9 | 66.67% | 7762.8283 | $0.000000 |
| workflow_routing | 9 | 77.78% | 7825.5321 | $0.000000 |

## Score-specific metrics

- Exact accuracy: 28.33%
- Within ±1 accuracy: 83.33%
- MAE of expected score: 0.9268
- Quadratic weighted kappa: 0.6259

## Interpretation notes

Accuracy and calibration are reported separately from latency and cost. The project intentionally does not collapse them into a single winner score. Provider cost is the billed/request-reported amount when available; local models have zero provider cost. Estimated local compute cost is only populated when a machine-hour price was explicitly supplied for the run.
