from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.report_get_from_storage_response_200 import ReportGetFromStorageResponse200
from typing import cast
from uuid import UUID



def _get_kwargs(
    *,
    uuid: UUID,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_uuid = str(uuid)
    params["uuid"] = json_uuid


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Report/GetFromStorage",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ReportGetFromStorageResponse200]:
    if response.status_code == 200:
        response_200 = ReportGetFromStorageResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ReportGetFromStorageResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    uuid: UUID,

) -> Response[ReportGetFromStorageResponse200]:
    """ 
    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ReportGetFromStorageResponse200]
     """


    kwargs = _get_kwargs(
        uuid=uuid,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    uuid: UUID,

) -> Optional[ReportGetFromStorageResponse200]:
    """ 
    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ReportGetFromStorageResponse200
     """


    return sync_detailed(
        client=client,
uuid=uuid,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    uuid: UUID,

) -> Response[ReportGetFromStorageResponse200]:
    """ 
    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ReportGetFromStorageResponse200]
     """


    kwargs = _get_kwargs(
        uuid=uuid,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    uuid: UUID,

) -> Optional[ReportGetFromStorageResponse200]:
    """ 
    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ReportGetFromStorageResponse200
     """


    return (await asyncio_detailed(
        client=client,
uuid=uuid,

    )).parsed
