from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.production_free_reserved_serial_numbers_response_200 import ProductionFreeReservedSerialNumbersResponse200
from ...models.virinco_wats_web_dashboard_models_mes_production_serial_number_range import VirincoWATSWebDashboardModelsMesProductionSerialNumberRange
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange'],
        list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange'],
        list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange'],
    ],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/internal/Production/SerialNumbers/Free",
    }

    if isinstance(body, list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange']):
        _kwargs["json"] = []
        for body_item_data in body:
            body_item = body_item_data.to_dict()
            _kwargs["json"].append(body_item)




        headers["Content-Type"] = "application/json"
    if isinstance(body, list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange']):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange']):
        _kwargs["json"] = []
        for body_item_data in body:
            body_item = body_item_data.to_dict()
            _kwargs["json"].append(body_item)




        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ProductionFreeReservedSerialNumbersResponse200]:
    if response.status_code == 200:
        response_200 = ProductionFreeReservedSerialNumbersResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ProductionFreeReservedSerialNumbersResponse200]:
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
        list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange'],
        list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange'],
        list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange'],
    ],

) -> Response[ProductionFreeReservedSerialNumbersResponse200]:
    """ Free all serial numbers in each specified range. Does not affect taken serial numbers.

    Args:
        body (list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange']):
        body (list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange']):
        body (list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionFreeReservedSerialNumbersResponse200]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange'],
        list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange'],
        list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange'],
    ],

) -> Optional[ProductionFreeReservedSerialNumbersResponse200]:
    """ Free all serial numbers in each specified range. Does not affect taken serial numbers.

    Args:
        body (list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange']):
        body (list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange']):
        body (list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionFreeReservedSerialNumbersResponse200
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange'],
        list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange'],
        list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange'],
    ],

) -> Response[ProductionFreeReservedSerialNumbersResponse200]:
    """ Free all serial numbers in each specified range. Does not affect taken serial numbers.

    Args:
        body (list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange']):
        body (list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange']):
        body (list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionFreeReservedSerialNumbersResponse200]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange'],
        list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange'],
        list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange'],
    ],

) -> Optional[ProductionFreeReservedSerialNumbersResponse200]:
    """ Free all serial numbers in each specified range. Does not affect taken serial numbers.

    Args:
        body (list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange']):
        body (list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange']):
        body (list['VirincoWATSWebDashboardModelsMesProductionSerialNumberRange']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionFreeReservedSerialNumbersResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
