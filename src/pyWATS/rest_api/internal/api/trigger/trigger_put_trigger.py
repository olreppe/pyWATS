from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.trigger_put_trigger_response_200 import TriggerPutTriggerResponse200
from ...models.virinco_wats_web_dashboard_models_tdm_trigger import VirincoWATSWebDashboardModelsTdmTrigger
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        VirincoWATSWebDashboardModelsTdmTrigger,
        VirincoWATSWebDashboardModelsTdmTrigger,
        VirincoWATSWebDashboardModelsTdmTrigger,
    ],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/internal/Trigger/PutTrigger",
    }

    if isinstance(body, VirincoWATSWebDashboardModelsTdmTrigger):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, VirincoWATSWebDashboardModelsTdmTrigger):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, VirincoWATSWebDashboardModelsTdmTrigger):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[TriggerPutTriggerResponse200]:
    if response.status_code == 200:
        response_200 = TriggerPutTriggerResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[TriggerPutTriggerResponse200]:
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
        VirincoWATSWebDashboardModelsTdmTrigger,
        VirincoWATSWebDashboardModelsTdmTrigger,
        VirincoWATSWebDashboardModelsTdmTrigger,
    ],

) -> Response[TriggerPutTriggerResponse200]:
    """ Updates a trigger. If the trigger does not exist, it is inserted (upsert)

    Args:
        body (VirincoWATSWebDashboardModelsTdmTrigger):
        body (VirincoWATSWebDashboardModelsTdmTrigger):
        body (VirincoWATSWebDashboardModelsTdmTrigger):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TriggerPutTriggerResponse200]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsTdmTrigger,
        VirincoWATSWebDashboardModelsTdmTrigger,
        VirincoWATSWebDashboardModelsTdmTrigger,
    ],

) -> Optional[TriggerPutTriggerResponse200]:
    """ Updates a trigger. If the trigger does not exist, it is inserted (upsert)

    Args:
        body (VirincoWATSWebDashboardModelsTdmTrigger):
        body (VirincoWATSWebDashboardModelsTdmTrigger):
        body (VirincoWATSWebDashboardModelsTdmTrigger):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TriggerPutTriggerResponse200
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsTdmTrigger,
        VirincoWATSWebDashboardModelsTdmTrigger,
        VirincoWATSWebDashboardModelsTdmTrigger,
    ],

) -> Response[TriggerPutTriggerResponse200]:
    """ Updates a trigger. If the trigger does not exist, it is inserted (upsert)

    Args:
        body (VirincoWATSWebDashboardModelsTdmTrigger):
        body (VirincoWATSWebDashboardModelsTdmTrigger):
        body (VirincoWATSWebDashboardModelsTdmTrigger):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TriggerPutTriggerResponse200]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsTdmTrigger,
        VirincoWATSWebDashboardModelsTdmTrigger,
        VirincoWATSWebDashboardModelsTdmTrigger,
    ],

) -> Optional[TriggerPutTriggerResponse200]:
    """ Updates a trigger. If the trigger does not exist, it is inserted (upsert)

    Args:
        body (VirincoWATSWebDashboardModelsTdmTrigger):
        body (VirincoWATSWebDashboardModelsTdmTrigger):
        body (VirincoWATSWebDashboardModelsTdmTrigger):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TriggerPutTriggerResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
