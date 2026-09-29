# Active models and selection rationale

The primary matrix is intentionally small. A model is included when it adds a useful deployment point, has a commercially usable path, has enough external evidence to be worth measuring, and can express Choice/Noul/Score without changing the semantic difficulty of the benchmark.

The historical v1 matrix contains four models:

| Key | Model | Role in the matrix | Deployment |
|---|---|---|---|
| `jev` | TypeSafe Jev 1.13 | hosted reference with native typed decisions | OpenRouter |
| `bosun` | Bosun v3.1 0.6B | tiny/fast local reference | local |
| `decider` | Mapika Decider 4B v2.1 | strong native 4B local decision model | local |
| `semif` | SemIf + Qwen3.5-4B | independent direct-logit 4B approach | local |

Two initially selected models were later removed because their tested deployment paths did not fit the target hardware class. See [EXCLUDED_MODELS.md](EXCLUDED_MODELS.md).

Three additional entries in `configs/models.yaml` are **post-v1 entrants**, not members of the original primary matrix. `julia1` is a specialized tiny local decision model; `luna-structured` and `luna-classifier` are hosted GPT-6 Luna experiments. All reuse the frozen v1 corpus so their quality can be compared directly by corpus/suite hash without rewriting the historical four-model result.

Upstream details below were checked during the v1 benchmark work in September 2026. Licenses are upstream-published terms, not legal advice.

## Jev 1.13 (`jev`)

