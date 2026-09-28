# Benchmark report: luna-structured

- Run: `20260928T083430Z-luna-structured-04dce78a`
- Suite: `perf`
- Cases: 180 (180 valid, 0 errors)
- Accuracy: 73.89%
- Provider cost: $0.004937
- Provider cost basis: `provider_reported`
- Provider cost / 1M decisions at this case mix: $27.426111
- Estimated local compute cost: $0.000000
- p50 / p95 latency: 910.7890 / 1457.0580 ms
- Suite throughput: 3.6014 requests/s
- Input / output tokens: 37,002 / 2,473
- Cached input / cache-write / reasoning tokens: 0 / 0 / 0

## Primitive results

| Primitive | n | Accuracy | Macro F1 | Prob. coverage | Brier | NLL | ECE-10 | p50 ms | p95 ms | Provider cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| choice | 60 | 91.67% | 0.8620 | 0.00% | — | — | — | 927.0124 | 1484.0916 | $0.001856 |
| noul | 60 | 86.67% | 0.8629 | 0.00% | — | — | — | 873.9511 | 1145.0271 | $0.001512 |
| score | 60 | 43.33% | — | 0.00% | — | — | — | 910.7765 | 1439.5876 | $0.001568 |

## Domains

| Domain | n | Accuracy | p50 ms | Provider cost |
|---|---:|---:|---:|---:|
| access_governance | 12 | 91.67% | 875.7425 | $0.000331 |
| agent_security | 12 | 91.67% | 985.9194 | $0.000384 |
| compliance | 12 | 75.00% | 884.9605 | $0.000324 |
| content_ops | 12 | 83.33% | 892.9909 | $0.000317 |
| customer_support | 12 | 91.67% | 905.7141 | $0.000333 |
| data_platform | 12 | 91.67% | 952.1394 | $0.000332 |
| ecommerce | 12 | 41.67% | 967.1200 | $0.000326 |
| finance_ops | 12 | 75.00% | 922.4609 | $0.000324 |
| hr_ops | 12 | 50.00% | 899.9363 | $0.000327 |
| it_operations | 12 | 66.67% | 964.8125 | $0.000320 |
| logistics | 12 | 41.67% | 960.6277 | $0.000318 |
| procurement | 12 | 75.00% | 842.5092 | $0.000316 |
| research | 9 | 66.67% | 894.5857 | $0.000243 |
| sales_ops | 9 | 100.00% | 916.2327 | $0.000249 |
| software_delivery | 9 | 66.67% | 907.3247 | $0.000244 |
| workflow_routing | 9 | 77.78% | 883.8475 | $0.000249 |

## Score-specific metrics

- Exact accuracy: 43.33%
- Within ±1 accuracy: 83.33%
- MAE of selected score: 0.7333
- MAE of expected score: —
- Quadratic weighted kappa: 0.7146

## Interpretation notes

Accuracy and calibration are reported separately from latency and cost. The project intentionally does not collapse them into a single winner score. Probability coverage states how many cases exposed a complete usable probability distribution; calibration metrics are computed only on those cases. Provider cost is provider-reported when available or computed from recorded token usage and the pricing snapshot stored in the model configuration. Local models have zero provider cost. Estimated local compute cost is only populated when a machine-hour price was explicitly supplied for the run.
