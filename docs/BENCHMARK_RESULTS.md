# Benchmark results — v1

This document summarizes the first complete four-model run of the v1 corpus. The headline quality results come from the frozen **5,760-case `full` suite**. Performance results come from the frozen **180-case `perf` suite** at concurrency 1, 4, and 16.

The four full runs used the same benchmark revision, corpus hash, and suite hash:

- benchmark revision: `67f5c2cf35a9b610afc15ea8ace6a598003c8632`
- corpus SHA-256: `9e9a98f43406e99643c7eaf5dee7aa56d5d62c7b9163f9c1df878f178e3e3ef2`
- full-suite SHA-256: `f5e0646d4050ac95a08607d0893c581bacc4f5e58274eaf532aca4bd101e4a0e`
- run date: 2026-09-27
- client host recorded by the manifests: `arm64`, `macOS-15.7.4-arm64-arm-64bit`, Python 3.11.16

The exact Mac chip/memory were not captured by the v1 manifest. Local latency numbers therefore describe this specific host/runtime setup and should not be generalized as portable hardware benchmarks. Jev is hosted, so its latency additionally includes network/OpenRouter/provider effects.

## Overall results

All four models completed all 5,760 full-suite cases with **zero provider/transport errors**.

| Model | Deployment | Overall | Choice | Noul | Score exact | Score ±1 | Score MAE | Score κ | p50 | p95 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Jev 1.13 | hosted | **74.50%** | **95.57%** | **86.88%** | **41.04%** | **87.71%** | **0.715** | **0.710** | 307 ms | 410 ms |
| Decider 4B v2.1 | local | 69.81% | 87.29% | 84.74% | 37.40% | 82.81% | 0.847 | 0.620 | **297 ms** | 938 ms |
| SemIf + Qwen3.5-4B | local | 66.42% | 85.36% | 75.68% | 38.23% | 76.51% | 0.860 | 0.580 | 711 ms | 745 ms |
| Bosun v3.1 0.6B | local | 54.93% | 66.51% | 64.90% | 33.39% | 65.47% | 1.000 | 0.347 | **79 ms** | **93 ms** |

`Score κ` is quadratic weighted kappa. `Score MAE` uses the probability-weighted expected score.

### What stands out

- **Jev produced the strongest full-corpus quality result** and led all three primitives on exact accuracy. Its advantage was especially large on Choice.
- **Decider was the strongest local quality result**, 4.89 percentage points behind Jev overall and 3.39 points ahead of SemIf.
- **SemIf landed between Decider and Bosun on overall quality**. Its Score exact accuracy (38.23%) was slightly above Decider's (37.40%), while Decider was better on within-1 accuracy, MAE, and weighted kappa.
- **Bosun was the fastest local model by a large margin** at single-request concurrency, but its quality was lower on this corpus.
- Score remained the hardest primitive for every model. The gap between exact Score accuracy and within-1 accuracy shows that many misses were adjacent-level rather than gross ordinal errors.

These are corpus-specific findings, not a universal ordering of the models.

## Probability quality and calibration

Accuracy is not enough for decision models because applications often route on probabilities.

| Model | Choice ECE | Noul ECE | Score ECE | Score Brier | Score NLL |
|---|---:|---:|---:|---:|---:|
| Jev | **0.025** | **0.044** | 0.311 | 0.848 | 2.929 |
| Decider | 0.026 | 0.051 | **0.107** | **0.743** | **1.452** |
| SemIf | 0.050 | 0.098 | 0.215 | 0.783 | 1.611 |
| Bosun | 0.106 | 0.140 | 0.247 | 0.841 | 1.678 |

A useful nuance is visible here: **Jev had the strongest Score decision quality but not the strongest Score probability metrics**. Decider produced substantially better Score ECE/Brier/NLL on this corpus. Consumers that threshold or combine Score probabilities should therefore evaluate calibration separately from top-level accuracy.

The corpus mean gold Score was **2.437**. Mean probability-weighted predicted Scores were:

| Model | Mean predicted Score | Bias vs. gold mean |
|---|---:|---:|
| Bosun | 2.761 | +0.324 |
| Jev | 2.224 | -0.213 |
| SemIf | 2.107 | -0.329 |
| Decider | 2.084 | -0.353 |

Bosun therefore showed an upward Score tendency, while the other three tended downward in this corpus.

## Paired full-suite comparisons

