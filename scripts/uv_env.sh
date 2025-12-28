#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UV_BIN="${REPO_ROOT}/.tools/uv"
VENV_DIR="${REPO_ROOT}/.venv"
CACHE_DIR="${REPO_ROOT}/.cache"

# Force caches into the repo (useful on locked-down systems)
export XDG_CACHE_HOME="${CACHE_DIR}"
export UV_CACHE_DIR="${CACHE_DIR}/uv"

usage() {
  cat <<'USAGE'
Usage:
  scripts/uv_env.sh install-uv
  scripts/uv_env.sh venv
  scripts/uv_env.sh run <script>

Examples:
  scripts/uv_env.sh install-uv
  scripts/uv_env.sh venv
  scripts/uv_env.sh run python/03_baseline_concat_pca.py
USAGE
}

install_uv() {
  mkdir -p "${REPO_ROOT}/.tools" "${UV_CACHE_DIR}"
  if [[ -x "${UV_BIN}" ]]; then
    "${UV_BIN}" --version
    exit 0
  fi

  # Requires network access.
  curl -LsSf https://astral.sh/uv/install.sh | UV_INSTALL_DIR="${REPO_ROOT}/.tools" sh
  "${UV_BIN}" --version
}

make_venv() {
  mkdir -p "${UV_CACHE_DIR}"
  if [[ ! -x "${UV_BIN}" ]]; then
    echo "uv not found at ${UV_BIN}. Run: scripts/uv_env.sh install-uv" >&2
    exit 1
  fi

  "${UV_BIN}" venv --system-site-packages "${VENV_DIR}"
  echo "Created venv at ${VENV_DIR}"
  echo "Activate with: source ${VENV_DIR}/bin/activate"
}

run_script() {
  local target="${1:-}"
  if [[ -z "${target}" ]]; then
    echo "Missing script path." >&2
    usage
    exit 2
  fi

  if [[ ! -x "${VENV_DIR}/bin/python" ]]; then
    echo "venv not found at ${VENV_DIR}. Run: scripts/uv_env.sh venv" >&2
    exit 1
  fi

  "${VENV_DIR}/bin/python" "${REPO_ROOT}/${target}"
}

cmd="${1:-}"
case "${cmd}" in
  install-uv) install_uv ;;
  venv) make_venv ;;
  run) shift; run_script "$@" ;;
  *) usage; exit 2 ;;
esac
