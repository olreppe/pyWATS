from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.mes_get_translations_response_200 import MesGetTranslationsResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    culture_code: str,
    system_language: Union[Unset, bool] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["cultureCode"] = culture_code

    params["systemLanguage"] = system_language


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Mes/GetTranslations",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[MesGetTranslationsResponse200]:
    if response.status_code == 200:
        response_200 = MesGetTranslationsResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[MesGetTranslationsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    culture_code: str,
    system_language: Union[Unset, bool] = UNSET,

) -> Response[MesGetTranslationsResponse200]:
    """ 
    Args:
        culture_code (str):
        system_language (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MesGetTranslationsResponse200]
     """


    kwargs = _get_kwargs(
        culture_code=culture_code,
system_language=system_language,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    culture_code: str,
    system_language: Union[Unset, bool] = UNSET,

) -> Optional[MesGetTranslationsResponse200]:
    """ 
    Args:
        culture_code (str):
        system_language (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MesGetTranslationsResponse200
     """


    return sync_detailed(
        client=client,
culture_code=culture_code,
system_language=system_language,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    culture_code: str,
    system_language: Union[Unset, bool] = UNSET,

) -> Response[MesGetTranslationsResponse200]:
    """ 
    Args:
        culture_code (str):
        system_language (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MesGetTranslationsResponse200]
     """


    kwargs = _get_kwargs(
        culture_code=culture_code,
system_language=system_language,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    culture_code: str,
    system_language: Union[Unset, bool] = UNSET,

) -> Optional[MesGetTranslationsResponse200]:
    """ 
    Args:
        culture_code (str):
        system_language (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MesGetTranslationsResponse200
     """


    return (await asyncio_detailed(
        client=client,
culture_code=culture_code,
system_language=system_language,

    )).parsed
