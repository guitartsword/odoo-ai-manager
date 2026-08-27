from __future__ import annotations

import html
import json
import os
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import parse_qs

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field, SecretStr, field_validator

from odoo_ai_manager.domain.models import DraftWorkflow


class OdooConnectionForm(BaseModel):
    """Valores que el usuario introduce en el configurador local."""

    model_config = ConfigDict(str_strip_whitespace=True)

    odoo_version: str = Field(min_length=1, max_length=30)
    domain: AnyHttpUrl
    token: SecretStr
    email: str = Field(min_length=3, max_length=255)
    database: str = Field(min_length=1, max_length=128)
    draft_workflow: DraftWorkflow = DraftWorkflow.REVIEW

    @field_validator("domain")
    @classmethod
    def require_https(cls, value: AnyHttpUrl) -> AnyHttpUrl:
        if value.scheme != "https":
            raise ValueError("El dominio de Odoo debe usar HTTPS")
        return value

    @field_validator("email")
    @classmethod
    def require_email_shape(cls, value: str) -> str:
        if value.count("@") != 1 or value.startswith("@") or value.endswith("@"):
            raise ValueError("El correo no tiene un formato valido")
        return value

    @field_validator("token")
    @classmethod
    def require_token(cls, value: SecretStr) -> SecretStr:
        if not value.get_secret_value().strip():
            raise ValueError("El token es obligatorio")
        return value

    @field_validator("draft_workflow", mode="before")
    @classmethod
    def default_draft_workflow(cls, value: Any) -> Any:
        return value or DraftWorkflow.REVIEW

    def dotenv_content(self) -> str:
        values = {
            "ODOO_VERSION": self.odoo_version,
            "ODOO_URL": str(self.domain).rstrip("/"),
            "ODOO_DB": self.database,
            "ODOO_USERNAME": self.email,
            "ODOO_TOKEN": self.token.get_secret_value(),
            "ODOO_DRAFT_WORKFLOW": self.draft_workflow.value,
        }
        return "\n".join(
            f"{key}={json.dumps(value)}" for key, value in values.items()
        ) + "\n"


def save_dotenv(form: OdooConnectionForm, env_path: Path) -> None:
    """Escribe .env de forma atomica y limita sus permisos cuando es posible."""

    env_path = Path(env_path)
    env_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = env_path.with_name(f".{env_path.name}.tmp")
    temporary_path.write_text(form.dotenv_content(), encoding="utf-8", newline="\n")
    try:
        os.chmod(temporary_path, 0o600)
    except OSError:
        pass
    os.replace(temporary_path, env_path)


