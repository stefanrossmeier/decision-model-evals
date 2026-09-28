# Benchmark report: semif

- Run: `20260927T095010Z-semif-25201782`
- Suite: `perf`
- Cases: 180 (180 valid, 0 errors)
- Accuracy: 66.11%
- Provider cost: $0.000000
- Provider cost / 1M decisions at this case mix: $0.000000
- Estimated local compute cost: $0.000000
- p50 / p95 latency: 10413.8398 / 11163.1515 ms
- Suite throughput: 1.5203 requests/s

## Primitive results

| Primitive | n | Accuracy | Macro F1 | Brier | NLL | ECE-10 | p50 ms | p95 ms | Provider cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| choice | 60 | 88.33% | 0.8492 | 0.1935 | 0.4285 | 0.0540 | 10503.3426 | 11178.7194 | $0.000000 |
| noul | 60 | 78.33% | 0.7689 | 0.1500 | 0.4667 | 0.0698 | 10251.4470 | 11019.9819 | $0.000000 |
| score | 60 | 31.67% | — | 0.8504 | 1.7516 | 0.3018 | 10455.5947 | 11151.1289 | $0.000000 |

## Domains

| Domain | n | Accuracy | p50 ms | Provider cost |
|---|---:|---:|---:|---:|
| access_governance | 12 | 75.00% | 10244.8353 | $0.000000 |
| agent_security | 12 | 58.33% | 10509.6299 | $0.000000 |
| compliance | 12 | 33.33% | 10264.2038 | $0.000000 |
| content_ops | 12 | 83.33% | 10535.7087 | $0.000000 |
| customer_support | 12 | 83.33% | 10559.4994 | $0.000000 |
| data_platform | 12 | 83.33% | 10422.4076 | $0.000000 |
| ecommerce | 12 | 50.00% | 10172.1592 | $0.000000 |
| finance_ops | 12 | 66.67% | 10160.7768 | $0.000000 |
| hr_ops | 12 | 50.00% | 10362.5080 | $0.000000 |
| it_operations | 12 | 75.00% | 10476.7065 | $0.000000 |
| logistics | 12 | 58.33% | 10025.0643 | $0.000000 |
| procurement | 12 | 66.67% | 10411.8301 | $0.000000 |
| research | 9 | 44.44% | 10460.1606 | $0.000000 |
| sales_ops | 9 | 88.89% | 10390.8323 | $0.000000 |
| software_delivery | 9 | 77.78% | 10760.1495 | $0.000000 |
| workflow_routing | 9 | 66.67% | 10467.8732 | $0.000000 |

## Score-specific metrics

- Exact accuracy: 31.67%
- Within ±1 accuracy: 71.67%
- MAE of expected score: 0.9170
- Quadratic weighted kappa: 0.5951

## Interpretation notes

Accuracy and calibration are reported separately from latency and cost. The project intentionally does not collapse them into a single winner score. Provider cost is the billed/request-reported amount when available; local models have zero provider cost. Estimated local compute cost is only populated when a machine-hour price was explicitly supplied for the run.
