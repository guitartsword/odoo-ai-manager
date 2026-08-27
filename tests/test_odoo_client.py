from collections.abc import Mapping, Sequence
from typing import Any
from zoneinfo import ZoneInfo

import pytest

from odoo_ai_manager.config import OdooSettings
from odoo_ai_manager.domain.models import AccessMode, DraftWorkflow, MutationKind
from odoo_ai_manager.infrastructure.odoo.xmlrpc import (
    MutationNotAllowedError,
    XmlRpcOdooClient,
)


class FakeCommonProxy:
    def version(self) -> dict[str, Any]:
        return {
            "server_version": "16.0+e",
            "server_version_info": [16, 0, 0, "final", 0],
        }

    def authenticate(
        self,
        database: str,
        username: str,
        password: str,
        context: Mapping[str, Any],
    ) -> int:
        return 7


class FakeObjectProxy:
    def __init__(self) -> None:
        self.mutations: list[tuple] = []

    def execute_kw(
        self,
        database: str,
        uid: int,
        password: str,
        model: str,
        method: str,
        args: Sequence[Any],
        kwargs: Mapping[str, Any],
    ) -> Any:
        if model == "res.users" and method == "read":
            return [{"id": 7, "tz": "America/Mexico_City"}]
        self.mutations.append((model, method, args, kwargs))
        return True


def make_settings(
    draft_workflow: DraftWorkflow = DraftWorkflow.REVIEW,
) -> OdooSettings:
    return OdooSettings(
        url="https://odoo.example.com",
        database="odoo",
        username="integration@example.com",
        password="secret",
        draft_workflow=draft_workflow,
    )


def test_xmlrpc_client_reads_user_timezone_and_server_version() -> None:
    client = XmlRpcOdooClient(
        make_settings(),
        common_proxy=FakeCommonProxy(),
        object_proxy=FakeObjectProxy(),
    )

    assert client.user_id == 7
    assert client.server_version == "16.0+e"
    assert client.user_timezone == ZoneInfo("America/Mexico_City")


def test_xmlrpc_client_rejects_mutations_by_default() -> None:
    client = XmlRpcOdooClient(
        make_settings(),
        common_proxy=FakeCommonProxy(),
        object_proxy=FakeObjectProxy(),
    )

    with pytest.raises(MutationNotAllowedError):
        client.execute_mutation("product.product", "create", [{"name": "Test"}])


def test_mutation_client_requires_explicit_confirmation() -> None:
    object_proxy = FakeObjectProxy()
    client = XmlRpcOdooClient(
        make_settings(),
        access_mode=AccessMode.MUTATION,
        allowed_mutations={
            ("purchase.order", "create"): MutationKind.DRAFT,
        },
        common_proxy=FakeCommonProxy(),
        object_proxy=object_proxy,
    )

    with pytest.raises(MutationNotAllowedError):
        client.execute_mutation("purchase.order", "create", [{"partner_id": 12}])

    result = client.execute_mutation(
        "purchase.order",
        "create",
        [{"partner_id": 12}],
        confirmed=True,
        kind=MutationKind.DRAFT,
    )

    assert result is True
    assert object_proxy.mutations[-1][0:2] == ("purchase.order", "create")


def test_mutation_client_rejects_an_unapproved_destructive_operation() -> None:
    client = XmlRpcOdooClient(
        make_settings(),
        access_mode=AccessMode.MUTATION,
        allowed_mutations={
            ("stock.picking", "create"): MutationKind.DRAFT,
        },
        common_proxy=FakeCommonProxy(),
        object_proxy=FakeObjectProxy(),
    )

    with pytest.raises(MutationNotAllowedError):
        client.execute_mutation(
            "stock.picking",
            "button_validate",
            [[1]],
            confirmed=True,
            kind=MutationKind.DESTRUCTIVE,
        )


def test_direct_draft_workflow_skips_per_action_confirmation() -> None:
    object_proxy = FakeObjectProxy()
    client = XmlRpcOdooClient(
        make_settings(DraftWorkflow.DIRECT),
        access_mode=AccessMode.MUTATION,
        allowed_mutations={
            ("purchase.order", "create"): MutationKind.DRAFT,
        },
        common_proxy=FakeCommonProxy(),
        object_proxy=object_proxy,
    )

    result = client.execute_mutation(
        "purchase.order",
        "create",
        [{"partner_id": 12}],
        kind=MutationKind.DRAFT,
    )

    assert result is True
    assert object_proxy.mutations[-1][0:2] == ("purchase.order", "create")


def test_direct_draft_workflow_does_not_bypass_destructive_confirmation() -> None:
    client = XmlRpcOdooClient(
        make_settings(DraftWorkflow.DIRECT),
        access_mode=AccessMode.MUTATION,
        allowed_mutations={
            ("stock.picking", "button_validate"): MutationKind.DESTRUCTIVE,
        },
        common_proxy=FakeCommonProxy(),
        object_proxy=FakeObjectProxy(),
    )

    with pytest.raises(MutationNotAllowedError):
        client.execute_mutation(
            "stock.picking",
            "button_validate",
            [[1]],
            kind=MutationKind.DESTRUCTIVE,
        )