Because every full run used the same 5,760 case IDs, correctness can be compared case by case. The counts below show cases where only one model in the pair was correct. Exact two-sided McNemar p-values are included as evidence that the observed differences are not just aggregate sampling noise within this frozen corpus.

| Pair | First-only correct | Second-only correct | McNemar p |
|---|---:|---:|---:|
| Jev vs. Decider | 591 | 321 | 2.88e-19 |
| Jev vs. SemIf | 827 | 362 | 2.44e-42 |
| Jev vs. Bosun | 1,528 | 401 | 2.00e-154 |
| Decider vs. SemIf | 590 | 395 | 5.61e-10 |
| Decider vs. Bosun | 1,399 | 542 | 5.62e-87 |
| SemIf vs. Bosun | 1,217 | 555 | 7.01e-57 |

These tests establish differences on this exact corpus. They do not make the corpus a representative sample of every production workload.

## Performance scaling

The perf suite contains 180 fixed cases. Quality percentages in this table are included only as a repeatability signal; the 5,760-case full suite remains the primary quality result.

| Model | Concurrency | Throughput | p50 | p95 | Perf accuracy |
|---|---:|---:|---:|---:|---:|
| Bosun | 1 | 12.11 req/s | 79 ms | 92 ms | 51.1% |
| Bosun | 4 | 12.91 req/s | 306 ms | 333 ms | 51.1% |
| Bosun | 16 | 13.12 req/s | 1,221 ms | 1,380 ms | 51.1% |
| Decider | 1 | 2.05 req/s | 296 ms | 939 ms | 70.0% |
| Decider | 4 | 1.86 req/s | 2,257 ms | 3,574 ms | 70.0% |
| Decider | 16 | 2.09 req/s | 7,584 ms | 11,000 ms | 70.0% |
| SemIf | 1 | 1.52 req/s | 712 ms | 744 ms | 66.1% |
| SemIf | 4 | 1.52 req/s | 2,686 ms | 2,897 ms | 66.1% |
| SemIf | 16 | 1.52 req/s | 10,414 ms | 11,163 ms | 66.1% |
| Jev | 1 | 3.06 req/s | 307 ms | 411 ms | 72.2% |
| Jev | 4 | 12.75 req/s | 291 ms | 436 ms | 72.8% |
| Jev | 16 | **44.33 req/s** | 286 ms | 853 ms | 71.7% |

### Local concurrency behavior

The three local server paths largely serialized inference:

- Bosun gained only modest throughput from concurrency while queueing latency grew sharply.
- Decider throughput stayed around ~2 req/s while p50 rose from 296 ms to 7.6 s at concurrency 16.
- SemIf throughput stayed essentially flat at ~1.52 req/s while p50 rose from 712 ms to 10.4 s.

For these specific local serving paths, increasing client concurrency mostly created a queue rather than increasing useful throughput.

### Hosted Jev concurrency behavior

Jev scaled differently: throughput rose from 3.06 req/s at concurrency 1 to 44.33 req/s at concurrency 16. Median latency remained near ~300 ms, although the p95 tail rose to 853 ms at concurrency 16.

The hosted perf runs were not bit-for-bit deterministic: the repeated 180-case runs showed small probability/prediction variation and perf accuracy ranged from 71.7% to 72.8%. Do not use the perf subset as a replacement for the full quality result.

## Cost

The Jev full run reported exact provider billing through OpenRouter:

- input tokens: **2,358,348**
- total provider cost: **$0.099050616**
- observed provider cost per 1,000 decisions: **$0.01720**
- observed provider cost per 1,000,000 decisions: **$17.20**

Those projections reflect this benchmark's input-size mix and the billing returned during the run; they are not a permanent price quote.

The three local runs have provider/API cost `$0`. No `LOCAL_COMPUTE_USD_PER_HOUR` value was supplied, so the benchmark did **not** estimate electricity, hardware depreciation, cloud VM/GPU rental, or operator cost. It would be incorrect to describe the local runs as economically free.

## Domain accuracy

Each domain contributes 360 cases in the full suite.

