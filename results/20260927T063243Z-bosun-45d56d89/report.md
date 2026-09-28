# Benchmark report: bosun

- Run: `20260927T063243Z-bosun-45d56d89`
- Suite: `perf`
- Cases: 180 (180 valid, 0 errors)
- Accuracy: 51.11%
- Provider cost: $0.000000
- Provider cost / 1M decisions at this case mix: $0.000000
- Estimated local compute cost: $0.000000
- p50 / p95 latency: 1220.6168 / 1379.7729 ms
- Suite throughput: 13.1170 requests/s

## Primitive results

| Primitive | n | Accuracy | Macro F1 | Brier | NLL | ECE-10 | p50 ms | p95 ms | Provider cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| choice | 60 | 58.33% | 0.4385 | 0.5452 | 1.0958 | 0.1830 | 1224.3944 | 1380.4291 | $0.000000 |
| noul | 60 | 61.67% | 0.6078 | 0.2435 | 0.7235 | 0.1722 | 1204.9764 | 1379.3396 | $0.000000 |
| score | 60 | 33.33% | — | 0.8211 | 1.6712 | 0.2512 | 1222.0090 | 1406.9831 | $0.000000 |

## Domains

| Domain | n | Accuracy | p50 ms | Provider cost |
|---|---:|---:|---:|---:|
| access_governance | 12 | 75.00% | 1218.5328 | $0.000000 |
| agent_security | 12 | 50.00% | 1225.2858 | $0.000000 |
| compliance | 12 | 25.00% | 1208.1674 | $0.000000 |
| content_ops | 12 | 50.00% | 1208.1896 | $0.000000 |
| customer_support | 12 | 83.33% | 1202.6515 | $0.000000 |
| data_platform | 12 | 83.33% | 1227.1696 | $0.000000 |
| ecommerce | 12 | 25.00% | 1222.7156 | $0.000000 |
| finance_ops | 12 | 41.67% | 1230.8349 | $0.000000 |
| hr_ops | 12 | 75.00% | 1242.2894 | $0.000000 |
| it_operations | 12 | 50.00% | 1227.9141 | $0.000000 |
| logistics | 12 | 41.67% | 1200.8875 | $0.000000 |
| procurement | 12 | 41.67% | 1196.5176 | $0.000000 |
| research | 9 | 22.22% | 1204.7579 | $0.000000 |
| sales_ops | 9 | 77.78% | 1207.7710 | $0.000000 |
| software_delivery | 9 | 44.44% | 1226.2827 | $0.000000 |
| workflow_routing | 9 | 22.22% | 1221.9615 | $0.000000 |

## Score-specific metrics

- Exact accuracy: 33.33%
- Within ±1 accuracy: 66.67%
- MAE of expected score: 1.0087
- Quadratic weighted kappa: 0.3856

## Interpretation notes

Accuracy and calibration are reported separately from latency and cost. The project intentionally does not collapse them into a single winner score. Provider cost is the billed/request-reported amount when available; local models have zero provider cost. Estimated local compute cost is only populated when a machine-hour price was explicitly supplied for the run.
