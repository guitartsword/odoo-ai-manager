from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class AccessMode(StrEnum):
    READ_ONLY = "read_only"
    MUTATION = "mutation"


class SkillManifest(BaseModel):
    """Metadatos que permiten a un agente descubrir una skill de forma segura."""

    model_config = ConfigDict(extra="ignore")

    id: str
    module: str
    name: str
    description: str
    access: AccessMode
    entrypoint: str | None = None
