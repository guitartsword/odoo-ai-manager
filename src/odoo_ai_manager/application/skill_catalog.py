from __future__ import annotations

import tomllib
from pathlib import Path

from odoo_ai_manager.domain.models import SkillManifest
from odoo_ai_manager.paths import project_root


class SkillCatalog:
    """Descubre solo skills versionadas con un manifiesto valido."""

    def __init__(self, root: Path | None = None) -> None:
        self._root = root or project_root() / "skills"

    def list(self, module: str | None = None) -> list[SkillManifest]:
        if not self._root.exists():
            return []
        trusted_root = self._root.resolve()
        manifests: list[SkillManifest] = []
        for manifest_path in sorted(self._root.glob("*/*/skill.toml")):
            if not manifest_path.resolve().is_relative_to(trusted_root):
                raise ValueError(f"Manifest fuera de la raiz de skills: {manifest_path}")
            manifest = SkillManifest.model_validate(
                tomllib.loads(manifest_path.read_text(encoding="utf-8"))
            )
            skill_dir = manifest_path.parent
            module_dir = skill_dir.parent
            if manifest.name != skill_dir.name or manifest.module != module_dir.name:
                raise ValueError(f"El manifest no coincide con su ruta: {manifest_path}")
            if module is None or manifest.module == module:
                manifests.append(manifest)
        return manifests

    def get(self, skill_id: str) -> SkillManifest:
        for manifest in self.list():
            if manifest.id == skill_id:
                return manifest
        raise KeyError(f"No existe la skill: {skill_id}")


class ContextLoader:
    """Carga la memoria relevante sin leer scripts temporales."""

    def __init__(self, root: Path | None = None) -> None:
        self._root = root or project_root()

    def load_module(self, module: str) -> str:
        if not module or Path(module).name != module:
            raise ValueError(f"Nombre de modulo invalido: {module}")
        paths = [
            self._root / "AGENTS.md",
            self._root / "knowledge" / "business.md",
            self._root / "knowledge" / "technical.md",
            self._root / "modules" / module / "business.md",
            self._root / "modules" / module / "technical.md",
        ]
        module_root = self._root / "modules" / module
        if not module_root.is_dir():
            raise FileNotFoundError(f"No existe contexto para el modulo: {module}")
        sections: list[str] = []
        for path in paths:
            if path.exists():
                sections.append(f"<!-- {path.as_posix()} -->\n{path.read_text(encoding='utf-8')}")
        if len(sections) < 5:
            raise FileNotFoundError(f"No existe contexto para el modulo: {module}")
        return "\n\n".join(sections)

    def load_skill(self, skill_id: str) -> str:
        catalog = SkillCatalog(self._root / "skills")
        manifest = catalog.get(skill_id)
        path = self._root / "skills" / manifest.module / manifest.name / "SKILL.md"
        if not path.exists():
            raise FileNotFoundError(f"No existe SKILL.md para: {skill_id}")
        return path.read_text(encoding="utf-8")