def render_config_page(values: Mapping[str, str] | None = None, *, message: str = "") -> str:
    values = values or {}

    def escaped(name: str) -> str:
        return html.escape(values.get(name, ""), quote=True)

    try:
        draft_workflow = DraftWorkflow(values.get("draft_workflow", "review"))
    except ValueError:
        draft_workflow = DraftWorkflow.REVIEW

    safe_message = html.escape(message, quote=True)
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Configuracion de Odoo AI Manager</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 42rem; margin: 3rem auto; padding: 0 1rem; }}
    label {{ display: block; margin-top: 1rem; font-weight: 600; }}
    input {{ box-sizing: border-box; margin-top: .35rem; padding: .65rem; width: 100%; }}
    input[type="radio"] {{ margin-right: .4rem; width: auto; }}
    button {{ margin-top: 1.5rem; padding: .7rem 1.2rem; }}
    .message {{ background: #e8f5e9; padding: .75rem; }}
  </style>
</head>
<body>
  <h1>Configuracion de Odoo</h1>
  <p>Los datos se guardaran en un archivo <code>.env</code> local.</p>
  {f'<p class="message">{safe_message}</p>' if safe_message else ''}
  <form method="post">
    <label>Version de Odoo
      <input name="odoo_version" required value="{escaped('odoo_version')}" placeholder="16.0">
    </label>
    <label>Dominio HTTPS de Odoo
      <input name="domain" type="url" required value="{escaped('domain')}" placeholder="https://odoo.example.com">
    </label>
    <label>Token o API key
      <input name="token" type="password" required autocomplete="new-password">
    </label>
    <label>Correo del usuario de Odoo
      <input name="email" type="email" required value="{escaped('email')}" placeholder="usuario@example.com">
    </label>
    <label>Base de datos
      <input name="database" required value="{escaped('database')}" placeholder="odoo">
    </label>
    <fieldset style="margin-top: 1rem;">
      <legend>Como trabajar con borradores (opcional)</legend>
      <p>Si no eliges una opcion, se usara revision previa.</p>
      <label style="font-weight: 400;">
        <input type="radio" name="draft_workflow" value="review"{" checked" if draft_workflow is DraftWorkflow.REVIEW else ""}>
        Crear borrador y pedir revision antes de guardarlo (modo seguro)
      </label>
      <label style="font-weight: 400;">
        <input type="radio" name="draft_workflow" value="direct"{" checked" if draft_workflow is DraftWorkflow.DIRECT else ""}>
        Crear borradores directamente (recomendado para usuarios avanzados)
      </label>
    </fieldset>
    <button type="submit">Guardar configuracion</button>
  </form>
</body>
</html>
"""


def _saved_form_values(env_path: Path) -> dict[str, str]:
    allowed_keys = {
        "ODOO_VERSION": "odoo_version",
        "ODOO_URL": "domain",
        "ODOO_USERNAME": "email",
        "ODOO_DB": "database",
        "ODOO_DRAFT_WORKFLOW": "draft_workflow",
    }
    values: dict[str, str] = {}
    if not env_path.exists():
        return values
    for line in env_path.read_text(encoding="utf-8").splitlines():
        key, separator, raw_value = line.partition("=")
        if separator and key in allowed_keys:
            try:
                value: Any = json.loads(raw_value)
            except json.JSONDecodeError:
                value = raw_value.strip().strip('"').strip("'")
            values[allowed_keys[key]] = str(value)
    return values


class ConfigurationRequestHandler(BaseHTTPRequestHandler):
    env_path = Path(".env")

    def do_GET(self) -> None:
        if self.path != "/":
            self._send_html(404, "<h1>Not found</h1>")
            return
        self._send_html(200, render_config_page(_saved_form_values(self.env_path)))

    def do_POST(self) -> None:
        if self.path != "/":
            self._send_html(404, "<h1>Not found</h1>")
            return
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            raw_body = self.rfile.read(content_length).decode("utf-8")
            values = {
                key: entries[0]
                for key, entries in parse_qs(raw_body, keep_blank_values=True).items()
            }
            form = OdooConnectionForm.model_validate(values)
            save_dotenv(form, self.env_path)
        except Exception:
            self._send_html(
                400,
                render_config_page(values if "values" in locals() else {}, message="Revisa los valores introducidos."),
            )
            return
        self._send_html(
            200,
            render_config_page(
                {
                    "odoo_version": form.odoo_version,
                    "domain": str(form.domain).rstrip("/"),
                    "email": form.email,
                    "database": form.database,
                    "draft_workflow": form.draft_workflow.value,
                },
                message="Configuracion guardada en .env. El token no se muestra.",
            ),
        )

    def log_message(self, format: str, *args: Any) -> None:
        return

    def _send_html(self, status: int, body: str) -> None:
        encoded_body = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded_body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(encoded_body)


def create_configuration_server(
    host: str = "127.0.0.1",
    port: int = 8765,
    env_path: Path = Path(".env"),
) -> ThreadingHTTPServer:
    class BoundConfigurationRequestHandler(ConfigurationRequestHandler):
        pass

    BoundConfigurationRequestHandler.env_path = Path(env_path).resolve()
    return ThreadingHTTPServer((host, port), BoundConfigurationRequestHandler)


def run_configuration_server(
    host: str = "127.0.0.1",
    port: int = 8765,
    env_path: Path = Path(".env"),
    *,
    open_browser: bool = True,
) -> None:
    server = create_configuration_server(host, port, env_path)
    address = f"http://{host}:{server.server_port}/"
    print(f"Configurador disponible en {address}")
    if host not in {"127.0.0.1", "localhost", "::1"}:
        print("ADVERTENCIA: el configurador esta expuesto fuera de localhost.")
    if open_browser:
        webbrowser.open(address)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Configurador detenido.")
    finally:
        server.server_close()
