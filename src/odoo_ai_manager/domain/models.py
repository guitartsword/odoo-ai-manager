from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, model_validator


class AccessMode(StrEnum):
    READ_ONLY = "read_only"
    MUTATION = "mutation"


class MutationKind(StrEnum):
    DRAFT = "draft"
    DESTRUCTIVE = "destructive"


class DraftWorkflow(StrEnum):
    REVIEW = "review"
    DIRECT = "direct"


class SkillStatus(StrEnum):
    AVAILABLE = "available"
    PLANNED = "planned"


class SkillManifest(BaseModel):
    """Metadatos que permiten a un agente descubrir una skill de forma segura."""

    model_config = ConfigDict(extra="ignore")

    id: str
    module: str
    name: str
    description: str
    access: AccessMode
    entrypoint: str | None = None
    status: SkillStatus = SkillStatus.AVAILABLE
    mutation_kind: MutationKind | None = None

    @model_validator(mode="after")
    def validate_access_policy(self) -> Self:
        if self.access is AccessMode.READ_ONLY and self.mutation_kind is not None:
            raise ValueError("Una skill read_only no puede declarar mutation_kind")
        if self.access is AccessMode.MUTATION and self.mutation_kind is None:
            raise ValueError("Una skill mutation debe declarar mutation_kind")
        return self
