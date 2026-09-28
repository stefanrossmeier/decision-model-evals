# Active models and selection rationale

The primary matrix is intentionally small. A model is included when it adds a useful deployment point, has a commercially usable path, has enough external evidence to be worth measuring, and can express Choice/Noul/Score without changing the semantic difficulty of the benchmark.

The v1 matrix contains four models:

| Key | Model | Role in the matrix | Deployment |
|---|---|---|---|
| `jev` | TypeSafe Jev 1.13 | hosted reference with native typed decisions | OpenRouter |
| `bosun` | Bosun v3.1 0.6B | tiny/fast local reference | local |
| `decider` | Mapika Decider 4B v2.1 | strong native 4B local decision model | local |
| `semif` | SemIf + Qwen3.5-4B | independent direct-logit 4B approach | local |

Two initially selected models were later removed because their tested deployment paths did not fit the target hardware class. See [EXCLUDED_MODELS.md](EXCLUDED_MODELS.md).

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
