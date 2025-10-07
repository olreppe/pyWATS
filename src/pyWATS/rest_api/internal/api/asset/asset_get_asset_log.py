from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.virinco_wats_web_dashboard_models_mes_asset_o_data_asset_log import VirincoWATSWebDashboardModelsMesAssetODataAssetLog
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/Asset/Log",
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[list['VirincoWATSWebDashboardModelsMesAssetODataAssetLog']]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            response_200_item = VirincoWATSWebDashboardModelsMesAssetODataAssetLog.from_dict(response_200_item_data)



            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[list['VirincoWATSWebDashboardModelsMesAssetODataAssetLog']]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[list['VirincoWATSWebDashboardModelsMesAssetODataAssetLog']]:
    """ Returns a list of asset log records matching the specified filter.

     This method supports OData query options such as the $filter, $top or $orderby query parameters.
    Returns top 1000 logs unless the $top query parameter have been specified with another value (e.g.
    $top=1).

    Results are always ordered by descending by log date/time (UTC), unless the $orderby query parameter
    has been specified otherwise.

    Examples:

    Log records for a certain asset:
    https://your-server-address/api/Asset/Log?$filter=assetId eq '1'

    Certain type of log records for an asset (e.g. asset update records only):
    https://your-server-address/api/Asset/Log?$filter=assetId eq '1' and type eq 2

    Type can be:
    0 = Message

    1 = Register (Asset created)

    2 = Update (Asset property updated)

    3 = Reset count (Running count has been reset in Asset Manager)

    4 = Calibration (Asset has been calibrated)

    5 = Maintenance (Asset has had maintenance)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VirincoWATSWebDashboardModelsMesAssetODataAssetLog']]
     """


    kwargs = _get_kwargs(
        
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[list['VirincoWATSWebDashboardModelsMesAssetODataAssetLog']]:
    """ Returns a list of asset log records matching the specified filter.

     This method supports OData query options such as the $filter, $top or $orderby query parameters.
    Returns top 1000 logs unless the $top query parameter have been specified with another value (e.g.
    $top=1).

    Results are always ordered by descending by log date/time (UTC), unless the $orderby query parameter
    has been specified otherwise.

    Examples:

    Log records for a certain asset:
    https://your-server-address/api/Asset/Log?$filter=assetId eq '1'

    Certain type of log records for an asset (e.g. asset update records only):
    https://your-server-address/api/Asset/Log?$filter=assetId eq '1' and type eq 2

    Type can be:
    0 = Message

    1 = Register (Asset created)

    2 = Update (Asset property updated)

    3 = Reset count (Running count has been reset in Asset Manager)

    4 = Calibration (Asset has been calibrated)

    5 = Maintenance (Asset has had maintenance)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VirincoWATSWebDashboardModelsMesAssetODataAssetLog']
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[list['VirincoWATSWebDashboardModelsMesAssetODataAssetLog']]:
    """ Returns a list of asset log records matching the specified filter.

     This method supports OData query options such as the $filter, $top or $orderby query parameters.
    Returns top 1000 logs unless the $top query parameter have been specified with another value (e.g.
    $top=1).

    Results are always ordered by descending by log date/time (UTC), unless the $orderby query parameter
    has been specified otherwise.

    Examples:

    Log records for a certain asset:
    https://your-server-address/api/Asset/Log?$filter=assetId eq '1'

    Certain type of log records for an asset (e.g. asset update records only):
    https://your-server-address/api/Asset/Log?$filter=assetId eq '1' and type eq 2

    Type can be:
    0 = Message

    1 = Register (Asset created)

    2 = Update (Asset property updated)

    3 = Reset count (Running count has been reset in Asset Manager)

    4 = Calibration (Asset has been calibrated)

    5 = Maintenance (Asset has had maintenance)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VirincoWATSWebDashboardModelsMesAssetODataAssetLog']]
     """


    kwargs = _get_kwargs(
        
    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[list['VirincoWATSWebDashboardModelsMesAssetODataAssetLog']]:
    """ Returns a list of asset log records matching the specified filter.

     This method supports OData query options such as the $filter, $top or $orderby query parameters.
    Returns top 1000 logs unless the $top query parameter have been specified with another value (e.g.
    $top=1).

    Results are always ordered by descending by log date/time (UTC), unless the $orderby query parameter
    has been specified otherwise.

    Examples:

    Log records for a certain asset:
    https://your-server-address/api/Asset/Log?$filter=assetId eq '1'

    Certain type of log records for an asset (e.g. asset update records only):
    https://your-server-address/api/Asset/Log?$filter=assetId eq '1' and type eq 2

    Type can be:
    0 = Message

    1 = Register (Asset created)

    2 = Update (Asset property updated)

    3 = Reset count (Running count has been reset in Asset Manager)

    4 = Calibration (Asset has been calibrated)

    5 = Maintenance (Asset has had maintenance)

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VirincoWATSWebDashboardModelsMesAssetODataAssetLog']
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
