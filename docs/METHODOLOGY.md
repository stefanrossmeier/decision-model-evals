# Methodology

The published v1 benchmark results are summarized in [BENCHMARK_RESULTS.md](BENCHMARK_RESULTS.md).

## Goal

Measure typed decision models under application-like workloads while keeping four axes separate: decision quality, calibration, latency/throughput, and economics.

## Unit of evaluation

A case contains:

- `state`: the application state the model sees;
- exactly one typed question (`choice`, `noul`, or `score`);
- explicit criteria/rubric;
- a frozen gold label and human-readable rationale;
- domain/task/tags used only for analysis.

Gold labels and rationales are never sent to the model.

Each operational scenario is represented by three independent cases (one per primitive). The runner sends one question per request so request latency and cost remain attributable to that primitive.

## Why rule-authored synthetic cases

The v1 corpus is not claimed to be a random sample of all enterprise decisions. It is a deliberately broad, controlled workload. Every scenario is generated from explicit authored archetypes and context modifiers in `tools/build_corpus.py`. This gives deterministic ground truth, makes licensing straightforward, and prevents an evaluated model from writing its own exam.

The trade-off is that template regularities can exist. Published conclusions should therefore be framed as evidence on this corpus, not universal model rankings. Future corpus versions can add separately licensed public/human datasets while preserving v1 unchanged.

## Frozen suite sizes

- `probe` (3): one call per primitive. Setup only.
- `smoke` (18): six calls per primitive across six domains.
- `quick` (300): stratified iteration set.
- `core` (1,500): substantial development comparison.
- `full` (5,760): all v1 cases and the primary quality result.
- `perf` (180): stratified workload intended for repeated concurrency/timing runs.

The subsets are deterministic and checked in. Do not tune prompts or adapters against `full` after inspecting model-specific failures and still describe the result as untouched evaluation.

## Quality metrics

### Choice

- top-1 accuracy;
- macro-F1;
- multiclass Brier score (sum of squared probability error across options);
- negative log likelihood of the gold option;
- 10-bin expected calibration error using top-option confidence.

When a provider returns only a class and no defensible probability distribution, accuracy/F1 remain valid but Brier/NLL/ECE are left unavailable. The harness records probability coverage rather than converting a hard class into a fake one-hot distribution.

### Noul

- threshold accuracy at 0.5;
- macro-F1 for yes/no;
- binary Brier score;
- binary negative log likelihood;
- 10-bin expected calibration error using confidence in the predicted side.

Noul is evaluated as a probability first; threshold accuracy is only one view.

Classification-only providers may return a boolean without `probability_yes`; in that case accuracy/F1 are still reported and probability metrics are omitted.

### Score

- exact class accuracy using the most probable rubric level when probabilities are available;
- within-±1 level accuracy;
- mean absolute error of the model's expected/fractional score;
- quadratic weighted kappa;
- multiclass Brier/NLL/ECE over score levels when probabilities are available.

The harness also reports MAE of the selected discrete Score level. Expected-score MAE is only calculated when an actual level distribution is available.

## Timing

The primary request latency is wall-clock end-to-end time measured by the benchmark client around the HTTP request. It includes local transport or network/gateway overhead because that is what application code experiences.

Report p50, p90, p95, and p99. `perf` should be repeated at multiple concurrency levels. Do not mix model startup/download time into request latency; startup is an operational metric to record separately when needed.

A fair publication should identify hardware, backend, concurrency, warm/cold conditions, network location for hosted calls, and whether retries occurred.

## Cost

Hosted provider cost is taken from the response when available. For Jev through OpenRouter, current responses can include `usage.cost`; this is preferred over reconstructing cost from a price page after the fact.

If a hosted API exposes token usage but not request-level billed dollars, a provider adapter may calculate cost from those usage counters and a pricing snapshot stored in the run's model configuration. Such reconstructed cost must be documented as such and must not silently use current web pricing when regenerating an old report.

Local models have **provider cost = $0**, not "cost = $0". If `LOCAL_COMPUTE_USD_PER_HOUR` or `--local-usd-per-hour` is supplied, the harness also records a simple modeled compute cost based on request wall time. This is explicitly labeled an estimate and is never substituted for provider cost.

For final reporting, useful derived quantities include cost per 1K/1M decisions and cost per correct decision, but they should not be collapsed into a single leaderboard score with quality.

## Reliability

All provider failures are retained in the result file with attempts and elapsed time. Error rate is part of the summary. Retries are explicit and configurable; timing results with retries should be analyzed separately from clean single-attempt latency.

## Reproducibility

Each run records:

- benchmark git revision when available;
- corpus and suite SHA-256;
- configured and provider-resolved model identifier;
- provider/deployment type;
- concurrency, retries, timeout, and local cost assumption;
- operating system, CPU architecture, Python version, and `nvidia-smi` identity when available;
- raw response, probabilities, token metadata (including cache/reasoning counters when exposed), provider cost plus its basis, and latency per case.

Raw `results.jsonl` is the source of truth. Reports are derived artifacts.
