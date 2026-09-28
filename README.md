# decision-model-evals

A vendor-neutral benchmark for **decision models**: models that make fast, bounded decisions instead of generating free-form text.

The benchmark evaluates three common primitives against one model-independent corpus:

- **Choice** — select one option from runtime-defined alternatives and retain the probability distribution.
- **Noul** — answer a binary semantic question with a probability of true/yes.
- **Score** — place an item on an ordered runtime-defined scale and retain per-level probabilities.

It keeps **quality, calibration, latency, throughput, deployment requirements, reliability, and cost separate**. There is deliberately no composite "winner score."

## v1 benchmark snapshot

The first complete benchmark run covers **5,760 cases across 16 domains**, balanced across Choice, Noul, and Score. All four active models completed the full suite with zero provider/transport errors.

| Model | Deployment | Overall accuracy | Choice | Noul | Score exact | Full-run p50 latency |
|---|---|---:|---:|---:|---:|---:|
| Jev 1.13 | hosted / OpenRouter | **74.50%** | **95.57%** | **86.88%** | **41.04%** | 307 ms |
| Decider 4B v2.1 | local | 69.81% | 87.29% | 84.74% | 37.40% | 297 ms |
| SemIf + Qwen3.5-4B | local | 66.42% | 85.36% | 75.68% | 38.23% | 711 ms |
| Bosun v3.1 0.6B | local | 54.93% | 66.51% | 64.90% | 33.39% | **79 ms** |

These are results on this corpus and this runtime setup, not universal model rankings. Local latency was measured on the same arm64 macOS host; Jev latency includes the hosted network/provider path. The exact Mac chip was not captured by the v1 hardware manifest, so these numbers should not be generalized as hardware benchmarks.

See [docs/BENCHMARK_RESULTS.md](docs/BENCHMARK_RESULTS.md) for calibration, Score metrics, concurrency scaling, provider cost, domains, paired comparisons, run IDs, and limitations.

## Models in the primary matrix

The v1 matrix intentionally spans different deployment points rather than only similarly sized models.

| Key | Model | Why it is included |
|---|---|---|
| `jev` | TypeSafe Jev 1.13 | Hosted reference model with native Choice/Noul/Score semantics and a pinned OpenRouter model ID. |
| `bosun` | Bosun v3.1 0.6B | Tiny local reference for low-latency, low-footprint deployment. |
| `decider` | Mapika Decider 4B v2.1 | Strong 4B local decision model with a native System One endpoint and practical Mac/Linux runtime paths. |
| `semif` | SemIf + pinned Qwen3.5-4B | Independent direct option-logit approach at the 4B scale, with Apple Silicon and Linux runtime paths. |

Two initially selected models were removed from the primary matrix:

- **JevK5 v0.2** — strong model, but the published serving path used in this project required CUDA and failed on Apple Silicon. The observed download was ~8.6 GB.
- **AutoJev-27B** — strong model, but ~50–52 GB in the tested setup and in a large-GPU deployment class, outside the intended normal MacBook / ordinary VPS target.

Their exclusion is about **deployment practicality, not model quality**. See [docs/EXCLUDED_MODELS.md](docs/EXCLUDED_MODELS.md).

## Quick start

Requirements: macOS or Linux, Python 3.11+, Git, and [`uv`](https://docs.astral.sh/uv/).

```bash
./scripts/setup
```

Then follow [docs/QUICKSTART.md](docs/QUICKSTART.md) for either hosted Jev or one of the local models. The cheapest validation flow is always:

```bash
./scripts/probe MODEL
./scripts/smoke MODEL
./scripts/run-benchmark MODEL quick
```

Only move to `full` and `perf` after those pass.

## Corpus and suites

The checked-in JSONL corpus contains **5,760 cases from 1,920 application-style states across 16 domains**. Every state contributes one case for each primitive, so the corpus contains 1,920 Choice, 1,920 Noul, and 1,920 Score cases.

The domains cover workflow routing, model/agent influencing security, customer support, IT operations, software delivery, data platforms, procurement, finance, logistics, ecommerce, research, content operations, sales operations, compliance, HR, and access governance.

Frozen suites keep setup checks cheap and final evaluation stable:

| Suite | Cases | Purpose |
|---|---:|---|
| `probe` | 3 | one request per primitive; setup validation |
| `smoke` | 18 | cheap cross-domain sanity check |
| `quick` | 300 | fast iteration / adapter validation |
| `core` | 1,500 | substantial development comparison |
| `full` | 5,760 | primary v1 quality result |
| `perf` | 180 | repeated latency/throughput workload |
| `routing` | 360 | workflow-routing slice |
| `agent-security` | 360 | agent-influencing/security slice |

See [docs/CORPUS.md](docs/CORPUS.md) and [docs/METHODOLOGY.md](docs/METHODOLOGY.md).

## What a run records

Each raw case retains the decision, available probability distribution, correctness, client-observed latency, retries/errors, resolved model/provider, provider timing where exposed, token usage where exposed, billed hosted cost where exposed, and the raw provider response.

Each run also records corpus/suite hashes, benchmark revision, concurrency, timeout/retry settings, and a hardware snapshot. `results.jsonl` is the source of truth; `summary.json` and `report.md` are derived artifacts.

Provider/API cost and local compute cost are kept separate. Local provider cost is `$0`, but local inference is not economically free. A modeled machine-hour cost is only included when explicitly supplied by the user.

## Reliability behavior

Probe, smoke, and normal benchmark commands return non-zero when provider/transport cases fail. Use `--allow-errors` only for deliberate diagnostic runs.

Local model servers run on fixed default ports:

- Bosun: `127.0.0.1:8000`
- Decider: `127.0.0.1:8011`
- SemIf: `127.0.0.1:8012`

If another service already owns a port, stop it or change the relevant supported endpoint before benchmarking. A port collision can otherwise make a healthy model appear broken.

## Scope and limitations

- The v1 corpus is synthetic and rule-authored. It is designed for controlled, application-style comparison, not as a random sample of all enterprise decisions.
- Gold labels are benchmark policy judgments, not observed business outcomes.
- v1 is English-only.
- The agent-security slice is an evaluation workload, not a safety certification.
- Latency and throughput are runtime/hardware/provider measurements; quality results are more portable than performance results.

See [docs/CORPUS.md](docs/CORPUS.md) and [docs/METHODOLOGY.md](docs/METHODOLOGY.md) for the full caveats.

## Documentation

- [Quick start](docs/QUICKSTART.md)
- [Benchmark results](docs/BENCHMARK_RESULTS.md)
- [Methodology](docs/METHODOLOGY.md)
- [Corpus design](docs/CORPUS.md)
- [Active models and runtime requirements](docs/MODELS.md)
- [Excluded models](docs/EXCLUDED_MODELS.md)
- [Licensing/admission policy](docs/LICENSING.md)
- [Results and publication guide](docs/RESULTS_GUIDE.md)

## Validation

```bash
./scripts/test-unit
./scripts/test-quality
```

The corpus is human-readable checked-in JSONL and is regenerated during the quality checks to detect drift.

## License

The repository code and authored v1 corpus are licensed under Apache-2.0. Model/runtime artifacts keep their upstream licenses or service terms; see [docs/LICENSING.md](docs/LICENSING.md).
