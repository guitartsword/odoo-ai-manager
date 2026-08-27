import pytest
from pydantic import ValidationError

from odoo_ai_manager.config import OdooSettings


def test_odoo_settings_rejects_insecure_urls() -> None:
    with pytest.raises(ValidationError):
        OdooSettings(
            url="http://odoo.example.com",
            database="odoo",
            username="integration@example.com",
            password="secret",
        )
