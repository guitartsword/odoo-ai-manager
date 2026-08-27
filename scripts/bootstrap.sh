#!/usr/bin/env bash
set -euo pipefail

install_missing="${INSTALL_MISSING:-0}"

has_command() {
  command -v "$1" >/dev/null 2>&1
}

if ! has_command python3 && ! has_command python; then
  printf '%s\n' "Falta Python 3.12+. Instala Python con el gestor de paquetes de tu sistema." >&2
  exit 1
fi

if ! has_command git; then
  printf '%s\n' "Falta git. Instala git con el gestor de paquetes de tu sistema." >&2
  exit 1
fi

if ! has_command uv; then
  if [[ "$install_missing" != "1" ]]; then
    printf '%s\n' "Falta uv. Ejecuta INSTALL_MISSING=1 ./scripts/bootstrap.sh para instalarlo." >&2
    exit 1
  fi
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

uv sync --locked
printf '%s\n' "Dependencias instaladas."
