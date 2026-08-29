#!/usr/bin/env bash
set -euo pipefail

install_missing="${INSTALL_MISSING:-0}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --install-missing)
      install_missing=1
      ;;
    *)
      printf '%s\n' "Argumento no reconocido: $1" >&2
      exit 2
      ;;
  esac
  shift
done

has_command() {
  command -v "$1" >/dev/null 2>&1
}

find_supported_python() {
  local candidate
  for candidate in python3 python; do
    if has_command "$candidate" && "$candidate" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 12) else 1)' >/dev/null 2>&1; then
      printf '%s' "$candidate"
      return 0
    fi
  done
  return 1
}

run_as_root() {
  if [[ "$(id -u)" -eq 0 ]]; then
    "$@"
  elif has_command sudo; then
    sudo "$@"
  else
    printf '%s\n' "Se necesitan permisos de administrador para instalar herramientas y no se encontro sudo." >&2
    return 1
  fi
}

install_system_tools() {
  case "$(uname -s)" in
    Darwin)
      if ! has_command brew; then
        printf '%s\n' "No se encontro Homebrew. El agente debe instalarlo o resolver la instalacion manualmente." >&2
        return 1
      fi
      brew install git python curl
      ;;
    Linux)
      if has_command apt-get; then
        run_as_root apt-get update
        run_as_root apt-get install -y git python3 curl
      elif has_command dnf; then
        run_as_root dnf install -y git python3 curl
      elif has_command pacman; then
        run_as_root pacman -Sy --noconfirm git python curl
      elif has_command zypper; then
        run_as_root zypper --non-interactive install git python3 curl
      else
        printf '%s\n' "No se encontro un gestor de paquetes compatible para instalar git y Python." >&2
        return 1
      fi
      ;;
    *)
      printf '%s\n' "Sistema operativo no compatible para instalacion automatica: $(uname -s)." >&2
      return 1
      ;;
  esac
}

python_command="$(find_supported_python || true)"
git_missing=0
if ! has_command git; then
  git_missing=1
fi
curl_missing=0
if ! has_command curl; then
  curl_missing=1
fi
if [[ -z "$python_command" || "$git_missing" -eq 1 || "$curl_missing" -eq 1 ]] && [[ "$install_missing" == "1" ]]; then
  install_system_tools
  python_command="$(find_supported_python || true)"
fi

if [[ -z "$python_command" ]]; then
  printf '%s\n' "Falta Python 3.12+. Ejecuta este script con --install-missing o resuelve la instalacion manualmente." >&2
  exit 1
fi

if ! has_command git; then
  printf '%s\n' "Falta git. Ejecuta este script con --install-missing o resuelve la instalacion manualmente." >&2
  exit 1
fi

if ! has_command uv; then
  if [[ "$install_missing" != "1" ]]; then
    printf '%s\n' "Falta uv. Ejecuta este script con --install-missing o INSTALL_MISSING=1 para instalarlo." >&2
    exit 1
  fi
  if ! has_command curl; then
    printf '%s\n' "Falta curl y no se puede instalar uv automaticamente." >&2
    exit 1
  fi
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
fi

if [[ -f pyproject.toml ]]; then
  uv sync --locked
  printf '%s\n' "Dependencias instaladas."
else
  printf '%s\n' "Herramientas listas. No se encontro pyproject.toml; ejecuta este script de nuevo dentro del checkout."
fi
