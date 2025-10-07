from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.virinco_wats_web_dashboard_models_data_access_watsuut_result import VirincoWATSWebDashboardModelsDataAccessWATSUUTResult
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    process_code: Union[Unset, int] = UNSET,
    serial_number: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    data: Union[Unset, str] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["processCode"] = process_code

    params["serialNumber"] = serial_number

    params["description"] = description

    params["data"] = data


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/Report/Query/HeaderByMiscInfo",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[list['VirincoWATSWebDashboardModelsDataAccessWATSUUTResult']]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            response_200_item = VirincoWATSWebDashboardModelsDataAccessWATSUUTResult.from_dict(response_200_item_data)



            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[list['VirincoWATSWebDashboardModelsDataAccessWATSUUTResult']]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    process_code: Union[Unset, int] = UNSET,
    serial_number: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    data: Union[Unset, str] = UNSET,

) -> Response[list['VirincoWATSWebDashboardModelsDataAccessWATSUUTResult']]:
    """ Get report header data by searching for misc information

    Args:
        process_code (Union[Unset, int]):
        serial_number (Union[Unset, str]):
        description (Union[Unset, str]):
        data (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VirincoWATSWebDashboardModelsDataAccessWATSUUTResult']]
     """


    kwargs = _get_kwargs(
        process_code=process_code,
serial_number=serial_number,
description=description,
data=data,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    process_code: Union[Unset, int] = UNSET,
    serial_number: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    data: Union[Unset, str] = UNSET,

) -> Optional[list['VirincoWATSWebDashboardModelsDataAccessWATSUUTResult']]:
    """ Get report header data by searching for misc information

    Args:
        process_code (Union[Unset, int]):
        serial_number (Union[Unset, str]):
        description (Union[Unset, str]):
        data (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VirincoWATSWebDashboardModelsDataAccessWATSUUTResult']
     """


    return sync_detailed(
        client=client,
process_code=process_code,
serial_number=serial_number,
description=description,
data=data,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    process_code: Union[Unset, int] = UNSET,
    serial_number: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    data: Union[Unset, str] = UNSET,

) -> Response[list['VirincoWATSWebDashboardModelsDataAccessWATSUUTResult']]:
    """ Get report header data by searching for misc information

    Args:
        process_code (Union[Unset, int]):
        serial_number (Union[Unset, str]):
        description (Union[Unset, str]):
        data (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VirincoWATSWebDashboardModelsDataAccessWATSUUTResult']]
     """


    kwargs = _get_kwargs(
        process_code=process_code,
serial_number=serial_number,
description=description,
data=data,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    process_code: Union[Unset, int] = UNSET,
    serial_number: Union[Unset, str] = UNSET,
    description: Union[Unset, str] = UNSET,
    data: Union[Unset, str] = UNSET,

) -> Optional[list['VirincoWATSWebDashboardModelsDataAccessWATSUUTResult']]:
    """ Get report header data by searching for misc information

    Args:
        process_code (Union[Unset, int]):
        serial_number (Union[Unset, str]):
        description (Union[Unset, str]):
        data (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VirincoWATSWebDashboardModelsDataAccessWATSUUTResult']
     """


    return (await asyncio_detailed(
        client=client,
process_code=process_code,
serial_number=serial_number,
description=description,
data=data,

    )).parsed
