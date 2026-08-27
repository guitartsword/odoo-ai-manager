from pathlib import Path

import pytest

from odoo_ai_manager.application.skill_catalog import ContextLoader, SkillCatalog
from odoo_ai_manager.domain.models import AccessMode, MutationKind, SkillManifest


def test_catalog_discovers_only_versioned_skills() -> None:
    manifests = SkillCatalog(Path("skills")).list(module="pos")

    assert [manifest.id for manifest in manifests] == ["pos.daily_sales_report"]
    assert manifests[0].access.value == "read_only"


def test_context_loader_combines_transversal_and_module_context() -> None:
    context = ContextLoader(Path(".")).load_module("pos")

    assert "Conocimiento transversal del negocio" in context
    assert "Punto de venta" in context
    assert "res.users.tz" in context


def test_context_loader_loads_skill_instructions() -> None:
    instructions = ContextLoader(Path(".")).load_skill("pos.daily_sales_report")

    assert "Reporte diario de ventas PoS" in instructions
    assert "read_only" in instructions


def test_mutation_manifest_declares_its_kind() -> None:
    manifest = SkillManifest(
        id="purchases.create_draft",
        module="purchases",
        name="create_draft",
        description="Crea una orden sin confirmarla.",
        access=AccessMode.MUTATION,
        mutation_kind=MutationKind.DRAFT,
    )

    assert manifest.mutation_kind is MutationKind.DRAFT


def test_manifest_rejects_inconsistent_mutation_metadata() -> None:
    with pytest.raises(ValueError):
        SkillManifest(
            id="pos.report",
            module="pos",
            name="report",
            description="Consulta datos.",
            access=AccessMode.READ_ONLY,
            mutation_kind=MutationKind.DRAFT,
        )

    with pytest.raises(ValueError):
        SkillManifest(
            id="pos.change",
            module="pos",
            name="change",
            description="Cambia datos.",
            access=AccessMode.MUTATION,
        )
