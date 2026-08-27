from collections.abc import Mapping, Sequence
from datetime import date
from typing import Any, Protocol
from zoneinfo import ZoneInfo

from .models import AccessMode, MutationKind


class OdooReadClient(Protocol):
    access_mode: AccessMode
    user_id: int
    user_timezone: ZoneInfo
    server_version: str
    company_id: int | None
    company_name: str

    def search_read(
        self,
        model: str,
        domain: Sequence[Sequence[Any]],
        fields: Sequence[str],
        *,
        offset: int = 0,
        limit: int = 1000,
        order: str | None = None,
        context: Mapping[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Busca registros sin exponer el transporte subyacente."""

    def read(
        self,
        model: str,
        ids: Sequence[int],
        fields: Sequence[str],
        *,
        context: Mapping[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Lee registros por id."""


class OdooMutationClient(OdooReadClient, Protocol):
    def execute_mutation(
        self,
        model: str,
        method: str,
        args: Sequence[Any] | None = None,
        kwargs: Mapping[str, Any] | None = None,
        *,
        confirmed: bool = False,
        kind: MutationKind = MutationKind.DESTRUCTIVE,
    ) -> Any:
        """Ejecuta una mutacion segun su tipo y flujo configurado."""
