# Benchmark report: semif

- Run: `20260927T084306Z-semif-ca2dfa66`
- Suite: `full`
- Cases: 5760 (5760 valid, 0 errors)
- Accuracy: 66.42%
- Provider cost: $0.000000
- Provider cost / 1M decisions at this case mix: $0.000000
- Estimated local compute cost: $0.000000
- p50 / p95 latency: 711.4624 / 745.2912 ms
- Suite throughput: 1.5209 requests/s

## Primitive results

| Primitive | n | Accuracy | Macro F1 | Brier | NLL | ECE-10 | p50 ms | p95 ms | Provider cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| choice | 1920 | 85.36% | 0.8530 | 0.2302 | 0.4548 | 0.0497 | 736.7116 | 927.7529 | $0.000000 |
| noul | 1920 | 75.68% | 0.7471 | 0.1765 | 0.5550 | 0.0980 | 553.1596 | 557.0247 | $0.000000 |
| score | 1920 | 38.23% | — | 0.7829 | 1.6105 | 0.2150 | 711.8063 | 738.7780 | $0.000000 |

## Domains

| Domain | n | Accuracy | p50 ms | Provider cost |
|---|---:|---:|---:|---:|
| access_governance | 360 | 64.17% | 713.5217 | $0.000000 |
| agent_security | 360 | 60.28% | 741.7008 | $0.000000 |
| compliance | 360 | 52.50% | 570.5812 | $0.000000 |
| content_ops | 360 | 72.22% | 709.0167 | $0.000000 |
| customer_support | 360 | 79.44% | 713.6869 | $0.000000 |
| data_platform | 360 | 69.72% | 713.8097 | $0.000000 |
| ecommerce | 360 | 66.11% | 712.7438 | $0.000000 |
| finance_ops | 360 | 70.83% | 571.2622 | $0.000000 |
| hr_ops | 360 | 63.33% | 706.9699 | $0.000000 |
| it_operations | 360 | 72.22% | 711.8512 | $0.000000 |
| logistics | 360 | 63.06% | 571.4695 | $0.000000 |
| procurement | 360 | 70.00% | 570.4902 | $0.000000 |
| research | 360 | 51.67% | 710.0174 | $0.000000 |
| sales_ops | 360 | 60.28% | 713.5600 | $0.000000 |
| software_delivery | 360 | 81.11% | 713.7377 | $0.000000 |
| workflow_routing | 360 | 65.83% | 725.7239 | $0.000000 |

## Score-specific metrics

- Exact accuracy: 38.23%
- Within ±1 accuracy: 76.51%
- MAE of expected score: 0.8596
- Quadratic weighted kappa: 0.5803

## Interpretation notes

Accuracy and calibration are reported separately from latency and cost. The project intentionally does not collapse them into a single winner score. Provider cost is the billed/request-reported amount when available; local models have zero provider cost. Estimated local compute cost is only populated when a machine-hour price was explicitly supplied for the run.
