from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.trigger_get_trigger_fields_by_trigger_response_200 import TriggerGetTriggerFieldsByTriggerResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    trigger_id: int,
    type_: Union[Unset, int] = UNSET,
    category: Union[Unset, str] = UNSET,
    include_action_category: Union[Unset, bool] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["triggerId"] = trigger_id

    params["type"] = type_

    params["category"] = category

    params["includeActionCategory"] = include_action_category


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Trigger/GetTriggerFieldsByTrigger",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[TriggerGetTriggerFieldsByTriggerResponse200]:
    if response.status_code == 200:
        response_200 = TriggerGetTriggerFieldsByTriggerResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[TriggerGetTriggerFieldsByTriggerResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    trigger_id: int,
    type_: Union[Unset, int] = UNSET,
    category: Union[Unset, str] = UNSET,
    include_action_category: Union[Unset, bool] = UNSET,

) -> Response[TriggerGetTriggerFieldsByTriggerResponse200]:
    """ Retrieves all trigger fields for a specific trigger

    Args:
        trigger_id (int):
        type_ (Union[Unset, int]):
        category (Union[Unset, str]):
        include_action_category (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TriggerGetTriggerFieldsByTriggerResponse200]
     """


    kwargs = _get_kwargs(
        trigger_id=trigger_id,
type_=type_,
category=category,
include_action_category=include_action_category,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    trigger_id: int,
    type_: Union[Unset, int] = UNSET,
    category: Union[Unset, str] = UNSET,
    include_action_category: Union[Unset, bool] = UNSET,

) -> Optional[TriggerGetTriggerFieldsByTriggerResponse200]:
    """ Retrieves all trigger fields for a specific trigger

    Args:
        trigger_id (int):
        type_ (Union[Unset, int]):
        category (Union[Unset, str]):
        include_action_category (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TriggerGetTriggerFieldsByTriggerResponse200
     """


    return sync_detailed(
        client=client,
trigger_id=trigger_id,
type_=type_,
category=category,
include_action_category=include_action_category,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    trigger_id: int,
    type_: Union[Unset, int] = UNSET,
    category: Union[Unset, str] = UNSET,
    include_action_category: Union[Unset, bool] = UNSET,

) -> Response[TriggerGetTriggerFieldsByTriggerResponse200]:
    """ Retrieves all trigger fields for a specific trigger

    Args:
        trigger_id (int):
        type_ (Union[Unset, int]):
        category (Union[Unset, str]):
        include_action_category (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TriggerGetTriggerFieldsByTriggerResponse200]
     """


    kwargs = _get_kwargs(
        trigger_id=trigger_id,
type_=type_,
category=category,
include_action_category=include_action_category,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    trigger_id: int,
    type_: Union[Unset, int] = UNSET,
    category: Union[Unset, str] = UNSET,
    include_action_category: Union[Unset, bool] = UNSET,

) -> Optional[TriggerGetTriggerFieldsByTriggerResponse200]:
    """ Retrieves all trigger fields for a specific trigger

    Args:
        trigger_id (int):
        type_ (Union[Unset, int]):
        category (Union[Unset, str]):
        include_action_category (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TriggerGetTriggerFieldsByTriggerResponse200
     """


    return (await asyncio_detailed(
        client=client,
trigger_id=trigger_id,
type_=type_,
category=category,
include_action_category=include_action_category,

    )).parsed
