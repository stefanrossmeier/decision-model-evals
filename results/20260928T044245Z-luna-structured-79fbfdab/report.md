# Benchmark report: luna-structured

- Run: `20260928T044245Z-luna-structured-79fbfdab`
- Suite: `full`
- Cases: 5760 (5760 valid, 0 errors)
- Accuracy: 73.12%
- Provider cost: $0.157664
- Provider cost basis: `provider_reported`
- Provider cost / 1M decisions at this case mix: $27.372222
- Estimated local compute cost: $0.000000
- p50 / p95 latency: 922.1121 / 1331.0572 ms
- Suite throughput: 1.0005 requests/s
- Input / output tokens: 1,183,260 / 78,676
- Cached input / cache-write / reasoning tokens: 0 / 0 / 0

## Primitive results

| Primitive | n | Accuracy | Macro F1 | Prob. coverage | Brier | NLL | ECE-10 | p50 ms | p95 ms | Provider cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| choice | 1920 | 94.74% | 0.9503 | 0.00% | — | — | — | 923.2358 | 1332.2784 | $0.059150 |
| noul | 1920 | 85.26% | 0.8520 | 0.00% | — | — | — | 921.6324 | 1327.8936 | $0.048291 |
| score | 1920 | 39.38% | — | 0.00% | — | — | — | 922.0371 | 1331.7626 | $0.050223 |

## Domains

| Domain | n | Accuracy | p50 ms | Provider cost |
|---|---:|---:|---:|---:|
| access_governance | 360 | 70.28% | 952.8109 | $0.010001 |
| agent_security | 360 | 81.67% | 922.5076 | $0.011405 |
| compliance | 360 | 70.28% | 922.3633 | $0.009649 |
| content_ops | 360 | 72.50% | 922.8600 | $0.009466 |
| customer_support | 360 | 80.00% | 962.8587 | $0.009932 |
| data_platform | 360 | 75.83% | 960.1959 | $0.009857 |
| ecommerce | 360 | 60.83% | 921.7477 | $0.009799 |
| finance_ops | 360 | 77.50% | 918.5291 | $0.009709 |
| hr_ops | 360 | 64.72% | 921.8337 | $0.009779 |
| it_operations | 360 | 68.06% | 921.3915 | $0.009673 |
| logistics | 360 | 63.61% | 921.2418 | $0.009556 |
| procurement | 360 | 82.78% | 921.3761 | $0.009470 |
| research | 360 | 67.50% | 920.4055 | $0.009849 |
| sales_ops | 360 | 78.61% | 919.5820 | $0.009867 |
| software_delivery | 360 | 79.72% | 969.7168 | $0.009710 |
| workflow_routing | 360 | 76.11% | 960.4497 | $0.009941 |

## Score-specific metrics

- Exact accuracy: 39.38%
- Within ±1 accuracy: 86.51%
- MAE of selected score: 0.7521
- MAE of expected score: —
- Quadratic weighted kappa: 0.7068

## Interpretation notes

Accuracy and calibration are reported separately from latency and cost. The project intentionally does not collapse them into a single winner score. Probability coverage states how many cases exposed a complete usable probability distribution; calibration metrics are computed only on those cases. Provider cost is provider-reported when available or computed from recorded token usage and the pricing snapshot stored in the model configuration. Local models have zero provider cost. Estimated local compute cost is only populated when a machine-hour price was explicitly supplied for the run.
