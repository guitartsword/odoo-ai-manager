from __future__ import annotations

import os
from pathlib import Path


def project_root(start: Path | None = None) -> Path:
    """Encuentra la raiz del checkout sin depender del directorio actual."""

    configured_root = os.getenv("ODOO_AI_MANAGER_ROOT")
    if configured_root:
        return Path(configured_root).expanduser().resolve()

    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / "pyproject.toml").is_file() and (candidate / "skills").is_dir():
            return candidate
    return current
