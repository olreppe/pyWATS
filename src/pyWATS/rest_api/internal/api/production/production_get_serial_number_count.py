from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.production_get_serial_number_count_response_200 import ProductionGetSerialNumberCountResponse200
from ...types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
import datetime



def _get_kwargs(
    *,
    serial_number_type: str,
    start_address: Union[Unset, str] = UNSET,
    end_address: Union[Unset, str] = UNSET,
    from_date: Union[Unset, datetime.datetime] = UNSET,
    to_date: Union[Unset, datetime.datetime] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["serialNumberType"] = serial_number_type

    params["startAddress"] = start_address

    params["endAddress"] = end_address

    json_from_date: Union[Unset, str] = UNSET
    if not isinstance(from_date, Unset):
        json_from_date = from_date.isoformat()
    params["fromDate"] = json_from_date

    json_to_date: Union[Unset, str] = UNSET
    if not isinstance(to_date, Unset):
        json_to_date = to_date.isoformat()
    params["toDate"] = json_to_date


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Production/SerialNumbers/Count",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ProductionGetSerialNumberCountResponse200]:
    if response.status_code == 200:
        response_200 = ProductionGetSerialNumberCountResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ProductionGetSerialNumberCountResponse200]:
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
    start_address: Union[Unset, str] = UNSET,
    end_address: Union[Unset, str] = UNSET,
    from_date: Union[Unset, datetime.datetime] = UNSET,
    to_date: Union[Unset, datetime.datetime] = UNSET,

) -> Response[ProductionGetSerialNumberCountResponse200]:
    """ Retrieves the number of affected serial numbers prior to export of data

    Args:
        serial_number_type (str):
        start_address (Union[Unset, str]):
        end_address (Union[Unset, str]):
        from_date (Union[Unset, datetime.datetime]):
        to_date (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionGetSerialNumberCountResponse200]
     """


    kwargs = _get_kwargs(
        serial_number_type=serial_number_type,
start_address=start_address,
end_address=end_address,
from_date=from_date,
to_date=to_date,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number_type: str,
    start_address: Union[Unset, str] = UNSET,
    end_address: Union[Unset, str] = UNSET,
    from_date: Union[Unset, datetime.datetime] = UNSET,
    to_date: Union[Unset, datetime.datetime] = UNSET,

) -> Optional[ProductionGetSerialNumberCountResponse200]:
    """ Retrieves the number of affected serial numbers prior to export of data

    Args:
        serial_number_type (str):
        start_address (Union[Unset, str]):
        end_address (Union[Unset, str]):
        from_date (Union[Unset, datetime.datetime]):
        to_date (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionGetSerialNumberCountResponse200
     """


    return sync_detailed(
        client=client,
serial_number_type=serial_number_type,
start_address=start_address,
end_address=end_address,
from_date=from_date,
to_date=to_date,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number_type: str,
    start_address: Union[Unset, str] = UNSET,
    end_address: Union[Unset, str] = UNSET,
    from_date: Union[Unset, datetime.datetime] = UNSET,
    to_date: Union[Unset, datetime.datetime] = UNSET,

) -> Response[ProductionGetSerialNumberCountResponse200]:
    """ Retrieves the number of affected serial numbers prior to export of data

    Args:
        serial_number_type (str):
        start_address (Union[Unset, str]):
        end_address (Union[Unset, str]):
        from_date (Union[Unset, datetime.datetime]):
        to_date (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductionGetSerialNumberCountResponse200]
     """


    kwargs = _get_kwargs(
        serial_number_type=serial_number_type,
start_address=start_address,
end_address=end_address,
from_date=from_date,
to_date=to_date,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number_type: str,
    start_address: Union[Unset, str] = UNSET,
    end_address: Union[Unset, str] = UNSET,
    from_date: Union[Unset, datetime.datetime] = UNSET,
    to_date: Union[Unset, datetime.datetime] = UNSET,

) -> Optional[ProductionGetSerialNumberCountResponse200]:
    """ Retrieves the number of affected serial numbers prior to export of data

    Args:
        serial_number_type (str):
        start_address (Union[Unset, str]):
        end_address (Union[Unset, str]):
        from_date (Union[Unset, datetime.datetime]):
        to_date (Union[Unset, datetime.datetime]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductionGetSerialNumberCountResponse200
     """


    return (await asyncio_detailed(
        client=client,
serial_number_type=serial_number_type,
start_address=start_address,
end_address=end_address,
from_date=from_date,
to_date=to_date,

    )).parsed
