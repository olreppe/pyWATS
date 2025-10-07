from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.trigger_put_trigger_actions_by_trigger_response_200 import TriggerPutTriggerActionsByTriggerResponse200
from ...models.virinco_wats_web_dashboard_models_tdm_trigger_action import VirincoWATSWebDashboardModelsTdmTriggerAction
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        list['VirincoWATSWebDashboardModelsTdmTriggerAction'],
        list['VirincoWATSWebDashboardModelsTdmTriggerAction'],
        list['VirincoWATSWebDashboardModelsTdmTriggerAction'],
    ],
    trigger_id: int,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["triggerId"] = trigger_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/internal/Trigger/PutTriggerActionsByTrigger",
        "params": params,
    }

    if isinstance(body, list['VirincoWATSWebDashboardModelsTdmTriggerAction']):
        _kwargs["json"] = []
        for body_item_data in body:
            body_item = body_item_data.to_dict()
            _kwargs["json"].append(body_item)




        headers["Content-Type"] = "application/json"
    if isinstance(body, list['VirincoWATSWebDashboardModelsTdmTriggerAction']):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, list['VirincoWATSWebDashboardModelsTdmTriggerAction']):
        _kwargs["json"] = []
        for body_item_data in body:
            body_item = body_item_data.to_dict()
            _kwargs["json"].append(body_item)




        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[TriggerPutTriggerActionsByTriggerResponse200]:
    if response.status_code == 200:
        response_200 = TriggerPutTriggerActionsByTriggerResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[TriggerPutTriggerActionsByTriggerResponse200]:
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
        list['VirincoWATSWebDashboardModelsTdmTriggerAction'],
        list['VirincoWATSWebDashboardModelsTdmTriggerAction'],
        list['VirincoWATSWebDashboardModelsTdmTriggerAction'],
    ],
    trigger_id: int,

) -> Response[TriggerPutTriggerActionsByTriggerResponse200]:
    """ Removes all trigger actions for a trigger, and replaces them with the actions provided.

    Args:
        trigger_id (int):
        body (list['VirincoWATSWebDashboardModelsTdmTriggerAction']):
        body (list['VirincoWATSWebDashboardModelsTdmTriggerAction']):
        body (list['VirincoWATSWebDashboardModelsTdmTriggerAction']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TriggerPutTriggerActionsByTriggerResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
trigger_id=trigger_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list['VirincoWATSWebDashboardModelsTdmTriggerAction'],
        list['VirincoWATSWebDashboardModelsTdmTriggerAction'],
        list['VirincoWATSWebDashboardModelsTdmTriggerAction'],
    ],
    trigger_id: int,

) -> Optional[TriggerPutTriggerActionsByTriggerResponse200]:
    """ Removes all trigger actions for a trigger, and replaces them with the actions provided.

    Args:
        trigger_id (int):
        body (list['VirincoWATSWebDashboardModelsTdmTriggerAction']):
        body (list['VirincoWATSWebDashboardModelsTdmTriggerAction']):
        body (list['VirincoWATSWebDashboardModelsTdmTriggerAction']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TriggerPutTriggerActionsByTriggerResponse200
     """


    return sync_detailed(
        client=client,
body=body,
trigger_id=trigger_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list['VirincoWATSWebDashboardModelsTdmTriggerAction'],
        list['VirincoWATSWebDashboardModelsTdmTriggerAction'],
        list['VirincoWATSWebDashboardModelsTdmTriggerAction'],
    ],
    trigger_id: int,

) -> Response[TriggerPutTriggerActionsByTriggerResponse200]:
    """ Removes all trigger actions for a trigger, and replaces them with the actions provided.

    Args:
        trigger_id (int):
        body (list['VirincoWATSWebDashboardModelsTdmTriggerAction']):
        body (list['VirincoWATSWebDashboardModelsTdmTriggerAction']):
        body (list['VirincoWATSWebDashboardModelsTdmTriggerAction']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TriggerPutTriggerActionsByTriggerResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
trigger_id=trigger_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list['VirincoWATSWebDashboardModelsTdmTriggerAction'],
        list['VirincoWATSWebDashboardModelsTdmTriggerAction'],
        list['VirincoWATSWebDashboardModelsTdmTriggerAction'],
    ],
    trigger_id: int,

) -> Optional[TriggerPutTriggerActionsByTriggerResponse200]:
    """ Removes all trigger actions for a trigger, and replaces them with the actions provided.

    Args:
        trigger_id (int):
        body (list['VirincoWATSWebDashboardModelsTdmTriggerAction']):
        body (list['VirincoWATSWebDashboardModelsTdmTriggerAction']):
        body (list['VirincoWATSWebDashboardModelsTdmTriggerAction']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TriggerPutTriggerActionsByTriggerResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
trigger_id=trigger_id,

    )).parsed
