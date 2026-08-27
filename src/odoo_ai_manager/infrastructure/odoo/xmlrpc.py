from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any
from xmlrpc.client import Fault, ProtocolError, SafeTransport, ServerProxy
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from odoo_ai_manager.config import OdooSettings
from odoo_ai_manager.domain.models import AccessMode


class OdooAuthenticationError(RuntimeError):
    """Las credenciales no fueron aceptadas por Odoo."""


class OdooTimezoneError(RuntimeError):
    """El timezone guardado en el usuario de Odoo no es valido."""


class MutationNotAllowedError(PermissionError):
    """La operacion no cumple el control de mutaciones."""


class OdooClientError(RuntimeError):
    """Error normalizado de comunicacion con Odoo."""


class _TimeoutSafeTransport(SafeTransport):
    def __init__(self, timeout_seconds: int) -> None:
        super().__init__()
        self._timeout_seconds = timeout_seconds

    def make_connection(self, host: str) -> Any:
        connection = super().make_connection(host)
        connection.timeout = self._timeout_seconds
        return connection


class XmlRpcOdooClient:
    """Cliente generico para Odoo 16/17 y otras versiones legacy."""

    def __init__(
        self,
        settings: OdooSettings,
        *,
        access_mode: AccessMode = AccessMode.READ_ONLY,
        allowed_mutations: Sequence[tuple[str, str]] = (),
        common_proxy: Any | None = None,
        object_proxy: Any | None = None,
    ) -> None:
        self._settings = settings
        self.access_mode = AccessMode(access_mode)
        self._allowed_mutations = frozenset(allowed_mutations)
        base_url = str(settings.url).rstrip("/")
        transport = _TimeoutSafeTransport(settings.timeout_seconds)
        self._common_proxy = (
            common_proxy
            if common_proxy is not None
            else ServerProxy(
                f"{base_url}/xmlrpc/2/common",
                allow_none=True,
                transport=transport,
            )
        )
        self._object_proxy = (
            object_proxy
            if object_proxy is not None
            else ServerProxy(
                f"{base_url}/xmlrpc/2/object",
                allow_none=True,
                transport=transport,
            )
        )
        version = self._common_proxy.version()
        self.server_version = str(version.get("server_version", "unknown"))
        self.server_version_info = tuple(version.get("server_version_info", ()))
        self.user_id = self._common_proxy.authenticate(
            settings.database,
            settings.username,
            settings.password.get_secret_value(),
            {},
        )
        if not self.user_id:
            raise OdooAuthenticationError(
                "Odoo rechazo las credenciales proporcionadas."
            )
        self.company_id, self.company_name, self.user_timezone = (
            self._load_user_context()
        )

    def _load_user_context(self) -> tuple[int | None, str, ZoneInfo]:
        records = self._execute_kw(
            "res.users",
            "read",
            [[self.user_id]],
            {"fields": ["tz", "company_id"]},
        )
        user = records[0] if records else {}
        configured_company_id = self._settings.company_id
        user_company_id = _relation_id(user.get("company_id"))
        company_id = configured_company_id or user_company_id
        company_name = _relation_name(user.get("company_id"))
        timezone_name = user.get("tz")
        try:
            user_timezone = ZoneInfo(timezone_name or "UTC")
        except ZoneInfoNotFoundError as error:
            raise OdooTimezoneError(
                f"El timezone del usuario de Odoo no es valido: {timezone_name}"
            ) from error
        return company_id, company_name, user_timezone

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
        kwargs: dict[str, Any] = {
            "fields": list(fields),
            "offset": offset,
            "limit": limit,
        }
        if order is not None:
            kwargs["order"] = order
        if context is not None:
            kwargs["context"] = self._merge_context(context)
        elif self.company_id is not None:
            kwargs["context"] = self._merge_context({})
        return list(self._execute_kw(model, "search_read", [list(domain)], kwargs))

    def read(
        self,
        model: str,
        ids: Sequence[int],
        fields: Sequence[str],
        *,
        context: Mapping[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        kwargs: dict[str, Any] = {"fields": list(fields)}
        if context is not None:
            kwargs["context"] = self._merge_context(context)
        elif self.company_id is not None:
            kwargs["context"] = self._merge_context({})
        return list(self._execute_kw(model, "read", [list(ids)], kwargs))

    def fields_get(
        self,
        model: str,
        fields: Sequence[str] | None = None,
        *,
        context: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        args: list[Any] = [list(fields)] if fields is not None else []
        kwargs = {"context": self._merge_context(context)} if context is not None else {}
        return dict(self._execute_kw(model, "fields_get", args, kwargs))

    def execute_mutation(
        self,
        model: str,
        method: str,
        args: Sequence[Any] | None = None,
        kwargs: Mapping[str, Any] | None = None,
        *,
        confirmed: bool = False,
    ) -> Any:
        if self.access_mode is not AccessMode.MUTATION:
            raise MutationNotAllowedError(
                "El cliente esta en modo read_only; crea una conexion mutation."
            )
        if not confirmed:
            raise MutationNotAllowedError(
                "Una mutacion requiere confirmacion explicita."
            )
        if (model, method) not in self._allowed_mutations:
            raise MutationNotAllowedError(
                f"La mutacion {model}.{method} no esta aprobada por la skill."
            )
        mutation_kwargs = dict(kwargs or {})
        mutation_kwargs["context"] = self._merge_context(
            mutation_kwargs.get("context") or {}
        )
        return self._execute_kw(model, method, list(args or []), mutation_kwargs)

    def _merge_context(self, context: Mapping[str, Any]) -> dict[str, Any]:
        merged: dict[str, Any] = {}
        if self.company_id is not None:
            merged["allowed_company_ids"] = [self.company_id]
        merged.update(context)
        return merged

    def _execute_kw(
        self,
        model: str,
        method: str,
        args: Sequence[Any],
        kwargs: Mapping[str, Any],
    ) -> Any:
        try:
            return self._object_proxy.execute_kw(
                self._settings.database,
                self.user_id,
                self._settings.password.get_secret_value(),
                model,
                method,
                list(args),
                dict(kwargs),
            )
        except (Fault, ProtocolError, OSError) as error:
            raise OdooClientError(
                f"No fue posible ejecutar {model}.{method} en Odoo."
            ) from error


def _relation_id(value: Any) -> int | None:
    if isinstance(value, (list, tuple)):
        value = value[0] if value else None
    if value in (None, False, ""):
        return None
    return int(value)


def _relation_name(value: Any) -> str:
    if isinstance(value, (list, tuple)):
        return str(value[1]) if len(value) > 1 and value[1] else ""
    return ""
