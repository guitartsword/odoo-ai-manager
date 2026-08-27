from pydantic import AliasChoices, AnyHttpUrl, Field, SecretStr, field_validator
from pydantic.types import PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict

from odoo_ai_manager.domain.models import DraftWorkflow


class OdooSettings(BaseSettings):
    """Configuracion de conexion. Nunca se imprime la credencial."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    url: AnyHttpUrl = Field(validation_alias="ODOO_URL")
    database: str = Field(
        validation_alias=AliasChoices("ODOO_DB", "ODOO_DATABASE")
    )
    username: str = Field(
        validation_alias=AliasChoices("ODOO_USERNAME", "ODOO_USER")
    )
    version: str | None = Field(
        default=None,
        validation_alias="ODOO_VERSION",
    )
    password: SecretStr = Field(
        validation_alias=AliasChoices("ODOO_TOKEN", "ODOO_PASSWORD")
    )
    company_id: int | None = Field(
        default=None,
        validation_alias=AliasChoices("ODOO_COMPANY_ID", "ODOO_COMPANY"),
    )
    timeout_seconds: PositiveInt = Field(
        default=30,
        validation_alias="ODOO_TIMEOUT_SECONDS",
    )
    draft_workflow: DraftWorkflow = Field(
        default=DraftWorkflow.REVIEW,
        validation_alias="ODOO_DRAFT_WORKFLOW",
    )

    @field_validator("url")
    @classmethod
    def require_https(cls, value: AnyHttpUrl) -> AnyHttpUrl:
        if value.scheme != "https":
            raise ValueError("ODOO_URL debe usar HTTPS")
        if value.username or value.password:
            raise ValueError("ODOO_URL no debe contener usuario ni contrasena")
        return value
