# Benchmark report: semif

- Run: `20260927T094613Z-semif-e74d753c`
- Suite: `perf`
- Cases: 180 (180 valid, 0 errors)
- Accuracy: 66.11%
- Provider cost: $0.000000
- Provider cost / 1M decisions at this case mix: $0.000000
- Estimated local compute cost: $0.000000
- p50 / p95 latency: 712.2894 / 744.1790 ms
- Suite throughput: 1.5185 requests/s

## Primitive results

| Primitive | n | Accuracy | Macro F1 | Brier | NLL | ECE-10 | p50 ms | p95 ms | Provider cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| choice | 60 | 88.33% | 0.8492 | 0.1935 | 0.4285 | 0.0540 | 736.4422 | 926.2762 | $0.000000 |
| noul | 60 | 78.33% | 0.7689 | 0.1500 | 0.4667 | 0.0698 | 552.2854 | 556.4064 | $0.000000 |
| score | 60 | 31.67% | — | 0.8504 | 1.7516 | 0.3018 | 712.2894 | 736.0414 | $0.000000 |

## Domains

| Domain | n | Accuracy | p50 ms | Provider cost |
|---|---:|---:|---:|---:|
| access_governance | 12 | 75.00% | 710.7447 | $0.000000 |
| agent_security | 12 | 58.33% | 740.4843 | $0.000000 |
| compliance | 12 | 33.33% | 639.6052 | $0.000000 |
| content_ops | 12 | 83.33% | 713.2495 | $0.000000 |
| customer_support | 12 | 83.33% | 715.0167 | $0.000000 |
| data_platform | 12 | 83.33% | 712.0442 | $0.000000 |
| ecommerce | 12 | 50.00% | 710.1667 | $0.000000 |
| finance_ops | 12 | 66.67% | 571.7836 | $0.000000 |
| hr_ops | 12 | 50.00% | 713.7906 | $0.000000 |
| it_operations | 12 | 75.00% | 710.2641 | $0.000000 |
| logistics | 12 | 58.33% | 572.2836 | $0.000000 |
| procurement | 12 | 66.67% | 572.0080 | $0.000000 |
| research | 9 | 44.44% | 712.1898 | $0.000000 |
| sales_ops | 9 | 88.89% | 714.8891 | $0.000000 |
| software_delivery | 9 | 77.78% | 715.1384 | $0.000000 |
| workflow_routing | 9 | 66.67% | 727.0421 | $0.000000 |

## Score-specific metrics

- Exact accuracy: 31.67%
- Within ±1 accuracy: 71.67%
- MAE of expected score: 0.9170
- Quadratic weighted kappa: 0.5951

## Interpretation notes

Accuracy and calibration are reported separately from latency and cost. The project intentionally does not collapse them into a single winner score. Provider cost is the billed/request-reported amount when available; local models have zero provider cost. Estimated local compute cost is only populated when a machine-hour price was explicitly supplied for the run.
