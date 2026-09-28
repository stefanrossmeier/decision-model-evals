# Results and publication guide

The current v1 public summary is in [BENCHMARK_RESULTS.md](BENCHMARK_RESULTS.md). This document describes what should accompany any future published result.

Do not publish only one accuracy number. For each model, retain the complete run directory and report at minimum:

- suite and exact case count;
- model/version and transport;
- benchmark revision plus corpus/suite hashes;
- overall and per-primitive accuracy;
- Brier, NLL, and ECE;
- probability coverage when a provider does not expose a complete distribution for every case;
- Score within-1 accuracy, MAE, and quadratic weighted kappa;
- p50/p95 latency and concurrency;
- total provider cost and mean cost/request where applicable;
- local hardware/backend and any explicit machine-hour price;
- error/retry rate;
- per-domain accuracy.

For Jev, publish the provider-resolved model snapshot returned by OpenRouter in addition to the requested `typesafe/jev-1.13` ID.

For local models, publish the actual hardware and backend. A result from an Apple MPS path, a CPU VPS, and a CUDA GPU can all be valid measurements, but their latency/throughput values are not directly interchangeable.

The repository ignores `results/*/` by default. For a public release, attach the exact raw run directories used for headline tables as immutable release assets or publish them in another stable artifact store. Each run should include:

```text
manifest.json
results.jsonl
summary.json
report.md
```

`results.jsonl` is the source of truth. Reports and comparisons can then be regenerated without repeating paid hosted inference.

For the GPT-6 Luna post-v1 experiments, preserve OpenRouter's resolved model/provider identity and request-reported cost in the raw rows. The frozen protocol is in [LUNA_EXPERIMENTS.md](LUNA_EXPERIMENTS.md); the canonical run IDs and published comparison are in [LUNA_VS_JEV.md](LUNA_VS_JEV.md).

When comparing models, keep quality, calibration, latency, throughput, deployment requirements, and cost as separate axes. Do not collapse them into an arbitrary composite score.