| Domain | Bosun | Decider | SemIf | Jev |
|---|---:|---:|---:|---:|
| Access governance | 56.7% | 55.6% | 64.2% | 71.4% |
| Agent security | 60.0% | 60.3% | 60.3% | **84.7%** |
| Compliance | 52.8% | 59.7% | 52.5% | **70.6%** |
| Content ops | 62.8% | **77.2%** | 72.2% | **77.2%** |
| Customer support | 75.3% | **81.9%** | 79.4% | 80.6% |
| Data platform | 65.0% | 70.0% | 69.7% | **73.3%** |
| Ecommerce | 25.0% | 65.6% | 66.1% | **71.1%** |
| Finance ops | 61.9% | 75.3% | 70.8% | **82.8%** |
| HR ops | 62.5% | 63.3% | 63.3% | **70.6%** |
| IT operations | 57.2% | 71.4% | **72.2%** | 70.3% |
| Logistics | 45.3% | **72.5%** | 63.1% | 70.6% |
| Procurement | 56.1% | 71.7% | 70.0% | **75.0%** |
| Research | 41.4% | 60.8% | 51.7% | **66.9%** |
| Sales ops | 54.7% | 78.1% | 60.3% | **81.9%** |
| Software delivery | 62.5% | 79.2% | **81.1%** | 80.8% |
| Workflow routing | 39.7% | **74.4%** | 65.8% | 64.2% |

No model led every domain. This is one reason the project publishes per-domain results rather than a composite score.

## Individual runs

### Jev 1.13

- requested model: `typesafe/jev-1.13`
- provider-resolved model: `typesafe/jev-1.13-20260917`
- deployment: hosted through OpenRouter Decisions API
- full run: `20260927T101408Z-jev-0c89145b`
- overall accuracy: **74.50%** (95% Wilson CI 73.35–75.61%)
- full-run duration: **1,814.94 s** (~30.2 min)
- full-run throughput: **3.17 req/s**
- provider errors: **0 / 5,760**
- billed full-run provider cost: **$0.09905**

Jev was strongest overall and on each primitive by exact accuracy. Its Score MAE and weighted kappa were also strongest, but its Score probability calibration metrics were weaker than Decider's.

### Decider 4B v2.1

- configured model: `Mapika/decider-4b`
- resolved model: `decider-4b-v2.1`
- deployment: local native `/v1/systemone`
- full run: `20260927T071225Z-decider-0b81b9b4`
- overall accuracy: **69.81%** (95% Wilson CI 68.61–70.98%)
- full-run duration: **2,797.64 s** (~46.6 min)
- full-run throughput: **2.06 req/s**
- provider errors: **0 / 5,760**

Decider was the strongest local model overall. Choice and Noul were particularly strong, and it had the best Score calibration metrics in the four-model set. Score requests were much slower than its Choice/Noul requests, producing the large full-run latency tail.

### SemIf + Qwen3.5-4B

- model: `Qwen/Qwen3.5-4B`
- resolved runtime identity: `SemIf:Qwen/Qwen3.5-4B@851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`
- deployment: local thin `/v1/systemone` transport around direct option-logit scoring
- full run: `20260927T084306Z-semif-ca2dfa66`
- overall accuracy: **66.42%** (95% Wilson CI 65.19–67.63%)
- full-run duration: **3,787.19 s** (~63.1 min)
- full-run throughput: **1.52 req/s**
- provider errors: **0 / 5,760**

This evaluation used the PyTorch/MPS path on Apple Silicon. Upstream SemIf documentation notes that Qwen3.5 hybrid-attention operations can fall back to slower reference kernels on MPS; these latency numbers therefore should not be treated as representative of CUDA or SemIf's MLX backend.

### Bosun v3.1 0.6B

- resolved model: `Hanno-Labs/bosun-v3.1-0.6b`
- deployment: local Jev-compatible server
- full run: `20260927T062423Z-bosun-84b85fed`
- overall accuracy: **54.93%** (95% Wilson CI 53.64–56.21%)
- full-run duration: **471.15 s** (~7.9 min)
- full-run throughput: **12.23 req/s**
- provider errors: **0 / 5,760**

Bosun was the smallest and fastest local reference. It was materially weaker on overall quality but remains useful when low per-request latency and a small local deployment footprint matter.

## Reproducibility and publication notes

The repository intentionally ignores `results/*/` by default. For a public benchmark release, publish the exact raw run directories used for these tables as release assets or another immutable artifact store. At minimum retain each run's `manifest.json`, `results.jsonl`, `summary.json`, and `report.md`.

The v1 hardware manifest records architecture/OS but not the exact Apple chip or memory size. Future performance publications should capture those fields before making cross-machine claims.

See [METHODOLOGY.md](METHODOLOGY.md) for metric definitions and [RESULTS_GUIDE.md](RESULTS_GUIDE.md) for publication requirements.
