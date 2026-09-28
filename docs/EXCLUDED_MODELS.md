# Models excluded from the primary benchmark

The primary matrix is a **deployment-practical** benchmark, not a catalog of every strong decision model. Two models were part of the initial candidate set and were removed after hands-on setup testing.

| Model | Why it was considered | Why it was excluded |
|---|---|---|
| JevK5 v0.2 | Strong Jev-style decision model with a native System One interface and strong public benchmark evidence. | The published `jevk5-serve` path used in this project required NVIDIA CUDA. On Apple Silicon it failed with `AssertionError: Torch not compiled with CUDA enabled`. The observed download was ~8.6 GB. |
| AutoJev-27B | Benchmark-strong open decision model with a System One-style interface. | The tested model occupied ~50–52 GB, loading failed part-way through on the Mac, and the published runtime requirements are in the large-GPU class. |

Both exclusions are about **deployment practicality, not model quality**.

The target primary matrix needs a realistic path across the intended deployment class: a modern MacBook for local development/testing and an ordinary reasonably provisioned Linux/VPS environment for server deployment. The project deliberately does not invent an unofficial runtime solely to keep a model in the comparison.

Historical results may still be useful when labelled with the exact old model/runtime configuration, but neither JevK5 nor AutoJev-27B is exposed by the normal setup/start/probe/smoke workflow.
