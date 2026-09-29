# Licensing and admission policy

The repository code and authored v1 corpus are Apache-2.0.

Model eligibility depends on how the model is delivered.

## Local models

A local benchmark entrant should have, at minimum:

1. model/weight terms that permit the intended commercial evaluation and deployment use;
2. runtime/code terms compatible with normal commercial deployment;
3. no known published non-commercial adapter restriction that conflicts with the intended use;
4. a public model card/repository sufficient to identify and pin the evaluated artifact.

Julia 1 is a local entrant under this policy. The evaluated `SupersonicLabs/Julia-1` artifact publishes Apache-2.0 terms; the benchmark pins the exact model repository revision and weight hash used by the run.

## Hosted models

A hosted model does not need downloadable weights. It should have a public service/API path with published terms suitable for the intended use, a stable or pinnable model identifier, and enough provider metadata to identify what was evaluated.

Jev is in this category: the benchmark calls the pinned OpenRouter model ID and records the provider-resolved model and exact billed cost returned by the API. This repository makes no claim about a downloadable Jev weight license.

The GPT-6 Luna experiments are also hosted-service entries. They access `openai/gpt-6-luna` through OpenRouter; this repository does not redistribute model weights or assert a downloadable model license.

## What this policy does not establish

These checks are necessary for the project's enterprise-oriented candidate matrix, but they are **not legal advice or enterprise legal approval**. A permissive artifact license does not prove the provenance of every training datum, and hosted service terms can change independently of this repository.

If a model later discloses a conflicting restriction, keep old benchmark results for historical reproducibility but mark the model as no longer eligible for the active enterprise-candidate matrix.

See [MODELS.md](MODELS.md) for the active artifacts and [EXCLUDED_MODELS.md](EXCLUDED_MODELS.md) for models removed on deployment-practicality grounds.
