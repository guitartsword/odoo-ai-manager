from pathlib import Path
from threading import Thread
from urllib.parse import urlencode
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from odoo_ai_manager.config import OdooSettings
from odoo_ai_manager.configuration import (
    OdooConnectionForm,
    create_configuration_server,
    render_config_page,
    save_dotenv,
)
from odoo_ai_manager.domain.models import DraftWorkflow


def make_form(
    draft_workflow: DraftWorkflow = DraftWorkflow.REVIEW,
) -> OdooConnectionForm:
    return OdooConnectionForm(
        odoo_version="16.0",
        domain="https://odoo.example.com",
        token="secret-token",
        email="integration@example.com",
        database="odoo",
        draft_workflow=draft_workflow,
    )


def test_configuration_form_saves_connection_to_dotenv(tmp_path: Path) -> None:
    env_path = tmp_path / ".env"

    save_dotenv(make_form(), env_path)

    settings = OdooSettings(_env_file=env_path)
    assert settings.version == "16.0"
    assert str(settings.url) == "https://odoo.example.com/"
    assert settings.database == "odoo"
    assert settings.username == "integration@example.com"
    assert settings.password.get_secret_value() == "secret-token"
    assert settings.draft_workflow is DraftWorkflow.REVIEW


def test_configuration_page_never_prefills_or_exposes_token() -> None:
    page = render_config_page(
        {
            "odoo_version": "16.0",
            "domain": "https://odoo.example.com",
            "email": "integration@example.com",
            "database": "odoo",
        }
    )

    assert 'name="token"' in page
    assert 'value="secret-token"' not in page
    assert "secret-token" not in page
    assert 'value="review" checked' in page


def test_configuration_page_renders_errors_as_actionable_red_feedback() -> None:
    page = render_config_page(
        {"odoo_version": "16.0"},
        errors=["Dominio HTTPS de Odoo: usa una URL HTTPS valida."],
    )

    assert 'class="message error"' in page
    assert 'class="message success"' not in page
    assert "Revisa estos datos:" in page
    assert "Dominio HTTPS de Odoo" in page


def test_configuration_form_can_record_direct_draft_workflow() -> None:
    form = make_form(DraftWorkflow.DIRECT)

    assert "ODOO_DRAFT_WORKFLOW=\"direct\"" in form.dotenv_content()


def test_configuration_server_saves_form_submission(tmp_path: Path) -> None:
    env_path = tmp_path / ".env"
    server = create_configuration_server(port=0, env_path=env_path)
    thread = Thread(target=server.serve_forever)
    thread.start()
    url = f"http://127.0.0.1:{server.server_port}/"
    try:
        with urlopen(url) as response:
            assert response.status == 200

        invalid_request = Request(
            url,
            data=urlencode(
                {
                    "odoo_version": "",
                    "domain": "http://odoo.example.com",
                    "token": "",
                    "email": "not-an-email",
                    "database": "",
                }
            ).encode(),
            method="POST",
        )
        try:
            urlopen(invalid_request)
        except HTTPError as error:
            invalid_body = error.read().decode()
            assert error.code == 400
        else:
            raise AssertionError("El formulario invalido debio responder 400")

        assert 'class="message error"' in invalid_body
        assert 'class="message success"' not in invalid_body
        assert "Version de Odoo" in invalid_body
        assert "Dominio HTTPS de Odoo" in invalid_body
        assert "Token o API key" in invalid_body
        assert "Correo del usuario de Odoo" in invalid_body
        assert "Base de datos" in invalid_body

        request = Request(
            url,
            data=urlencode(
                {
                    "odoo_version": "16.0",
                    "domain": "https://odoo.example.com",
                    "token": "secret-token",
                    "email": "integration@example.com",
                    "database": "odoo",
                    "draft_workflow": "direct",
                }
            ).encode(),
            method="POST",
        )
        with urlopen(request) as response:
            body = response.read().decode()
            assert response.status == 200
            assert "Configuracion guardada" in body
            assert "secret-token" not in body

        settings = OdooSettings(_env_file=env_path)
        assert settings.draft_workflow is DraftWorkflow.DIRECT
    finally:
        server.shutdown()
        thread.join()
        server.server_close()
