from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.distribution_get_entity_changes_with_data_response_200_item import DistributionGetEntityChangesWithDataResponse200Item
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    site_code: str,
    entity_type: str,
    *,
    max_count: Union[Unset, int] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["maxCount"] = max_count


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Distribution/Changes/Reserve/{site_code}/{entity_type}".format(site_code=site_code,entity_type=entity_type,),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[list['DistributionGetEntityChangesWithDataResponse200Item']]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            response_200_item = DistributionGetEntityChangesWithDataResponse200Item.from_dict(response_200_item_data)



            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[list['DistributionGetEntityChangesWithDataResponse200Item']]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    site_code: str,
    entity_type: str,
    *,
    client: Union[AuthenticatedClient, Client],
    max_count: Union[Unset, int] = UNSET,

) -> Response[list['DistributionGetEntityChangesWithDataResponse200Item']]:
    """ 
    Args:
        site_code (str):
        entity_type (str):
        max_count (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['DistributionGetEntityChangesWithDataResponse200Item']]
     """


    kwargs = _get_kwargs(
        site_code=site_code,
entity_type=entity_type,
max_count=max_count,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    site_code: str,
    entity_type: str,
    *,
    client: Union[AuthenticatedClient, Client],
    max_count: Union[Unset, int] = UNSET,

) -> Optional[list['DistributionGetEntityChangesWithDataResponse200Item']]:
    """ 
    Args:
        site_code (str):
        entity_type (str):
        max_count (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['DistributionGetEntityChangesWithDataResponse200Item']
     """


    return sync_detailed(
        site_code=site_code,
entity_type=entity_type,
client=client,
max_count=max_count,

    ).parsed

async def asyncio_detailed(
    site_code: str,
    entity_type: str,
    *,
    client: Union[AuthenticatedClient, Client],
    max_count: Union[Unset, int] = UNSET,

) -> Response[list['DistributionGetEntityChangesWithDataResponse200Item']]:
    """ 
    Args:
        site_code (str):
        entity_type (str):
        max_count (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['DistributionGetEntityChangesWithDataResponse200Item']]
     """


    kwargs = _get_kwargs(
        site_code=site_code,
entity_type=entity_type,
max_count=max_count,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    site_code: str,
    entity_type: str,
    *,
    client: Union[AuthenticatedClient, Client],
    max_count: Union[Unset, int] = UNSET,

) -> Optional[list['DistributionGetEntityChangesWithDataResponse200Item']]:
    """ 
    Args:
        site_code (str):
        entity_type (str):
        max_count (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['DistributionGetEntityChangesWithDataResponse200Item']
     """


    return (await asyncio_detailed(
        site_code=site_code,
entity_type=entity_type,
client=client,
max_count=max_count,

    )).parsed
