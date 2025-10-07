from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.mes_update_translations_response_200 import MesUpdateTranslationsResponse200
from ...models.virinco_wats_web_dashboard_models_mes_translation_ext import VirincoWATSWebDashboardModelsMesTranslationExt
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    body: Union[
        list['VirincoWATSWebDashboardModelsMesTranslationExt'],
        list['VirincoWATSWebDashboardModelsMesTranslationExt'],
        list['VirincoWATSWebDashboardModelsMesTranslationExt'],
    ],
    system_language: Union[Unset, bool] = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["systemLanguage"] = system_language


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Mes/UpdateTranslations",
        "params": params,
    }

    if isinstance(body, list['VirincoWATSWebDashboardModelsMesTranslationExt']):
        _kwargs["json"] = []
        for body_item_data in body:
            body_item = body_item_data.to_dict()
            _kwargs["json"].append(body_item)




        headers["Content-Type"] = "application/json"
    if isinstance(body, list['VirincoWATSWebDashboardModelsMesTranslationExt']):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, list['VirincoWATSWebDashboardModelsMesTranslationExt']):
        _kwargs["json"] = []
        for body_item_data in body:
            body_item = body_item_data.to_dict()
            _kwargs["json"].append(body_item)




        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[MesUpdateTranslationsResponse200]:
    if response.status_code == 200:
        response_200 = MesUpdateTranslationsResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[MesUpdateTranslationsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list['VirincoWATSWebDashboardModelsMesTranslationExt'],
        list['VirincoWATSWebDashboardModelsMesTranslationExt'],
        list['VirincoWATSWebDashboardModelsMesTranslationExt'],
    ],
    system_language: Union[Unset, bool] = UNSET,

) -> Response[MesUpdateTranslationsResponse200]:
    """ 
    Args:
        system_language (Union[Unset, bool]):
        body (list['VirincoWATSWebDashboardModelsMesTranslationExt']):
        body (list['VirincoWATSWebDashboardModelsMesTranslationExt']):
        body (list['VirincoWATSWebDashboardModelsMesTranslationExt']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MesUpdateTranslationsResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
system_language=system_language,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list['VirincoWATSWebDashboardModelsMesTranslationExt'],
        list['VirincoWATSWebDashboardModelsMesTranslationExt'],
        list['VirincoWATSWebDashboardModelsMesTranslationExt'],
    ],
    system_language: Union[Unset, bool] = UNSET,

) -> Optional[MesUpdateTranslationsResponse200]:
    """ 
    Args:
        system_language (Union[Unset, bool]):
        body (list['VirincoWATSWebDashboardModelsMesTranslationExt']):
        body (list['VirincoWATSWebDashboardModelsMesTranslationExt']):
        body (list['VirincoWATSWebDashboardModelsMesTranslationExt']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MesUpdateTranslationsResponse200
     """


    return sync_detailed(
        client=client,
body=body,
system_language=system_language,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list['VirincoWATSWebDashboardModelsMesTranslationExt'],
        list['VirincoWATSWebDashboardModelsMesTranslationExt'],
        list['VirincoWATSWebDashboardModelsMesTranslationExt'],
    ],
    system_language: Union[Unset, bool] = UNSET,

) -> Response[MesUpdateTranslationsResponse200]:
    """ 
    Args:
        system_language (Union[Unset, bool]):
        body (list['VirincoWATSWebDashboardModelsMesTranslationExt']):
        body (list['VirincoWATSWebDashboardModelsMesTranslationExt']):
        body (list['VirincoWATSWebDashboardModelsMesTranslationExt']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MesUpdateTranslationsResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
system_language=system_language,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list['VirincoWATSWebDashboardModelsMesTranslationExt'],
        list['VirincoWATSWebDashboardModelsMesTranslationExt'],
        list['VirincoWATSWebDashboardModelsMesTranslationExt'],
    ],
    system_language: Union[Unset, bool] = UNSET,

) -> Optional[MesUpdateTranslationsResponse200]:
    """ 
    Args:
        system_language (Union[Unset, bool]):
        body (list['VirincoWATSWebDashboardModelsMesTranslationExt']):
        body (list['VirincoWATSWebDashboardModelsMesTranslationExt']):
        body (list['VirincoWATSWebDashboardModelsMesTranslationExt']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MesUpdateTranslationsResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
system_language=system_language,

    )).parsed
