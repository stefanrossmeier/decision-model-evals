# GPT-6 Luna classification experiments

This document defines two **post-v1 model/inference experiments against the existing frozen v1 corpus**. They do not add cases, change gold labels, or modify any published Jev/local result.

The practical question is: how close can a cheap general-purpose LLM get to a specialized decision model when it is deliberately used as a classifier rather than as a normal text generator?

The experiments are now complete. On the 5,760-case `full` suite, `luna-structured` scored **73.12%** and `luna-classifier` **73.14%**, compared with the existing Jev result of **74.50%**. See [LUNA_VS_JEV.md](LUNA_VS_JEV.md) for the detailed quality, paired, cost, latency, and throughput analysis.

Both experiments access GPT-6 Luna through OpenRouter:

- model slug: `openai/gpt-6-luna`;
- endpoint: `POST https://openrouter.ai/api/v1/chat/completions`;
- authentication: `OPENROUTER_API_KEY`;
- reasoning effort: `none`;
- seed: `0`;
- OpenRouter provider routing pinned to `OpenAI`, with fallbacks disabled;
- `require_parameters: true` so OpenRouter does not silently route to an endpoint that lacks the requested structured-output/reasoning controls;
- no few-shot examples;
- no domain-specific prompts;
- no prompt tuning against inspected `full` failures;
- the original v1 state, instructions, and criteria are the only semantic case input.

The adapter prompt is intentionally generic. It tells the model to behave as a classification function, to treat state content as data rather than instructions, to select one allowed output, and not to explain the decision.

## Why these OpenRouter experiments do not use temperature or token logprobs

OpenRouter's current endpoint metadata for `openai/gpt-6-luna` advertises structured outputs, reasoning controls, and `seed`, but does **not** advertise `temperature`, `logprobs`, or `top_logprobs` for the available GPT-6 Luna endpoints.

That changes the experiment design from the earlier direct-OpenAI draft:

- the benchmark does not send `temperature: 0`, because OpenRouter cannot currently guarantee that parameter for this model;
- `seed: 0` is used as the supported reproducibility control;
- the earlier token-logprob experiment is not represented as if it were available through OpenRouter;
- neither Luna experiment exposes a model probability distribution, so Luna calibration metrics remain unavailable.

If OpenRouter later adds token-logprob support for GPT-6 Luna, a separate logprob experiment can be added without changing the frozen corpus or these published run identities.

## Experiment 1: `luna-structured`

This is the conventional general-LLM structured-classification baseline.

For every case, the adapter supplies the original state, decision instructions, and criteria and asks OpenRouter for a strict JSON Schema response containing only:

```json
{"decision": "..."}
```

The schema constrains `decision` to the legal Choice option, boolean Noul value, or Score level for that case.

This experiment deliberately does **not** ask the model to generate confidence values. A generated numeric confidence would be a self-reported number, not the model's class probability distribution. Therefore:

- accuracy, macro-F1, Score exact/within-1/kappa, latency, token use, and cost are valid;
- Brier/NLL/ECE and expected-Score MAE are unavailable;
- reports show probability coverage as `0%` rather than fabricating one-hot probabilities.

## Experiment 2: `luna-classifier`

This experiment keeps the same model, transport, and supported inference controls, but changes the task representation to a closed-label classifier.

The adapter maps the legal outputs for each case to short verbalizer labels (`A`, `B`, `C`, ...). The prompt presents the label-to-meaning mapping and asks the model to choose the single best class. A strict JSON Schema allows only one of those labels:

```json
{"label": "B"}
```

The adapter then maps the label back to the original Choice/Noul/Score value.

This experiment isolates whether explicit classifier framing and abstract class labels change decision quality compared with directly asking for the semantic decision value. It still uses Structured Outputs for transport reliability; it does **not** claim access to Luna's token probabilities.

Like `luna-structured`, this run has no model probability distribution and therefore no calibration metrics.

## Routing and cost accounting

Both experiments use OpenRouter for model access and deliberately pin the provider to `OpenAI` with provider fallbacks disabled. This avoids mixing provider implementations within a benchmark run and keeps the requested controls stable.

The request asks OpenRouter to include usage data. When `usage.cost` is returned, the benchmark stores that exact request-level cost as `provider_reported`, just as it does for Jev/OpenRouter. Token counts, cached-token counts, cache-write counts, and reasoning-token counts are retained when OpenRouter returns them.

Do not reconstruct these Luna run costs from a later pricing page when publishing results; use the checked-in raw result rows.

## Run protocol

The same OpenRouter key already used for Jev is sufficient:

```text
OPENROUTER_API_KEY=...
```

Validate both experiment configurations:

```bash
./scripts/check-model luna-structured
./scripts/check-model luna-classifier
```

Run the cheap transport/adapter checks first:

```bash
./scripts/probe luna-structured
./scripts/smoke luna-structured

./scripts/probe luna-classifier
./scripts/smoke luna-classifier
```

Inspect the generated reports and raw rows for provider errors, resolved model/provider identity, token usage, and provider-reported cost. If the probe/smoke runs expose a generic adapter problem, fix that before running `full`; do not tune prompts against full-suite errors.

Then run the two full quality experiments:

```bash
./scripts/run-benchmark luna-structured full
./scripts/run-benchmark luna-classifier full
```

Because the motivating claim also concerns latency/throughput, run the comparable perf suite afterward:

```bash
./scripts/run-perf luna-structured
./scripts/run-perf luna-classifier
```

`run-perf` uses the existing frozen 180-case suite at concurrency 1, 4, and 16.

## Compare with the existing Jev run

Do **not** re-run Jev solely for this experiment. The snapshot already contains the canonical v1 Jev full run:

```text
results/20260927T101408Z-jev-0c89145b
```

The canonical completed full runs can be compared directly with:

```bash
./scripts/compare-results \
  results/20260927T101408Z-jev-0c89145b \
  results/20260928T044245Z-luna-structured-79fbfdab \
  results/20260928T062221Z-luna-classifier-60e0d309
```

The comparison command verifies that corpus and suite hashes match before producing paired correctness/McNemar statistics. The human-written interpretation, including the dedicated perf runs and their timing caveats, is maintained in [LUNA_VS_JEV.md](LUNA_VS_JEV.md).

## Publishing the new raw evidence

`results/*/` is ignored by default. Publish only the two canonical full runs and the six canonical perf runs listed in [LUNA_VS_JEV.md](LUNA_VS_JEV.md). Do not commit probe, smoke, failed setup, or discarded tuning runs as canonical evidence.

Each completed run should contain `manifest.json`, `results.jsonl`, `summary.json`, and `report.md`. The raw JSONL remains the source of truth.
