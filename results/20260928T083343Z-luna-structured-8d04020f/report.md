# Benchmark report: luna-structured

- Run: `20260928T083343Z-luna-structured-8d04020f`
- Suite: `perf`
- Cases: 180 (180 valid, 0 errors)
- Accuracy: 75.00%
- Provider cost: $0.004937
- Provider cost basis: `provider_reported`
- Provider cost / 1M decisions at this case mix: $27.426111
- Estimated local compute cost: $0.000000
- p50 / p95 latency: 952.6623 / 1472.4117 ms
- Suite throughput: 3.8910 requests/s
- Input / output tokens: 37,002 / 2,473
- Cached input / cache-write / reasoning tokens: 0 / 0 / 0

## Primitive results

| Primitive | n | Accuracy | Macro F1 | Prob. coverage | Brier | NLL | ECE-10 | p50 ms | p95 ms | Provider cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| choice | 60 | 93.33% | 0.8876 | 0.00% | — | — | — | 973.1362 | 1442.1760 | $0.001856 |
| noul | 60 | 88.33% | 0.8806 | 0.00% | — | — | — | 956.2234 | 1721.3040 | $0.001509 |
| score | 60 | 43.33% | — | 0.00% | — | — | — | 920.0163 | 1268.8322 | $0.001571 |

## Domains

| Domain | n | Accuracy | p50 ms | Provider cost |
|---|---:|---:|---:|---:|
| access_governance | 12 | 91.67% | 919.6843 | $0.000334 |
| agent_security | 12 | 75.00% | 985.8758 | $0.000381 |
| compliance | 12 | 83.33% | 943.3783 | $0.000324 |
| content_ops | 12 | 91.67% | 889.1692 | $0.000317 |
| customer_support | 12 | 91.67% | 1022.0229 | $0.000333 |
| data_platform | 12 | 83.33% | 969.5453 | $0.000332 |
| ecommerce | 12 | 50.00% | 879.6797 | $0.000326 |
| finance_ops | 12 | 83.33% | 930.7104 | $0.000324 |
| hr_ops | 12 | 50.00% | 943.6623 | $0.000327 |
| it_operations | 12 | 58.33% | 1006.6658 | $0.000320 |
| logistics | 12 | 41.67% | 925.3460 | $0.000318 |
| procurement | 12 | 83.33% | 891.8245 | $0.000316 |
| research | 9 | 66.67% | 968.4949 | $0.000243 |
| sales_ops | 9 | 100.00% | 975.2222 | $0.000249 |
| software_delivery | 9 | 77.78% | 932.1299 | $0.000244 |
| workflow_routing | 9 | 77.78% | 1036.3422 | $0.000249 |

## Score-specific metrics

- Exact accuracy: 43.33%
- Within ±1 accuracy: 85.00%
- MAE of selected score: 0.7167
- MAE of expected score: —
- Quadratic weighted kappa: 0.7158

## Interpretation notes

Accuracy and calibration are reported separately from latency and cost. The project intentionally does not collapse them into a single winner score. Probability coverage states how many cases exposed a complete usable probability distribution; calibration metrics are computed only on those cases. Provider cost is provider-reported when available or computed from recorded token usage and the pricing snapshot stored in the model configuration. Local models have zero provider cost. Estimated local compute cost is only populated when a machine-hour price was explicitly supplied for the run.
