from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.transfer_create_rule_response_200 import TransferCreateRuleResponse200
from ...models.virinco_wats_web_dashboard_models_tdm_transfer_share_rule import VirincoWATSWebDashboardModelsTdmTransferShareRule
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    body: Union[
        VirincoWATSWebDashboardModelsTdmTransferShareRule,
        VirincoWATSWebDashboardModelsTdmTransferShareRule,
        VirincoWATSWebDashboardModelsTdmTransferShareRule,
    ],
    rule_type: Union[Unset, int] = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["ruleType"] = rule_type


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Transfer/Share/Rule",
        "params": params,
    }

    if isinstance(body, VirincoWATSWebDashboardModelsTdmTransferShareRule):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, VirincoWATSWebDashboardModelsTdmTransferShareRule):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, VirincoWATSWebDashboardModelsTdmTransferShareRule):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[TransferCreateRuleResponse200]:
    if response.status_code == 200:
        response_200 = TransferCreateRuleResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[TransferCreateRuleResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsTdmTransferShareRule,
        VirincoWATSWebDashboardModelsTdmTransferShareRule,
        VirincoWATSWebDashboardModelsTdmTransferShareRule,
    ],
    rule_type: Union[Unset, int] = UNSET,

) -> Response[TransferCreateRuleResponse200]:
    """ 
    Args:
        rule_type (Union[Unset, int]):
        body (VirincoWATSWebDashboardModelsTdmTransferShareRule):
        body (VirincoWATSWebDashboardModelsTdmTransferShareRule):
        body (VirincoWATSWebDashboardModelsTdmTransferShareRule):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TransferCreateRuleResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
rule_type=rule_type,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsTdmTransferShareRule,
        VirincoWATSWebDashboardModelsTdmTransferShareRule,
        VirincoWATSWebDashboardModelsTdmTransferShareRule,
    ],
    rule_type: Union[Unset, int] = UNSET,

) -> Optional[TransferCreateRuleResponse200]:
    """ 
    Args:
        rule_type (Union[Unset, int]):
        body (VirincoWATSWebDashboardModelsTdmTransferShareRule):
        body (VirincoWATSWebDashboardModelsTdmTransferShareRule):
        body (VirincoWATSWebDashboardModelsTdmTransferShareRule):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TransferCreateRuleResponse200
     """


    return sync_detailed(
        client=client,
body=body,
rule_type=rule_type,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsTdmTransferShareRule,
        VirincoWATSWebDashboardModelsTdmTransferShareRule,
        VirincoWATSWebDashboardModelsTdmTransferShareRule,
    ],
    rule_type: Union[Unset, int] = UNSET,

) -> Response[TransferCreateRuleResponse200]:
    """ 
    Args:
        rule_type (Union[Unset, int]):
        body (VirincoWATSWebDashboardModelsTdmTransferShareRule):
        body (VirincoWATSWebDashboardModelsTdmTransferShareRule):
        body (VirincoWATSWebDashboardModelsTdmTransferShareRule):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TransferCreateRuleResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
rule_type=rule_type,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsTdmTransferShareRule,
        VirincoWATSWebDashboardModelsTdmTransferShareRule,
        VirincoWATSWebDashboardModelsTdmTransferShareRule,
    ],
    rule_type: Union[Unset, int] = UNSET,

) -> Optional[TransferCreateRuleResponse200]:
    """ 
    Args:
        rule_type (Union[Unset, int]):
        body (VirincoWATSWebDashboardModelsTdmTransferShareRule):
        body (VirincoWATSWebDashboardModelsTdmTransferShareRule):
        body (VirincoWATSWebDashboardModelsTdmTransferShareRule):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TransferCreateRuleResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
rule_type=rule_type,

    )).parsed
