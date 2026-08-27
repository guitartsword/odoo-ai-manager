from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path
from typing import Sequence

from odoo_ai_manager.application.skill_catalog import ContextLoader, SkillCatalog
from odoo_ai_manager.paths import project_root


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Catalogo y herramientas seguras para trabajar con Odoo."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser(
        "doctor",
        help="Revisa que Python, uv y git esten disponibles.",
    )

    configure_parser = subparsers.add_parser(
        "configure",
        help="Configura Odoo mediante un formulario web local.",
    )
    configure_parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Interfaz donde escucha el configurador (por defecto localhost).",
    )
    configure_parser.add_argument(
        "--port",
        type=int,
        default=8765,
        help="Puerto HTTP local (por defecto 8765).",
    )
    configure_parser.add_argument(
        "--env-path",
        type=Path,
        help="Ruta del archivo .env; por defecto, la raiz del proyecto.",
    )
    configure_parser.add_argument(
        "--no-browser",
        action="store_true",
        help="No abrir el navegador automaticamente.",
    )

    skills_parser = subparsers.add_parser("skills", help="Inspecciona skills.")
    skills_subparsers = skills_parser.add_subparsers(
        dest="skills_command",
        required=True,
    )
    list_parser = skills_subparsers.add_parser("list", help="Lista skills.")
    list_parser.add_argument("--module", help="Filtra por modulo.")
    show_parser = skills_subparsers.add_parser(
        "show",
        help="Muestra las instrucciones de una skill.",
    )
    show_parser.add_argument("skill_id")

    context_parser = subparsers.add_parser(
        "context",
        help="Imprime el contexto de negocio y tecnica de un modulo.",
    )
    context_parser.add_argument("module")

    report_parser = subparsers.add_parser(
        "report",
        help="Ejecuta un reporte aprobado.",
    )
    report_subparsers = report_parser.add_subparsers(
        dest="report_name",
        required=True,
    )
    pos_parser = report_subparsers.add_parser(
        "pos-daily-sales",
        help="Genera el reporte de ventas PoS.",
    )
    pos_parser.add_argument("--start-date", required=True)
    pos_parser.add_argument("--end-date")
    pos_parser.add_argument("--output-path")
    return parser


def _run_doctor() -> int:
    checks = {
        "python": shutil.which("python") or shutil.which("python3"),
        "uv": shutil.which("uv"),
        "git": shutil.which("git"),
    }
    for name, path in checks.items():
        print(f"{name}: {path or 'NO ENCONTRADO'}")
    python_version = sys.version_info[:3]
    print(f"python version: {'.'.join(str(part) for part in python_version)}")
    env_status = "configurado" if (project_root() / ".env").exists() else "pendiente (.env no existe)"
    print(f"odoo credentials: {env_status}")
    python_is_supported = sys.version_info >= (3, 12)
    return 0 if all(checks.values()) and python_is_supported else 1


def _run_skill_list(module: str | None) -> int:
    manifests = SkillCatalog().list(module)
    if not manifests:
        print("No hay skills para el filtro indicado.")
        return 0
    for manifest in manifests:
        mutation_kind = manifest.mutation_kind.value if manifest.mutation_kind else "-"
        print(
            f"{manifest.id}\t{manifest.access.value}\t{mutation_kind}\t"
            f"{manifest.status.value}\t{manifest.description}"
        )
    return 0


def _run_skill_show(skill_id: str) -> int:
    print(ContextLoader().load_skill(skill_id))
    return 0


def _run_report(args: argparse.Namespace) -> int:
    from odoo_ai_manager.modules.pos.daily_sales_report import cli_main

    forwarded_args = ["--start-date", args.start_date]
    if args.end_date:
        forwarded_args.extend(["--end-date", args.end_date])
    if args.output_path:
        forwarded_args.extend(["--output-path", args.output_path])
    return cli_main(forwarded_args)


def _run_configure(args: argparse.Namespace) -> int:
    from odoo_ai_manager.configuration import run_configuration_server

    run_configuration_server(
        host=args.host,
        port=args.port,
        env_path=args.env_path or project_root() / ".env",
        open_browser=not args.no_browser,
    )
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "doctor":
            return _run_doctor()
        if args.command == "configure":
            return _run_configure(args)
        if args.command == "skills":
            if args.skills_command == "list":
                return _run_skill_list(args.module)
            return _run_skill_show(args.skill_id)
        if args.command == "context":
            print(ContextLoader().load_module(args.module))
            return 0
        if args.command == "report":
            return _run_report(args)
    except (FileNotFoundError, KeyError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    raise AssertionError(f"Comando no soportado: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
