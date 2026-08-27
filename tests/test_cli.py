from odoo_ai_manager.cli import main


def test_cli_lists_skills(capsys) -> None:
    result = main(["skills", "list", "--module", "pos"])

    assert result == 0
    assert "pos.daily_sales_report" in capsys.readouterr().out


def test_cli_shows_skill_instructions(capsys) -> None:
    result = main(["skills", "show", "pos.daily_sales_report"])

    assert result == 0
    assert "Reporte diario de ventas PoS" in capsys.readouterr().out
