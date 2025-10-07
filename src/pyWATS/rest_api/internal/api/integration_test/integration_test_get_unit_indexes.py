from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.integration_test_get_unit_indexes_response_200 import IntegrationTestGetUnitIndexesResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    sn: Union[Unset, str] = UNSET,
    pn: Union[Unset, str] = UNSET,
    pc: Union[Unset, int] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["sn"] = sn

    params["pn"] = pn

    params["pc"] = pc


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/IntegrationTest/UnitIndexes",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[IntegrationTestGetUnitIndexesResponse200]:
    if response.status_code == 200:
        response_200 = IntegrationTestGetUnitIndexesResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[IntegrationTestGetUnitIndexesResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    sn: Union[Unset, str] = UNSET,
    pn: Union[Unset, str] = UNSET,
    pc: Union[Unset, int] = UNSET,

) -> Response[IntegrationTestGetUnitIndexesResponse200]:
    """ 
    Args:
        sn (Union[Unset, str]):
        pn (Union[Unset, str]):
        pc (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[IntegrationTestGetUnitIndexesResponse200]
     """


    kwargs = _get_kwargs(
        sn=sn,
pn=pn,
pc=pc,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    sn: Union[Unset, str] = UNSET,
    pn: Union[Unset, str] = UNSET,
    pc: Union[Unset, int] = UNSET,

) -> Optional[IntegrationTestGetUnitIndexesResponse200]:
    """ 
    Args:
        sn (Union[Unset, str]):
        pn (Union[Unset, str]):
        pc (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        IntegrationTestGetUnitIndexesResponse200
     """


    return sync_detailed(
        client=client,
sn=sn,
pn=pn,
pc=pc,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    sn: Union[Unset, str] = UNSET,
    pn: Union[Unset, str] = UNSET,
    pc: Union[Unset, int] = UNSET,

) -> Response[IntegrationTestGetUnitIndexesResponse200]:
    """ 
    Args:
        sn (Union[Unset, str]):
        pn (Union[Unset, str]):
        pc (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[IntegrationTestGetUnitIndexesResponse200]
     """


    kwargs = _get_kwargs(
        sn=sn,
pn=pn,
pc=pc,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    sn: Union[Unset, str] = UNSET,
    pn: Union[Unset, str] = UNSET,
    pc: Union[Unset, int] = UNSET,

) -> Optional[IntegrationTestGetUnitIndexesResponse200]:
    """ 
    Args:
        sn (Union[Unset, str]):
        pn (Union[Unset, str]):
        pc (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        IntegrationTestGetUnitIndexesResponse200
     """


    return (await asyncio_detailed(
        client=client,
sn=sn,
pn=pn,
pc=pc,

    )).parsed
