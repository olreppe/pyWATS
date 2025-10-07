from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.virinco_wats_web_dashboard_models_mes_product_product_view import VirincoWATSWebDashboardModelsMesProductProductView
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/Product/Query",
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[list['VirincoWATSWebDashboardModelsMesProductProductView']]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            response_200_item = VirincoWATSWebDashboardModelsMesProductProductView.from_dict(response_200_item_data)



            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[list['VirincoWATSWebDashboardModelsMesProductProductView']]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[list['VirincoWATSWebDashboardModelsMesProductProductView']]:
    """ Returns the list of products matching the specified filter.

      Method supports OData query options such as $filter and $top.
     Only returns $top=1000 if $filter option is not specified

    Examples:

    Restrict to a specified part number:
    https://your-server-address/api/product/query?$filter=PartNumber eq 'XYZ123'

    Restrict to a product category:
    https://your-server-address/api/product/query?$filter=Category eq 'PCB'

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VirincoWATSWebDashboardModelsMesProductProductView']]
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

) -> Optional[list['VirincoWATSWebDashboardModelsMesProductProductView']]:
    """ Returns the list of products matching the specified filter.

      Method supports OData query options such as $filter and $top.
     Only returns $top=1000 if $filter option is not specified

    Examples:

    Restrict to a specified part number:
    https://your-server-address/api/product/query?$filter=PartNumber eq 'XYZ123'

    Restrict to a product category:
    https://your-server-address/api/product/query?$filter=Category eq 'PCB'

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VirincoWATSWebDashboardModelsMesProductProductView']
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[list['VirincoWATSWebDashboardModelsMesProductProductView']]:
    """ Returns the list of products matching the specified filter.

      Method supports OData query options such as $filter and $top.
     Only returns $top=1000 if $filter option is not specified

    Examples:

    Restrict to a specified part number:
    https://your-server-address/api/product/query?$filter=PartNumber eq 'XYZ123'

    Restrict to a product category:
    https://your-server-address/api/product/query?$filter=Category eq 'PCB'

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VirincoWATSWebDashboardModelsMesProductProductView']]
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

) -> Optional[list['VirincoWATSWebDashboardModelsMesProductProductView']]:
    """ Returns the list of products matching the specified filter.

      Method supports OData query options such as $filter and $top.
     Only returns $top=1000 if $filter option is not specified

    Examples:

    Restrict to a specified part number:
    https://your-server-address/api/product/query?$filter=PartNumber eq 'XYZ123'

    Restrict to a product category:
    https://your-server-address/api/product/query?$filter=Category eq 'PCB'

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VirincoWATSWebDashboardModelsMesProductProductView']
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
