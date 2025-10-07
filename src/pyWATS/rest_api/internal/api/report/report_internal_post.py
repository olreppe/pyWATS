from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.system_xml_linq_x_element import SystemXmlLinqXElement
from ...models.virinco_wats_models_store_insert_report_result import VirincoWATSModelsStoreInsertReportResult
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        SystemXmlLinqXElement,
        SystemXmlLinqXElement,
        SystemXmlLinqXElement,
    ],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Report/InternalPost",
    }

    if isinstance(body, SystemXmlLinqXElement):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, SystemXmlLinqXElement):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, SystemXmlLinqXElement):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[list['VirincoWATSModelsStoreInsertReportResult']]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            response_200_item = VirincoWATSModelsStoreInsertReportResult.from_dict(response_200_item_data)



            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[list['VirincoWATSModelsStoreInsertReportResult']]:
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
        SystemXmlLinqXElement,
        SystemXmlLinqXElement,
        SystemXmlLinqXElement,
    ],

) -> Response[list['VirincoWATSModelsStoreInsertReportResult']]:
    """ Swagger support - Post WRML report

    Args:
        body (SystemXmlLinqXElement):
        body (SystemXmlLinqXElement):
        body (SystemXmlLinqXElement):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VirincoWATSModelsStoreInsertReportResult']]
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
        SystemXmlLinqXElement,
        SystemXmlLinqXElement,
        SystemXmlLinqXElement,
    ],

) -> Optional[list['VirincoWATSModelsStoreInsertReportResult']]:
    """ Swagger support - Post WRML report

    Args:
        body (SystemXmlLinqXElement):
        body (SystemXmlLinqXElement):
        body (SystemXmlLinqXElement):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VirincoWATSModelsStoreInsertReportResult']
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        SystemXmlLinqXElement,
        SystemXmlLinqXElement,
        SystemXmlLinqXElement,
    ],

) -> Response[list['VirincoWATSModelsStoreInsertReportResult']]:
    """ Swagger support - Post WRML report

    Args:
        body (SystemXmlLinqXElement):
        body (SystemXmlLinqXElement):
        body (SystemXmlLinqXElement):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VirincoWATSModelsStoreInsertReportResult']]
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
        SystemXmlLinqXElement,
        SystemXmlLinqXElement,
        SystemXmlLinqXElement,
    ],

) -> Optional[list['VirincoWATSModelsStoreInsertReportResult']]:
    """ Swagger support - Post WRML report

    Args:
        body (SystemXmlLinqXElement):
        body (SystemXmlLinqXElement):
        body (SystemXmlLinqXElement):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VirincoWATSModelsStoreInsertReportResult']
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
