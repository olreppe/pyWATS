from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.production_put_batches_response_200 import ProductionPutBatchesResponse200
from ...models.virinco_wats_web_dashboard_models_mes_production_public_production_batch import VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch'],
        list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch'],
        list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch'],
    ],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/Production/Batches",
    }

    if isinstance(body, list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch']):
        _kwargs["json"] = []
        for body_item_data in body:
            body_item = body_item_data.to_dict()
            _kwargs["json"].append(body_item)




        headers["Content-Type"] = "application/json"
    if isinstance(body, list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch']):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch']):
        _kwargs["json"] = []
        for body_item_data in body:
            body_item = body_item_data.to_dict()
            _kwargs["json"].append(body_item)




        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ProductionPutBatchesResponse200]:
    if response.status_code == 200:
        response_200 = ProductionPutBatchesResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ProductionPutBatchesResponse200]:
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
        list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch'],
        list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch'],
        list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch'],
    ],

) -> Response[ProductionPutBatchesResponse200]:
    """ Add or update unit batches.

    Args:
        body (list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch']):
        body (list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch']):
        body (list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionPutBatchesResponse200]
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
        list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch'],
        list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch'],
        list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch'],
    ],

) -> Optional[ProductionPutBatchesResponse200]:
    """ Add or update unit batches.

    Args:
        body (list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch']):
        body (list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch']):
        body (list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionPutBatchesResponse200
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch'],
        list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch'],
        list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch'],
    ],

) -> Response[ProductionPutBatchesResponse200]:
    """ Add or update unit batches.

    Args:
        body (list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch']):
        body (list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch']):
        body (list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionPutBatchesResponse200]
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
        list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch'],
        list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch'],
        list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch'],
    ],

) -> Optional[ProductionPutBatchesResponse200]:
    """ Add or update unit batches.

    Args:
        body (list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch']):
        body (list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch']):
        body (list['VirincoWATSWebDashboardModelsMesProductionPublicProductionBatch']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionPutBatchesResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
