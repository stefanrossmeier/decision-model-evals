# Benchmark report: jev

- Run: `20260927T101408Z-jev-0c89145b`
- Suite: `full`
- Cases: 5760 (5760 valid, 0 errors)
- Accuracy: 74.50%
- Provider cost: $0.099051
- Provider cost / 1M decisions at this case mix: $17.196288
- Estimated local compute cost: $0.000000
- p50 / p95 latency: 307.1232 / 410.1540 ms
- Suite throughput: 3.1737 requests/s

## Primitive results

| Primitive | n | Accuracy | Macro F1 | Brier | NLL | ECE-10 | p50 ms | p95 ms | Provider cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| choice | 1920 | 95.57% | 0.9583 | 0.0765 | 0.1440 | 0.0254 | 307.1625 | 410.2383 | $0.037262 |
| noul | 1920 | 86.88% | 0.8687 | 0.0929 | 0.3055 | 0.0441 | 307.0373 | 410.0677 | $0.030166 |
| score | 1920 | 41.04% | — | 0.8480 | 2.9291 | 0.3112 | 307.1469 | 410.0246 | $0.031622 |

## Domains

| Domain | n | Accuracy | p50 ms | Provider cost |
|---|---:|---:|---:|---:|
| access_governance | 360 | 71.39% | 307.4003 | $0.006227 |
| agent_security | 360 | 84.72% | 307.0368 | $0.006814 |
| compliance | 360 | 70.56% | 307.0942 | $0.006080 |
| content_ops | 360 | 77.22% | 306.9330 | $0.006044 |
| customer_support | 360 | 80.56% | 307.2933 | $0.006272 |
| data_platform | 360 | 73.33% | 307.2098 | $0.006220 |
| ecommerce | 360 | 71.11% | 307.2156 | $0.006178 |
| finance_ops | 360 | 82.78% | 307.1117 | $0.006104 |
| hr_ops | 360 | 70.56% | 307.2008 | $0.006137 |
| it_operations | 360 | 70.28% | 307.2286 | $0.006153 |
| logistics | 360 | 70.56% | 307.0627 | $0.006086 |
| procurement | 360 | 75.00% | 307.1332 | $0.006041 |
| research | 360 | 66.94% | 307.3700 | $0.006142 |
| sales_ops | 360 | 81.94% | 306.9864 | $0.006162 |
| software_delivery | 360 | 80.83% | 306.9244 | $0.006144 |
| workflow_routing | 360 | 64.17% | 306.8335 | $0.006246 |

## Score-specific metrics

- Exact accuracy: 41.04%
- Within ±1 accuracy: 87.71%
- MAE of expected score: 0.7149
- Quadratic weighted kappa: 0.7095

## Interpretation notes

Accuracy and calibration are reported separately from latency and cost. The project intentionally does not collapse them into a single winner score. Provider cost is the billed/request-reported amount when available; local models have zero provider cost. Estimated local compute cost is only populated when a machine-hour price was explicitly supplied for the run.
