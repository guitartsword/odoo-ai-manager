from pathlib import Path
from threading import Thread
from urllib.parse import urlencode
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
