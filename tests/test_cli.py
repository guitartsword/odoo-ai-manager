from odoo_ai_manager.cli import build_parser, main


def test_cli_lists_skills(capsys) -> None:
    result = main(["skills", "list", "--module", "pos"])

    assert result == 0
    assert "pos.daily_sales_report" in capsys.readouterr().out


def test_cli_shows_skill_instructions(capsys) -> None:
    result = main(["skills", "show", "pos.daily_sales_report"])

    assert result == 0
    assert "Reporte diario de ventas PoS" in capsys.readouterr().out


def test_cli_exposes_local_configuration_options() -> None:
    args = build_parser().parse_args(
        ["configure", "--port", "9000", "--no-browser"]
    )

    assert args.command == "configure"
    assert args.port == 9000
    assert args.no_browser is True
