from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.distribution_initialize_sync_response_200 import DistributionInitializeSyncResponse200
from typing import cast



def _get_kwargs(
    site_code: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Distribution/Initialize/{site_code}".format(site_code=site_code,),
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[DistributionInitializeSyncResponse200]:
    if response.status_code == 200:
        response_200 = DistributionInitializeSyncResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[DistributionInitializeSyncResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    site_code: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[DistributionInitializeSyncResponse200]:
    """ 
    Args:
        site_code (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DistributionInitializeSyncResponse200]
     """


    kwargs = _get_kwargs(
        site_code=site_code,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    site_code: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[DistributionInitializeSyncResponse200]:
    """ 
    Args:
        site_code (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DistributionInitializeSyncResponse200
     """


    return sync_detailed(
        site_code=site_code,
client=client,

    ).parsed

async def asyncio_detailed(
    site_code: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[DistributionInitializeSyncResponse200]:
    """ 
    Args:
        site_code (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DistributionInitializeSyncResponse200]
     """


    kwargs = _get_kwargs(
        site_code=site_code,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    site_code: str,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[DistributionInitializeSyncResponse200]:
    """ 
    Args:
        site_code (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DistributionInitializeSyncResponse200
     """


    return (await asyncio_detailed(
        site_code=site_code,
client=client,

    )).parsed
