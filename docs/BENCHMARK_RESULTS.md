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

## Expanded frozen-corpus comparison

The original v1 four-model table above remains historical. Later experiments reused the **same frozen 5,760-case corpus and full-suite hashes**, so the completed runs can also be viewed together without changing the underlying cases or labels. Julia 1 and the two GPT-6 Luna modes were added after the original v1 benchmark.

| Model | Deployment | Overall | Choice | Noul | Score exact | Full-run p50 | Probability coverage |
|---|---|---:|---:|---:|---:|---:|---:|
| Jev 1.13 | hosted | 74.50% | 95.57% | 86.88% | 41.04% | 307 ms | 100% |
| GPT-6 Luna — classifier | hosted | 73.14% | 95.31% | 85.26% | 38.85% | 938 ms | 0% |
| GPT-6 Luna — structured | hosted | 73.12% | 94.74% | 85.26% | 39.38% | 922 ms | 0% |
| Decider 4B v2.1 | local | 69.81% | 87.29% | 84.74% | 37.40% | 297 ms | 100% |
| SemIf + Qwen3.5-4B | local | 66.42% | 85.36% | 75.68% | 38.23% | 711 ms | 100% |
| Bosun v3.1 0.6B | local | 54.93% | 66.51% | 64.90% | 33.39% | 79 ms | 100% |
| Julia 1 144.3M | local CPU | 42.20% | 44.95% | 58.54% | 23.12% | **27 ms** | 100% |

Julia is the fastest measured local entrant by a wide margin on this host, but its quality is also the lowest of the completed full-suite runs. It finished **32.29 percentage points behind Jev overall**, **27.60 points behind Decider**, **24.22 points behind SemIf**, and **12.73 points behind Bosun**. The two Luna rows do not expose model probability distributions through the evaluated OpenRouter path, so their `0%` probability coverage is an interface limitation rather than a statement about hidden model confidence.

Latency comparisons require caution: all local runs were recorded on an arm64 macOS host, but the exact Apple chip and memory were not captured; Jev and Luna include network/provider latency. Julia used its CPU FP32 runtime, while Decider/SemIf used their documented Apple-local paths.

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

### Post-v1 Julia 1 performance

Julia 1 used the same frozen 180-case perf suite on the recorded arm64 macOS host, running CPU FP32 inference. All three runs returned identical quality (42.22%) and zero errors.

| Concurrency | Throughput | p50 | p95 | Perf accuracy |
|---:|---:|---:|---:|---:|
| 1 | 36.19 req/s | 27 ms | 31 ms | 42.22% |
| 4 | **37.22 req/s** | 106 ms | 115 ms | 42.22% |
| 16 | 36.52 req/s | 427 ms | 466 ms | 42.22% |

The nearly flat ~36–37 req/s throughput together with roughly linear latency growth indicates that this simple local serving path mostly serialized CPU inference under concurrent load. Even so, its single-request path was about **2.9× faster than Bosun's measured p50** on the same recorded host class (27 ms vs. 79 ms), and the 5,760-case Julia full run completed in **156.4 seconds** (~2.6 minutes).

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

Bosun was the smallest and fastest local reference in the original v1 matrix. It was materially weaker on overall quality but remains useful when low per-request latency and a small local deployment footprint matter. Julia 1 later established an even smaller/faster post-v1 CPU point, with substantially lower quality on this corpus.

### Julia 1 144.3M (post-v1)

- model: `SupersonicLabs/Julia-1`
- pinned Julia revision: `a85b127321d580d65176c89ced8273f305745d85`
- weight SHA-256: `df853bf7fe424420011f3d0c47a05d7341aa9eefa7fb9f203ea4aada4ad95b72`
- base encoder: `jhu-clsp/mmBERT-small` / multilingual ModernBERT family
- deployment: local CPU through a thin `/v1/systemone` adapter around Julia's native named-question API
- full run: `20260929T172106Z-julia1-cdeac5d1`
- benchmark revision: `42bb8c152faf52a9011f153d627927f1abed4de5`
- overall accuracy: **42.20%** (95% Wilson CI 40.94–43.49%)
- full-run duration: **156.41 s** (~2.6 min)
- full-run throughput: **36.83 req/s**
- p50 / p95: **27.0 / 31.2 ms**
- provider/transport errors: **0 / 5,760**

Primitive quality was **44.95% Choice**, **58.54% Noul**, and **23.12% Score exact**. Score within-1 accuracy was 54.32%, expected-score MAE 1.357, selected-score MAE 1.481, and quadratic weighted kappa 0.078. Julia exposed complete probability distributions for every case, but calibration was weak on this corpus: Choice/Noul/Score ECE were 0.414/0.318/0.527 respectively.

Paired correctness confirms that this is not a small aggregate gap. Against Jev, there were **2,246 cases correct only for Jev versus 386 correct only for Julia**. Against Bosun, there were **1,506 Bosun-only versus 773 Julia-only** cases. Julia's strongest domains were HR operations (57.22%), finance operations (51.39%), and customer support (51.11%); its weakest were workflow routing (28.89%), ecommerce (31.67%), and research (33.61%).

The result is notably different from Julia's own [published typed-decision benchmark](https://huggingface.co/SupersonicLabs/Julia-1). The upstream project reports a September 26 CPU FP32 reproduction of 426/600 Choice, 483/600 Noul, and 542/800 Score on its pinned typed dataset. That is a **different dataset and task distribution**, so the numbers are not contradictory; the gap is evidence that Julia's published typed benchmark did not transfer to this frozen enterprise-style corpus. The benchmark adapter preserves the native question descriptions and uses the same strict-encoding/runtime settings rather than replacing Julia's decision logic.

## Reproducibility and publication notes

The repository intentionally ignores `results/*/` by default. For a public benchmark release, publish the exact raw run directories used for these tables as release assets or another immutable artifact store. At minimum retain each run's `manifest.json`, `results.jsonl`, `summary.json`, and `report.md`.

The v1 hardware manifest records architecture/OS but not the exact Apple chip or memory size. Future performance publications should capture those fields before making cross-machine claims.

Canonical Julia artifacts included with this result set:

- probe: `20260929T172051Z-julia1-cccb0a52`
- smoke: `20260929T172052Z-julia1-e65c7946`
- quick: `20260929T172052Z-julia1-fcfe2f76`
- full: `20260929T172106Z-julia1-cdeac5d1`
- perf c=1: `20260929T180041Z-julia1-552c857d`
- perf c=4: `20260929T180046Z-julia1-03ca558c`
- perf c=16: `20260929T180051Z-julia1-bb4b47f8`

See [METHODOLOGY.md](METHODOLOGY.md) for metric definitions and [RESULTS_GUIDE.md](RESULTS_GUIDE.md) for publication requirements.

## Post-v1 GPT-6 Luna comparison

The original four-model v1 table above remains frozen. Two later GPT-6 Luna experiments reused the same 5,760-case corpus without changing any cases or gold labels. The direct Structured Outputs mode scored **73.12%** overall and the explicit `A/B/C/...` classifier mode **73.14%**, compared with Jev's existing **74.50%** result. Their full quality, prompt design, paired statistics, provider cost, and dedicated latency/throughput measurements are reported separately in [LUNA_VS_JEV.md](LUNA_VS_JEV.md).
