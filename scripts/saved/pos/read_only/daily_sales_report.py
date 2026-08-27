"""Entry point versionado para la skill de ventas PoS."""

from odoo_ai_manager.modules.pos.daily_sales_report import cli_main


if __name__ == "__main__":
    raise SystemExit(cli_main())
