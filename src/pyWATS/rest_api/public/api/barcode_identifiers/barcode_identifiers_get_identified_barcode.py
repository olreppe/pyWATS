from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.virinco_wats_web_dashboard_models_tdm_barcode_identifier import VirincoWATSWebDashboardModelsTdmBarcodeIdentifier
from typing import cast



def _get_kwargs(
    *,
    code: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["code"] = code


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/BarcodeIdentifiers/IdentifyBarcode",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[VirincoWATSWebDashboardModelsTdmBarcodeIdentifier]:
    if response.status_code == 200:
        response_200 = VirincoWATSWebDashboardModelsTdmBarcodeIdentifier.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[VirincoWATSWebDashboardModelsTdmBarcodeIdentifier]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    code: str,

) -> Response[VirincoWATSWebDashboardModelsTdmBarcodeIdentifier]:
    """  Identify a barcode.

    ‏‏‎ ‎

     Default format:

     SerialNumber/PartNumber/Revision/BatchNumber/Process

    Args:
        code (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VirincoWATSWebDashboardModelsTdmBarcodeIdentifier]
     """


    kwargs = _get_kwargs(
        code=code,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    code: str,

) -> Optional[VirincoWATSWebDashboardModelsTdmBarcodeIdentifier]:
    """  Identify a barcode.

    ‏‏‎ ‎

     Default format:

     SerialNumber/PartNumber/Revision/BatchNumber/Process

    Args:
        code (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VirincoWATSWebDashboardModelsTdmBarcodeIdentifier
     """


    return sync_detailed(
        client=client,
code=code,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    code: str,

) -> Response[VirincoWATSWebDashboardModelsTdmBarcodeIdentifier]:
    """  Identify a barcode.

    ‏‏‎ ‎

     Default format:

     SerialNumber/PartNumber/Revision/BatchNumber/Process

    Args:
        code (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[VirincoWATSWebDashboardModelsTdmBarcodeIdentifier]
     """


    kwargs = _get_kwargs(
        code=code,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    code: str,

) -> Optional[VirincoWATSWebDashboardModelsTdmBarcodeIdentifier]:
    """  Identify a barcode.

    ‏‏‎ ‎

     Default format:

     SerialNumber/PartNumber/Revision/BatchNumber/Process

    Args:
        code (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        VirincoWATSWebDashboardModelsTdmBarcodeIdentifier
     """


    return (await asyncio_detailed(
        client=client,
code=code,

    )).parsed
