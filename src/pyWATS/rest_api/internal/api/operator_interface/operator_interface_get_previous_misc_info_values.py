from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.virinco_wats_web_dashboard_models_misc_info import VirincoWATSWebDashboardModelsMiscInfo
from typing import cast



def _get_kwargs(
    *,
    serial_number: str,
    part_number: str,
    process_code: int,
    report_type: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["serialNumber"] = serial_number

    params["partNumber"] = part_number

    params["processCode"] = process_code

    params["reportType"] = report_type


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/OperatorInterface/GetPreviousMiscInfoValues",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[list['VirincoWATSWebDashboardModelsMiscInfo']]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            response_200_item = VirincoWATSWebDashboardModelsMiscInfo.from_dict(response_200_item_data)



            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[list['VirincoWATSWebDashboardModelsMiscInfo']]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number: str,
    part_number: str,
    process_code: int,
    report_type: str,

) -> Response[list['VirincoWATSWebDashboardModelsMiscInfo']]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        process_code (int):
        report_type (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VirincoWATSWebDashboardModelsMiscInfo']]
     """


    kwargs = _get_kwargs(
        serial_number=serial_number,
part_number=part_number,
process_code=process_code,
report_type=report_type,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number: str,
    part_number: str,
    process_code: int,
    report_type: str,

) -> Optional[list['VirincoWATSWebDashboardModelsMiscInfo']]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        process_code (int):
        report_type (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VirincoWATSWebDashboardModelsMiscInfo']
     """


    return sync_detailed(
        client=client,
serial_number=serial_number,
part_number=part_number,
process_code=process_code,
report_type=report_type,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number: str,
    part_number: str,
    process_code: int,
    report_type: str,

) -> Response[list['VirincoWATSWebDashboardModelsMiscInfo']]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        process_code (int):
        report_type (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VirincoWATSWebDashboardModelsMiscInfo']]
     """


    kwargs = _get_kwargs(
        serial_number=serial_number,
part_number=part_number,
process_code=process_code,
report_type=report_type,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number: str,
    part_number: str,
    process_code: int,
    report_type: str,

) -> Optional[list['VirincoWATSWebDashboardModelsMiscInfo']]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        process_code (int):
        report_type (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VirincoWATSWebDashboardModelsMiscInfo']
     """


    return (await asyncio_detailed(
        client=client,
serial_number=serial_number,
part_number=part_number,
process_code=process_code,
report_type=report_type,

    )).parsed
