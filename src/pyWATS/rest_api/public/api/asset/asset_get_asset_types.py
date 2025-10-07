from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.virinco_wats_web_dashboard_models_mes_asset_o_data_asset_type import VirincoWATSWebDashboardModelsMesAssetODataAssetType
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/Asset/Types",
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[list['VirincoWATSWebDashboardModelsMesAssetODataAssetType']]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            response_200_item = VirincoWATSWebDashboardModelsMesAssetODataAssetType.from_dict(response_200_item_data)



            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[list['VirincoWATSWebDashboardModelsMesAssetODataAssetType']]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[list['VirincoWATSWebDashboardModelsMesAssetODataAssetType']]:
    """ Returns a list of asset types matching the specified filter.

     This method supports OData query options such as the $filter, $top or $orderby query parameters.
    Returns top 1000 types unless the $top query parameter have been specified with another value (e.g.
    $top=1).
    Results are always ordered by name, unless the $orderby query parameter has been specified
    otherwise.

    Examples:

    Restrict to a certain asset type:
    https://your-server-address/api/Asset/Types?$filter=typeName eq 'Fixture'

    Asset types requiring calibration each 30 days:
    https://your-server-address/api/Asset/Types?$filter=calibrationInterval eq 30

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VirincoWATSWebDashboardModelsMesAssetODataAssetType']]
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

) -> Optional[list['VirincoWATSWebDashboardModelsMesAssetODataAssetType']]:
    """ Returns a list of asset types matching the specified filter.

     This method supports OData query options such as the $filter, $top or $orderby query parameters.
    Returns top 1000 types unless the $top query parameter have been specified with another value (e.g.
    $top=1).
    Results are always ordered by name, unless the $orderby query parameter has been specified
    otherwise.

    Examples:

    Restrict to a certain asset type:
    https://your-server-address/api/Asset/Types?$filter=typeName eq 'Fixture'

    Asset types requiring calibration each 30 days:
    https://your-server-address/api/Asset/Types?$filter=calibrationInterval eq 30

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VirincoWATSWebDashboardModelsMesAssetODataAssetType']
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[list['VirincoWATSWebDashboardModelsMesAssetODataAssetType']]:
    """ Returns a list of asset types matching the specified filter.

     This method supports OData query options such as the $filter, $top or $orderby query parameters.
    Returns top 1000 types unless the $top query parameter have been specified with another value (e.g.
    $top=1).
    Results are always ordered by name, unless the $orderby query parameter has been specified
    otherwise.

    Examples:

    Restrict to a certain asset type:
    https://your-server-address/api/Asset/Types?$filter=typeName eq 'Fixture'

    Asset types requiring calibration each 30 days:
    https://your-server-address/api/Asset/Types?$filter=calibrationInterval eq 30

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VirincoWATSWebDashboardModelsMesAssetODataAssetType']]
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

) -> Optional[list['VirincoWATSWebDashboardModelsMesAssetODataAssetType']]:
    """ Returns a list of asset types matching the specified filter.

     This method supports OData query options such as the $filter, $top or $orderby query parameters.
    Returns top 1000 types unless the $top query parameter have been specified with another value (e.g.
    $top=1).
    Results are always ordered by name, unless the $orderby query parameter has been specified
    otherwise.

    Examples:

    Restrict to a certain asset type:
    https://your-server-address/api/Asset/Types?$filter=typeName eq 'Fixture'

    Asset types requiring calibration each 30 days:
    https://your-server-address/api/Asset/Types?$filter=calibrationInterval eq 30

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VirincoWATSWebDashboardModelsMesAssetODataAssetType']
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
