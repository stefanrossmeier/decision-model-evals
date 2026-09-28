# Quick start

This guide gets one model from setup to a trustworthy benchmark run. Start with `probe`, then `smoke`, then `quick`. Do not jump directly to `full` until the cheap checks are clean.

## 1. Repository setup

Requirements:

- macOS or Linux;
- Python 3.11+;
- Git;
- [`uv`](https://docs.astral.sh/uv/).

From the repository root:

```bash
./scripts/setup
```

This installs the benchmark environment, validates the corpus/configuration, and creates `.env` from `.env.example` if `.env` does not already exist.

## 2. Choose a model

### Hosted Jev

Add an OpenRouter API key to `.env`:

```text
OPENROUTER_API_KEY=...
```

Check configuration and run the cheap validation suites:

```bash
./scripts/check-model jev
./scripts/probe jev
./scripts/smoke jev
```

Jev does not require a local server.

### GPT-6 Luna classification experiments

These are post-v1 comparators against the same frozen corpus, not replacements for the original four-model result. They use the same OpenRouter credential as Jev:

```text
OPENROUTER_API_KEY=...
```

There are two fixed inference modes:

```bash
./scripts/check-model luna-structured
./scripts/probe luna-structured
./scripts/smoke luna-structured

./scripts/check-model luna-classifier
./scripts/probe luna-classifier
./scripts/smoke luna-classifier
```

Both use OpenRouter model `openai/gpt-6-luna`, reasoning effort `none`, seed `0`, provider pinning to OpenAI, and no few-shot examples. `luna-structured` asks directly for the legal semantic decision. `luna-classifier` maps legal decisions to `A/B/C/...` labels before classification. OpenRouter currently does not advertise temperature or token-logprob support for GPT-6 Luna, so neither run exposes calibration probabilities.

See [LUNA_EXPERIMENTS.md](LUNA_EXPERIMENTS.md) before running `full`.

### Bosun

```bash
./scripts/setup-model bosun
./scripts/check-model bosun
```

Start the model in terminal 1:

```bash
./scripts/start-model bosun
```

Then in terminal 2:

```bash
./scripts/probe bosun
./scripts/smoke bosun
```

Bosun uses `127.0.0.1:8000` by default.

### Decider

```bash
./scripts/setup-model decider
./scripts/check-model decider
```

The ~8.4 GB BF16 weights download on first start:

```bash
./scripts/start-model decider
```

In another terminal:

```bash
./scripts/probe decider
./scripts/smoke decider
```

Decider uses `127.0.0.1:8011` by default.

### SemIf

```bash
./scripts/setup-model semif
./scripts/check-model semif
```

The pinned Qwen3.5-4B repository payload (~9.34 GB) downloads on first start:

```bash
./scripts/start-model semif
```

In another terminal:

```bash
./scripts/probe semif
./scripts/smoke semif
```

SemIf uses `127.0.0.1:8012` by default. On Apple Silicon this benchmark adapter uses PyTorch/MPS. Warnings about reference implementations for Qwen3.5 hybrid-attention kernels are expected on that path and affect speed, not request correctness.

## 3. Run the benchmark

Once `probe` and `smoke` are clean:

```bash
./scripts/run-benchmark MODEL quick
```

Inspect the generated report before committing to the full run. Then:

```bash
./scripts/run-benchmark MODEL full
./scripts/run-perf MODEL
```

`run-perf` uses the frozen 180-case perf suite at concurrency 1, 4, and 16 by default.

The optional `core` suite is useful during development:

```bash
./scripts/run-benchmark MODEL core
```

## 4. Find the outputs

Every run creates a directory under `results/` with a timestamp/model/run-id name. A completed run contains:

```text
manifest.json
results.jsonl
summary.json
report.md
```

`manifest.json` is written when the run starts. In the current runner, `results.jsonl`, `summary.json`, and `report.md` are finalized only after the suite completes, so a long-running `full` directory can contain only the manifest while work is still in progress.

`results.jsonl` is the raw source of truth. Keep it if you want to recompute reports or do paired comparisons later.

## 5. Compare completed runs

Pass two or more completed run directories:

```bash
./scripts/compare-results \
  results/<run-a> \
  results/<run-b> \
  results/<run-c>
```

The comparison machinery uses aligned case IDs and includes paired statistics where applicable.

## 6. Common problems

### Port already in use

If a local server fails to bind, check whether another application already owns its port. On systems with `lsof`:

```bash
lsof -nP -iTCP:8000 -sTCP:LISTEN
lsof -nP -iTCP:8011 -sTCP:LISTEN
lsof -nP -iTCP:8012 -sTCP:LISTEN
```

This matters especially for port 8000, which is commonly used by other local inference servers.

### Hosted Jev configuration error

```bash
./scripts/check-model jev
```

If it reports a missing key, set `OPENROUTER_API_KEY` in `.env` or the shell environment.

### Provider/transport errors

Probe and smoke intentionally fail non-zero when requests fail. Do not treat a generated report with transport errors as a valid model result.

## 7. Validate repository changes

Before publishing or opening a pull request:

```bash
./scripts/test-unit
./scripts/test-quality
```

For model pins, backend caveats, and disk/runtime requirements, see [MODELS.md](MODELS.md).
