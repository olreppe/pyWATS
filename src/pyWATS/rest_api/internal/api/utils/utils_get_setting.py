from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.utils_get_setting_response_200 import UtilsGetSettingResponse200
from typing import cast



def _get_kwargs(
    *,
    key: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["key"] = key


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Utils/GetSetting",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[UtilsGetSettingResponse200]:
    if response.status_code == 200:
        response_200 = UtilsGetSettingResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[UtilsGetSettingResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    key: str,

) -> Response[UtilsGetSettingResponse200]:
    """ Returns the setting value for the specified key in [cfg].[Settings]

    Args:
        key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UtilsGetSettingResponse200]
     """


    kwargs = _get_kwargs(
        key=key,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    key: str,

) -> Optional[UtilsGetSettingResponse200]:
    """ Returns the setting value for the specified key in [cfg].[Settings]

    Args:
        key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UtilsGetSettingResponse200
     """


    return sync_detailed(
        client=client,
key=key,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    key: str,

) -> Response[UtilsGetSettingResponse200]:
    """ Returns the setting value for the specified key in [cfg].[Settings]

    Args:
        key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UtilsGetSettingResponse200]
     """


    kwargs = _get_kwargs(
        key=key,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    key: str,

) -> Optional[UtilsGetSettingResponse200]:
    """ Returns the setting value for the specified key in [cfg].[Settings]

    Args:
        key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UtilsGetSettingResponse200
     """


    return (await asyncio_detailed(
        client=client,
key=key,

    )).parsed
