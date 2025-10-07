from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.app_product_groups_response_200 import AppProductGroupsResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    include_filters: Union[Unset, bool] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["includeFilters"] = include_filters


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/App/ProductGroups",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[AppProductGroupsResponse200]:
    if response.status_code == 200:
        response_200 = AppProductGroupsResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[AppProductGroupsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    include_filters: Union[Unset, bool] = UNSET,

) -> Response[AppProductGroupsResponse200]:
    """ Retrieves all ProductGroups

    Args:
        include_filters (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AppProductGroupsResponse200]
     """


    kwargs = _get_kwargs(
        include_filters=include_filters,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    include_filters: Union[Unset, bool] = UNSET,

) -> Optional[AppProductGroupsResponse200]:
    """ Retrieves all ProductGroups

    Args:
        include_filters (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AppProductGroupsResponse200
     """


    return sync_detailed(
        client=client,
include_filters=include_filters,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    include_filters: Union[Unset, bool] = UNSET,

) -> Response[AppProductGroupsResponse200]:
    """ Retrieves all ProductGroups

    Args:
        include_filters (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AppProductGroupsResponse200]
     """


    kwargs = _get_kwargs(
        include_filters=include_filters,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    include_filters: Union[Unset, bool] = UNSET,

) -> Optional[AppProductGroupsResponse200]:
    """ Retrieves all ProductGroups

    Args:
        include_filters (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AppProductGroupsResponse200
     """


    return (await asyncio_detailed(
        client=client,
include_filters=include_filters,

    )).parsed
