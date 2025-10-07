from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.software_log_response_200 import SoftwareLogResponse200
from typing import cast
from uuid import UUID



def _get_kwargs(
    *,
    package_id: UUID,
    download_size: int,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_package_id = str(package_id)
    params["packageId"] = json_package_id

    params["downloadSize"] = download_size


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Software/Log",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[SoftwareLogResponse200]:
    if response.status_code == 200:
        response_200 = SoftwareLogResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[SoftwareLogResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    package_id: UUID,
    download_size: int,

) -> Response[SoftwareLogResponse200]:
    """ Package download history.
    Store information about downloaded packages, size, date

    Args:
        package_id (UUID):
        download_size (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SoftwareLogResponse200]
     """


    kwargs = _get_kwargs(
        package_id=package_id,
download_size=download_size,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    package_id: UUID,
    download_size: int,

) -> Optional[SoftwareLogResponse200]:
    """ Package download history.
    Store information about downloaded packages, size, date

    Args:
        package_id (UUID):
        download_size (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SoftwareLogResponse200
     """


    return sync_detailed(
        client=client,
package_id=package_id,
download_size=download_size,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    package_id: UUID,
    download_size: int,

) -> Response[SoftwareLogResponse200]:
    """ Package download history.
    Store information about downloaded packages, size, date

    Args:
        package_id (UUID):
        download_size (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SoftwareLogResponse200]
     """


    kwargs = _get_kwargs(
        package_id=package_id,
download_size=download_size,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    package_id: UUID,
    download_size: int,

) -> Optional[SoftwareLogResponse200]:
    """ Package download history.
    Store information about downloaded packages, size, date

    Args:
        package_id (UUID):
        download_size (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SoftwareLogResponse200
     """


    return (await asyncio_detailed(
        client=client,
package_id=package_id,
download_size=download_size,

    )).parsed
