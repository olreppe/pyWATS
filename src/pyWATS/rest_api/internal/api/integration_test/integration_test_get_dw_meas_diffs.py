from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.integration_test_get_dw_meas_diffs_response_200 import IntegrationTestGetDWMeasDiffsResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    pn: Union[Unset, str] = UNSET,
    pc: Union[Unset, int] = UNSET,
    period_length: Union[Unset, int] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["pn"] = pn

    params["pc"] = pc

    params["periodLength"] = period_length


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/IntegrationTest/DWMeasDiffs",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[IntegrationTestGetDWMeasDiffsResponse200]:
    if response.status_code == 200:
        response_200 = IntegrationTestGetDWMeasDiffsResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[IntegrationTestGetDWMeasDiffsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    pn: Union[Unset, str] = UNSET,
    pc: Union[Unset, int] = UNSET,
    period_length: Union[Unset, int] = UNSET,

) -> Response[IntegrationTestGetDWMeasDiffsResponse200]:
    """ 
    Args:
        pn (Union[Unset, str]):
        pc (Union[Unset, int]):
        period_length (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[IntegrationTestGetDWMeasDiffsResponse200]
     """


    kwargs = _get_kwargs(
        pn=pn,
pc=pc,
period_length=period_length,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    pn: Union[Unset, str] = UNSET,
    pc: Union[Unset, int] = UNSET,
    period_length: Union[Unset, int] = UNSET,

) -> Optional[IntegrationTestGetDWMeasDiffsResponse200]:
    """ 
    Args:
        pn (Union[Unset, str]):
        pc (Union[Unset, int]):
        period_length (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        IntegrationTestGetDWMeasDiffsResponse200
     """


    return sync_detailed(
        client=client,
pn=pn,
pc=pc,
period_length=period_length,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    pn: Union[Unset, str] = UNSET,
    pc: Union[Unset, int] = UNSET,
    period_length: Union[Unset, int] = UNSET,

) -> Response[IntegrationTestGetDWMeasDiffsResponse200]:
    """ 
    Args:
        pn (Union[Unset, str]):
        pc (Union[Unset, int]):
        period_length (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[IntegrationTestGetDWMeasDiffsResponse200]
     """


    kwargs = _get_kwargs(
        pn=pn,
pc=pc,
period_length=period_length,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    pn: Union[Unset, str] = UNSET,
    pc: Union[Unset, int] = UNSET,
    period_length: Union[Unset, int] = UNSET,

) -> Optional[IntegrationTestGetDWMeasDiffsResponse200]:
    """ 
    Args:
        pn (Union[Unset, str]):
        pc (Union[Unset, int]):
        period_length (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        IntegrationTestGetDWMeasDiffsResponse200
     """


    return (await asyncio_detailed(
        client=client,
pn=pn,
pc=pc,
period_length=period_length,

    )).parsed
