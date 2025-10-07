from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.asset_post_asset_message_response_200 import AssetPostAssetMessageResponse200
from ...models.virinco_wats_web_dashboard_models_mes_asset_asset_message import VirincoWATSWebDashboardModelsMesAssetAssetMessage
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    body: Union[
        VirincoWATSWebDashboardModelsMesAssetAssetMessage,
        VirincoWATSWebDashboardModelsMesAssetAssetMessage,
        VirincoWATSWebDashboardModelsMesAssetAssetMessage,
    ],
    id: Union[Unset, str] = UNSET,
    serial_number: Union[Unset, str] = UNSET,
    culture_code: Union[Unset, str] = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["id"] = id

    params["serialNumber"] = serial_number

    params["cultureCode"] = culture_code


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/Asset/Message",
        "params": params,
    }

    if isinstance(body, VirincoWATSWebDashboardModelsMesAssetAssetMessage):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, VirincoWATSWebDashboardModelsMesAssetAssetMessage):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, VirincoWATSWebDashboardModelsMesAssetAssetMessage):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[AssetPostAssetMessageResponse200]:
    if response.status_code == 200:
        response_200 = AssetPostAssetMessageResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[AssetPostAssetMessageResponse200]:
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
        VirincoWATSWebDashboardModelsMesAssetAssetMessage,
        VirincoWATSWebDashboardModelsMesAssetAssetMessage,
        VirincoWATSWebDashboardModelsMesAssetAssetMessage,
    ],
    id: Union[Unset, str] = UNSET,
    serial_number: Union[Unset, str] = UNSET,
    culture_code: Union[Unset, str] = UNSET,

) -> Response[AssetPostAssetMessageResponse200]:
    """ Post a message/comment to the asset log.

    Args:
        id (Union[Unset, str]):
        serial_number (Union[Unset, str]):
        culture_code (Union[Unset, str]):
        body (VirincoWATSWebDashboardModelsMesAssetAssetMessage):
        body (VirincoWATSWebDashboardModelsMesAssetAssetMessage):
        body (VirincoWATSWebDashboardModelsMesAssetAssetMessage):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetPostAssetMessageResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
id=id,
serial_number=serial_number,
culture_code=culture_code,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsMesAssetAssetMessage,
        VirincoWATSWebDashboardModelsMesAssetAssetMessage,
        VirincoWATSWebDashboardModelsMesAssetAssetMessage,
    ],
    id: Union[Unset, str] = UNSET,
    serial_number: Union[Unset, str] = UNSET,
    culture_code: Union[Unset, str] = UNSET,

) -> Optional[AssetPostAssetMessageResponse200]:
    """ Post a message/comment to the asset log.

    Args:
        id (Union[Unset, str]):
        serial_number (Union[Unset, str]):
        culture_code (Union[Unset, str]):
        body (VirincoWATSWebDashboardModelsMesAssetAssetMessage):
        body (VirincoWATSWebDashboardModelsMesAssetAssetMessage):
        body (VirincoWATSWebDashboardModelsMesAssetAssetMessage):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetPostAssetMessageResponse200
     """


    return sync_detailed(
        client=client,
body=body,
id=id,
serial_number=serial_number,
culture_code=culture_code,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsMesAssetAssetMessage,
        VirincoWATSWebDashboardModelsMesAssetAssetMessage,
        VirincoWATSWebDashboardModelsMesAssetAssetMessage,
    ],
    id: Union[Unset, str] = UNSET,
    serial_number: Union[Unset, str] = UNSET,
    culture_code: Union[Unset, str] = UNSET,

) -> Response[AssetPostAssetMessageResponse200]:
    """ Post a message/comment to the asset log.

    Args:
        id (Union[Unset, str]):
        serial_number (Union[Unset, str]):
        culture_code (Union[Unset, str]):
        body (VirincoWATSWebDashboardModelsMesAssetAssetMessage):
        body (VirincoWATSWebDashboardModelsMesAssetAssetMessage):
        body (VirincoWATSWebDashboardModelsMesAssetAssetMessage):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AssetPostAssetMessageResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
id=id,
serial_number=serial_number,
culture_code=culture_code,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsMesAssetAssetMessage,
        VirincoWATSWebDashboardModelsMesAssetAssetMessage,
        VirincoWATSWebDashboardModelsMesAssetAssetMessage,
    ],
    id: Union[Unset, str] = UNSET,
    serial_number: Union[Unset, str] = UNSET,
    culture_code: Union[Unset, str] = UNSET,

) -> Optional[AssetPostAssetMessageResponse200]:
    """ Post a message/comment to the asset log.

    Args:
        id (Union[Unset, str]):
        serial_number (Union[Unset, str]):
        culture_code (Union[Unset, str]):
        body (VirincoWATSWebDashboardModelsMesAssetAssetMessage):
        body (VirincoWATSWebDashboardModelsMesAssetAssetMessage):
        body (VirincoWATSWebDashboardModelsMesAssetAssetMessage):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AssetPostAssetMessageResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
id=id,
serial_number=serial_number,
culture_code=culture_code,

    )).parsed
