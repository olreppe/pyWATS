from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.product_bom_response_200 import ProductBOMResponse200
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/Product/BOM",
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[Any, ProductBOMResponse200]]:
    if response.status_code == 200:
        response_200 = ProductBOMResponse200.from_dict(response.json())



        return response_200

    if response.status_code == 500:
        response_500 = cast(Any, None)
        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[Any, ProductBOMResponse200]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[Union[Any, ProductBOMResponse200]]:
    r""" Inserts or updates a BOM using WSBF (WATS Standard BOM Format) in the request body

     <a target=\"_blank\" href=\"http://support.virinco.com/hc/en-us/articles/115000498526-Add-BOM-list-
    to-WATS\">Click here for documentation and examples (Add BOM list to WATS)</a>

                Request body example (Content-Type: application/xml):
                <pre lang=\"xml\">
                &lt;?xml version=\"1.0\" encoding=\"utf-16\"?&gt;
                &lt;BOM Partnumber=\"100100\" Revision=\"1.0\" Desc=\"Product Description\"
    xmlns=\"http://wats.virinco.com/schemas/WATS/wsbf \"&gt;
                 &lt;Component Number=\"100200\" Rev=\"1.0\" Qty=\"2\" Desc=\"Component Description\"
    Ref=\"A30;A31\" FunctionBlock=\"A\" /&gt;
                 &lt;Component Number=\"100201\" Rev=\"1.1\" Qty=\"2\" Desc=\"Component Description\"
    Ref=\"A32;A34\" FunctionBlock=\"B\" /&gt;
                &lt;/BOM&gt;
                </pre>

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ProductBOMResponse200]]
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

) -> Optional[Union[Any, ProductBOMResponse200]]:
    r""" Inserts or updates a BOM using WSBF (WATS Standard BOM Format) in the request body

     <a target=\"_blank\" href=\"http://support.virinco.com/hc/en-us/articles/115000498526-Add-BOM-list-
    to-WATS\">Click here for documentation and examples (Add BOM list to WATS)</a>

                Request body example (Content-Type: application/xml):
                <pre lang=\"xml\">
                &lt;?xml version=\"1.0\" encoding=\"utf-16\"?&gt;
                &lt;BOM Partnumber=\"100100\" Revision=\"1.0\" Desc=\"Product Description\"
    xmlns=\"http://wats.virinco.com/schemas/WATS/wsbf \"&gt;
                 &lt;Component Number=\"100200\" Rev=\"1.0\" Qty=\"2\" Desc=\"Component Description\"
    Ref=\"A30;A31\" FunctionBlock=\"A\" /&gt;
                 &lt;Component Number=\"100201\" Rev=\"1.1\" Qty=\"2\" Desc=\"Component Description\"
    Ref=\"A32;A34\" FunctionBlock=\"B\" /&gt;
                &lt;/BOM&gt;
                </pre>

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ProductBOMResponse200]
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[Union[Any, ProductBOMResponse200]]:
    r""" Inserts or updates a BOM using WSBF (WATS Standard BOM Format) in the request body

     <a target=\"_blank\" href=\"http://support.virinco.com/hc/en-us/articles/115000498526-Add-BOM-list-
    to-WATS\">Click here for documentation and examples (Add BOM list to WATS)</a>

                Request body example (Content-Type: application/xml):
                <pre lang=\"xml\">
                &lt;?xml version=\"1.0\" encoding=\"utf-16\"?&gt;
                &lt;BOM Partnumber=\"100100\" Revision=\"1.0\" Desc=\"Product Description\"
    xmlns=\"http://wats.virinco.com/schemas/WATS/wsbf \"&gt;
                 &lt;Component Number=\"100200\" Rev=\"1.0\" Qty=\"2\" Desc=\"Component Description\"
    Ref=\"A30;A31\" FunctionBlock=\"A\" /&gt;
                 &lt;Component Number=\"100201\" Rev=\"1.1\" Qty=\"2\" Desc=\"Component Description\"
    Ref=\"A32;A34\" FunctionBlock=\"B\" /&gt;
                &lt;/BOM&gt;
                </pre>

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ProductBOMResponse200]]
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

) -> Optional[Union[Any, ProductBOMResponse200]]:
    r""" Inserts or updates a BOM using WSBF (WATS Standard BOM Format) in the request body

     <a target=\"_blank\" href=\"http://support.virinco.com/hc/en-us/articles/115000498526-Add-BOM-list-
    to-WATS\">Click here for documentation and examples (Add BOM list to WATS)</a>

                Request body example (Content-Type: application/xml):
                <pre lang=\"xml\">
                &lt;?xml version=\"1.0\" encoding=\"utf-16\"?&gt;
                &lt;BOM Partnumber=\"100100\" Revision=\"1.0\" Desc=\"Product Description\"
    xmlns=\"http://wats.virinco.com/schemas/WATS/wsbf \"&gt;
                 &lt;Component Number=\"100200\" Rev=\"1.0\" Qty=\"2\" Desc=\"Component Description\"
    Ref=\"A30;A31\" FunctionBlock=\"A\" /&gt;
                 &lt;Component Number=\"100201\" Rev=\"1.1\" Qty=\"2\" Desc=\"Component Description\"
    Ref=\"A32;A34\" FunctionBlock=\"B\" /&gt;
                &lt;/BOM&gt;
                </pre>

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ProductBOMResponse200]
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