- Upstream/API: [OpenRouter — TypeSafe Jev 1.13](https://openrouter.ai/typesafe/jev-1.13)
- Configured model ID: `typesafe/jev-1.13`
- Transport: OpenRouter Decisions API, `POST https://openrouter.ai/api/alpha/decisions`
- Authentication: `OPENROUTER_API_KEY`
- Why included: native Choice/Noul/Score semantics and a hosted reference point with no local model/runtime management.
- Reproducibility: the public v1 full run resolved to `typesafe/jev-1.13-20260917`; the harness records the resolved model returned by the provider.
- Cost: use provider-reported billing from each run rather than reconstructing historic cost from a later price page.

Jev is a hosted service entry. The project does not claim a downloadable Jev weight license or local deployment path.

## Julia 1 (`julia1`)

- Weights/runtime: [SupersonicLabs/Julia-1](https://huggingface.co/SupersonicLabs/Julia-1).
- Base encoder: `jhu-clsp/mmBERT-small`, from the multilingual ModernBERT family.
- Size: **144.3M parameters**, with a published FP32 checkpoint of about **550.5 MiB**.
- License: Apache-2.0 on the published model artifact.
- Benchmark pin: Julia repository revision `a85b127321d580d65176c89ced8273f305745d85`; weight SHA-256 `df853bf7fe424420011f3d0c47a05d7341aa9eefa7fb9f203ea4aada4ad95b72`.
- Runtime pins: `torch==2.14.0`, `transformers==5.0.0`, strict encoding, 8,192-token runtime limit, 512-token question/options head budget, marker-only head disabled.
- Transport: thin local `/v1/systemone` adapter around Julia's native named-question API; the adapter does not replace Julia's scoring logic.
- Default endpoint: `http://127.0.0.1:8013/v1/systemone`.
- Mac/Linux: CPU is the supported default in this benchmark; CUDA can be selected with `JULIA_DEVICE=cuda`. The published Julia runtime does not expose an MPS path.
- Why included: it is much smaller than the earlier local entrants and directly tests whether a compact specialized encoder can provide useful Jev-like Choice/Noul/Score behavior on ordinary CPU hardware.

The pinned revision is important because it preserves descriptive Boolean criteria in the named-question API. The upstream project also publishes a CPU FP32 typed-decision reproduction using the same Torch/Transformers versions; that reproduction is a different dataset and should not be treated as a substitute for this benchmark.

The canonical post-v1 full run is `20260929T172106Z-julia1-cdeac5d1`. It completed all 5,760 cases with zero errors and scored **42.20% overall** (44.95% Choice, 58.54% Noul, 23.12% Score exact). Its full-run p50/p95 latency was **27.0/31.2 ms** on the recorded arm64 macOS CPU host. This is substantially faster than the other measured local paths, but quality on this corpus is also substantially lower. See [BENCHMARK_RESULTS.md](BENCHMARK_RESULTS.md).

## GPT-6 Luna experiments (`luna-structured`, `luna-classifier`)

- API/model: OpenRouter Chat Completions API with `openai/gpt-6-luna`.
- Authentication: `OPENROUTER_API_KEY`.
- Deployment: hosted through OpenRouter, pinned to the OpenAI provider with fallbacks disabled.
- Fixed supported controls: reasoning effort `none`, seed `0`, strict Structured Outputs, no few-shot examples.
- `luna-structured`: strict JSON Schema constrains the selected Choice/Noul/Score value directly.
- `luna-classifier`: maps legal outputs to `A/B/C/...` and uses a strict enum schema for the selected class label before mapping back to the original value.
- OpenRouter's current GPT-6 Luna endpoint metadata does not advertise `temperature`, `logprobs`, or `top_logprobs`; these OpenRouter-only experiments therefore do not claim temperature-zero sampling or model probability distributions.
- Purpose: test whether a low-cost general LLM, deliberately invoked as a classifier, can approach the existing Jev result without changing the corpus.
- Cost: use OpenRouter's request-reported `usage.cost` when available, preserving the same provider-reported cost basis used for Jev.

These entries were added after the original v1 four-model benchmark. Their results should be reported alongside, not silently inserted into, the historical headline table. Both full runs are now complete: `luna-structured` scored **73.12%** and `luna-classifier` **73.14%**, versus the existing Jev result of **74.50%** on the same frozen corpus. See [LUNA_VS_JEV.md](LUNA_VS_JEV.md) for the comparison and performance caveats.

## Bosun v3.1 0.6B (`bosun`)

- Weights: [Hanno-Labs/bosun-v3.1-0.6b](https://huggingface.co/Hanno-Labs/bosun-v3.1-0.6b)
- Upstream license: Apache-2.0 on the model card.
- Size: ~0.6B parameters; the benchmark uses it as the small local reference.
- Runtime pinned here: `jev-compatible-server[transformers]==0.1.1`
- Transport: native Jev-compatible `/v1/systemone`
- Default endpoint: `http://127.0.0.1:8000/v1/systemone`
- Why included: materially smaller/faster than the 4B candidates and practical on the target Mac/Linux class.

The v1 full run completed successfully on the target arm64 Mac. The server did not expose useful input-token or provider-side timing telemetry in these runs, so Bosun's performance reporting uses client-observed latency.

## Decider 4B v2.1 (`decider`)

- Upstream code: [Mapika/decider](https://github.com/Mapika/decider)
- Weights: `Mapika/decider-4b`, pinned to Hub commit `eb5fbdfc9448473ec25e399882912863afbdb70e`
- Release: v2.1
- Runtime pinned here: `decider-ai[serve]==1.4.0`
- License: Apache-2.0 for the published project/model artifacts used here; base model `Qwen3.5-4B-Base` is also published as Apache-2.0.
- Size: upstream reports ~8.4 GB BF16 weights; allow additional cache/runtime space.
- Transport: native `POST /v1/systemone`
- Default endpoint: `http://127.0.0.1:8011/v1/systemone`
- Mac: the runtime supports MPS; the v1 evaluation validated it on the target Apple Silicon machine.
- Linux/VPS: CUDA is preferred for performance; CPU is a functional but slower reference path.
- Why included: strong 4B decision quality with native System One semantics and a realistic local deployment path.

Setup installs the runtime; weights download on first start.

## SemIf + Qwen3.5-4B (`semif`)

- Upstream project: [SemIf](https://github.com/TheoLeeCJ/SemIf), formerly OpenJev.
- Benchmark source pin: commit `1f2dea3` from [`TheoLeeCJ/SemIf-OpenJev`](https://github.com/TheoLeeCJ/SemIf-OpenJev); setup records the resolved full commit in `.models/semif/REVISION.txt`.
- Model: [Qwen/Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B), pinned to revision `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`.
- License: SemIf code MIT; Qwen3.5-4B model card publishes Apache-2.0.
- Size: ~9.34 GB repository payload for the pinned BF16 model snapshot used here.
- Semantics: direct last-position option-logit scoring rather than a native System One HTTP service.
- Adapter: `scripts/semif-server.py` preserves runtime options; Noul maps to explicit false/true options and Score to ordered rubric levels with a probability-weighted expected score.
- Default endpoint: `http://127.0.0.1:8012/v1/systemone`
- Mac: this benchmark server uses the upstream PyTorch/MPS direct scorer. Upstream also supports an MLX backend, but MLX timings are not mixed with the v1 MPS results.
- Linux/VPS: CUDA is the normal performance path; `SEMIF_DEVICE=cpu` provides a much slower Torch CPU reference.
- Why included: an independent 4B decision approach with different scoring mechanics and viable Mac/Linux paths.

SemIf probabilities are conditional option scores and should not automatically be treated as operationally calibrated probabilities.

## Admission policy

For **local** entrants, published code and weight terms must permit the intended commercial evaluation/deployment use. For **hosted** entrants, the service must expose published terms and an API suitable for the intended use; downloadable weight licensing is not required.

All primary entrants must also have:

1. a realistic deployment path for the role they represent;
2. enough external evidence to justify benchmarking;
3. Choice/Noul/Score support or a semantics-preserving adapter;
4. an identifiable, pinnable model/runtime configuration.

The corpus is model-independent. Adding or removing a model never changes benchmark cases.
