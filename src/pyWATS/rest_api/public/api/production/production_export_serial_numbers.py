from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.production_export_serial_numbers_response_200 import ProductionExportSerialNumbersResponse200
from ...types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
import datetime



def _get_kwargs(
    *,
    serial_number_type: str,
    format_: str,
    start_address: Union[Unset, str] = UNSET,
    end_address: Union[Unset, str] = UNSET,
    start_date: Union[Unset, datetime.datetime] = UNSET,
    end_date: Union[Unset, datetime.datetime] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["serialNumberType"] = serial_number_type

    params["format"] = format_

    params["startAddress"] = start_address

    params["endAddress"] = end_address

    json_start_date: Union[Unset, str] = UNSET
    if not isinstance(start_date, Unset):
        json_start_date = start_date.isoformat()
    params["startDate"] = json_start_date

    json_end_date: Union[Unset, str] = UNSET
    if not isinstance(end_date, Unset):
        json_end_date = end_date.isoformat()
    params["endDate"] = json_end_date


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/Production/SerialNumbers",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ProductionExportSerialNumbersResponse200]:
    if response.status_code == 200:
        response_200 = ProductionExportSerialNumbersResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ProductionExportSerialNumbersResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number_type: str,
    format_: str,
    start_address: Union[Unset, str] = UNSET,
    end_address: Union[Unset, str] = UNSET,
    start_date: Union[Unset, datetime.datetime] = UNSET,
    end_date: Union[Unset, datetime.datetime] = UNSET,

) -> Response[ProductionExportSerialNumbersResponse200]:
    """ Get an export of serial numbers as XML or CSV file.

    Args:
        serial_number_type (str):
        format_ (str):
        start_address (Union[Unset, str]):
        end_address (Union[Unset, str]):
        start_date (Union[Unset, datetime.datetime]):
        end_date (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionExportSerialNumbersResponse200]
     """


    kwargs = _get_kwargs(
        serial_number_type=serial_number_type,
format_=format_,
start_address=start_address,
end_address=end_address,
start_date=start_date,
end_date=end_date,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number_type: str,
    format_: str,
    start_address: Union[Unset, str] = UNSET,
    end_address: Union[Unset, str] = UNSET,
    start_date: Union[Unset, datetime.datetime] = UNSET,
    end_date: Union[Unset, datetime.datetime] = UNSET,

) -> Optional[ProductionExportSerialNumbersResponse200]:
    """ Get an export of serial numbers as XML or CSV file.

    Args:
        serial_number_type (str):
        format_ (str):
        start_address (Union[Unset, str]):
        end_address (Union[Unset, str]):
        start_date (Union[Unset, datetime.datetime]):
        end_date (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionExportSerialNumbersResponse200
     """


    return sync_detailed(
        client=client,
serial_number_type=serial_number_type,
format_=format_,
start_address=start_address,
end_address=end_address,
start_date=start_date,
end_date=end_date,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number_type: str,
    format_: str,
    start_address: Union[Unset, str] = UNSET,
    end_address: Union[Unset, str] = UNSET,
    start_date: Union[Unset, datetime.datetime] = UNSET,
    end_date: Union[Unset, datetime.datetime] = UNSET,

) -> Response[ProductionExportSerialNumbersResponse200]:
    """ Get an export of serial numbers as XML or CSV file.

    Args:
        serial_number_type (str):
        format_ (str):
        start_address (Union[Unset, str]):
        end_address (Union[Unset, str]):
        start_date (Union[Unset, datetime.datetime]):
        end_date (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionExportSerialNumbersResponse200]
     """


    kwargs = _get_kwargs(
        serial_number_type=serial_number_type,
format_=format_,
start_address=start_address,
end_address=end_address,
start_date=start_date,
end_date=end_date,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number_type: str,
    format_: str,
    start_address: Union[Unset, str] = UNSET,
    end_address: Union[Unset, str] = UNSET,
    start_date: Union[Unset, datetime.datetime] = UNSET,
    end_date: Union[Unset, datetime.datetime] = UNSET,

) -> Optional[ProductionExportSerialNumbersResponse200]:
    """ Get an export of serial numbers as XML or CSV file.

    Args:
        serial_number_type (str):
        format_ (str):
        start_address (Union[Unset, str]):
        end_address (Union[Unset, str]):
        start_date (Union[Unset, datetime.datetime]):
        end_date (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionExportSerialNumbersResponse200
     """


    return (await asyncio_detailed(
        client=client,
serial_number_type=serial_number_type,
format_=format_,
start_address=start_address,
end_address=end_address,
start_date=start_date,
end_date=end_date,

    )).parsed
