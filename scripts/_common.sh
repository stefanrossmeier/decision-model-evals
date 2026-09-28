#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODELS_DIR="${ROOT}/.models"
mkdir -p "${MODELS_DIR}"

need() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "error: required command '$1' not found" >&2
    exit 2
  fi
}

need_uv() {
  if ! command -v uv >/dev/null 2>&1; then
    echo "error: uv is required. Install it from https://docs.astral.sh/uv/getting-started/installation/" >&2
    exit 2
  fi
}

have_nvidia_cuda() {
  command -v nvidia-smi >/dev/null 2>&1 && nvidia-smi -L >/dev/null 2>&1
}

max_nvidia_memory_mib() {
  if ! have_nvidia_cuda; then
    echo 0
    return
  fi
  nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null \
    | awk 'BEGIN { max=0 } { if ($1+0 > max) max=$1+0 } END { print int(max) }'
}

require_cuda_model() {
  local model="$1"
  local min_mib="$2"
  local requirement="$3"

  if [[ "${ALLOW_UNSUPPORTED_LOCAL:-0}" == "1" ]]; then
    echo "warning: ALLOW_UNSUPPORTED_LOCAL=1; skipping CUDA hardware guard for ${model}" >&2
    return 0
  fi

  if ! have_nvidia_cuda; then
    cat >&2 <<MSG
error: ${model} is not supported by this repository on the detected machine.

${requirement}
The upstream runtime used by this benchmark requires CUDA/NVIDIA. Apple MPS is not a
supported substitute for this model path. Run this model on a Linux CUDA host, or set
ALLOW_UNSUPPORTED_LOCAL=1 only if you intentionally want to experiment with an
unsupported upstream configuration.
MSG
    exit 2
  fi

  local available
  available="$(max_nvidia_memory_mib)"
  if (( available < min_mib )); then
    cat >&2 <<MSG
error: ${model} needs more GPU memory than the largest detected NVIDIA GPU exposes.
required by this benchmark preflight: >= ${min_mib} MiB
largest detected GPU: ${available} MiB
${requirement}
Set ALLOW_UNSUPPORTED_LOCAL=1 only if you intentionally want to bypass this guard.
MSG
    exit 2
  fi
}

require_free_disk_gib() {
  local path="$1"
  local required_gib="$2"
  mkdir -p "$path"
  local available_kib
  available_kib="$(df -Pk "$path" | awk 'NR==2 {print $4}')"
  local required_kib=$(( required_gib * 1024 * 1024 ))
  if (( available_kib < required_kib )); then
    local available_gib=$(( available_kib / 1024 / 1024 ))
    echo "error: insufficient free disk under $path: ${available_gib} GiB available, ${required_gib} GiB required" >&2
    exit 2
  fi
}

hf_auth_hint() {
  if [[ -z "${HF_TOKEN:-}" ]]; then
    echo "note: HF_TOKEN is not set; Hugging Face downloads will be unauthenticated and may be rate-limited." >&2
  fi
}
