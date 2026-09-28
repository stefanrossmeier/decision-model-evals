# Benchmark report: decider

- Run: `20260927T071225Z-decider-0b81b9b4`
- Suite: `full`
- Cases: 5760 (5760 valid, 0 errors)
- Accuracy: 69.81%
- Provider cost: $0.000000
- Provider cost / 1M decisions at this case mix: $0.000000
- Estimated local compute cost: $0.000000
- p50 / p95 latency: 297.0824 / 938.4843 ms
- Suite throughput: 2.0589 requests/s

## Primitive results

| Primitive | n | Accuracy | Macro F1 | Brier | NLL | ECE-10 | p50 ms | p95 ms | Provider cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| choice | 1920 | 87.29% | 0.8779 | 0.1876 | 0.3533 | 0.0258 | 297.0824 | 382.7941 | $0.000000 |
| noul | 1920 | 84.74% | 0.8463 | 0.1210 | 0.3962 | 0.0508 | 212.0246 | 215.0092 | $0.000000 |
| score | 1920 | 37.40% | — | 0.7426 | 1.4519 | 0.1069 | 937.5057 | 939.6710 | $0.000000 |

## Domains

| Domain | n | Accuracy | p50 ms | Provider cost |
|---|---:|---:|---:|---:|
| access_governance | 360 | 55.56% | 297.7824 | $0.000000 |
| agent_security | 360 | 60.28% | 383.4688 | $0.000000 |
| compliance | 360 | 59.72% | 297.8632 | $0.000000 |
| content_ops | 360 | 77.22% | 296.7124 | $0.000000 |
| customer_support | 360 | 81.94% | 296.9353 | $0.000000 |
| data_platform | 360 | 70.00% | 296.5382 | $0.000000 |
| ecommerce | 360 | 65.56% | 296.9817 | $0.000000 |
| finance_ops | 360 | 75.28% | 296.7908 | $0.000000 |
| hr_ops | 360 | 63.33% | 298.1145 | $0.000000 |
| it_operations | 360 | 71.39% | 296.5666 | $0.000000 |
| logistics | 360 | 72.50% | 296.7496 | $0.000000 |
| procurement | 360 | 71.67% | 296.5881 | $0.000000 |
| research | 360 | 60.83% | 296.9128 | $0.000000 |
| sales_ops | 360 | 78.06% | 297.4431 | $0.000000 |
| software_delivery | 360 | 79.17% | 296.6584 | $0.000000 |
| workflow_routing | 360 | 74.44% | 297.3101 | $0.000000 |

## Score-specific metrics

- Exact accuracy: 37.40%
- Within ±1 accuracy: 82.81%
- MAE of expected score: 0.8467
- Quadratic weighted kappa: 0.6203

## Interpretation notes

Accuracy and calibration are reported separately from latency and cost. The project intentionally does not collapse them into a single winner score. Provider cost is the billed/request-reported amount when available; local models have zero provider cost. Estimated local compute cost is only populated when a machine-hour price was explicitly supplied for the run.
