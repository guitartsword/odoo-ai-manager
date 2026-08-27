from pathlib import Path

from odoo_ai_manager.application.skill_catalog import ContextLoader, SkillCatalog


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
