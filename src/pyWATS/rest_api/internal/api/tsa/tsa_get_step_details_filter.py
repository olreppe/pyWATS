from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.tsa_get_step_details_filter_response_200 import TSAGetStepDetailsFilterResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    uuid: str,
    step_order_number: int,
    part_number: str,
    process_code: int,
    revision: str,
    utc_date: str,
    sw_version: str,
    sw_filename: str,
    process_name: str,
    measure_name: Union[Unset, str] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["uuid"] = uuid

    params["stepOrderNumber"] = step_order_number

    params["partNumber"] = part_number

    params["processCode"] = process_code

    params["revision"] = revision

    params["utcDate"] = utc_date

    params["swVersion"] = sw_version

    params["swFilename"] = sw_filename

    params["processName"] = process_name

    params["measureName"] = measure_name


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/TSA/GetStepDetailsFilter",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[TSAGetStepDetailsFilterResponse200]:
    if response.status_code == 200:
        response_200 = TSAGetStepDetailsFilterResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[TSAGetStepDetailsFilterResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    uuid: str,
    step_order_number: int,
    part_number: str,
    process_code: int,
    revision: str,
    utc_date: str,
    sw_version: str,
    sw_filename: str,
    process_name: str,
    measure_name: Union[Unset, str] = UNSET,

) -> Response[TSAGetStepDetailsFilterResponse200]:
    """ UUT drilldown to step-details

    Args:
        uuid (str):
        step_order_number (int):
        part_number (str):
        process_code (int):
        revision (str):
        utc_date (str):
        sw_version (str):
        sw_filename (str):
        process_name (str):
        measure_name (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TSAGetStepDetailsFilterResponse200]
     """


    kwargs = _get_kwargs(
        uuid=uuid,
step_order_number=step_order_number,
part_number=part_number,
process_code=process_code,
revision=revision,
utc_date=utc_date,
sw_version=sw_version,
sw_filename=sw_filename,
process_name=process_name,
measure_name=measure_name,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    uuid: str,
    step_order_number: int,
    part_number: str,
    process_code: int,
    revision: str,
    utc_date: str,
    sw_version: str,
    sw_filename: str,
    process_name: str,
    measure_name: Union[Unset, str] = UNSET,

) -> Optional[TSAGetStepDetailsFilterResponse200]:
    """ UUT drilldown to step-details

    Args:
        uuid (str):
        step_order_number (int):
        part_number (str):
        process_code (int):
        revision (str):
        utc_date (str):
        sw_version (str):
        sw_filename (str):
        process_name (str):
        measure_name (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TSAGetStepDetailsFilterResponse200
     """


    return sync_detailed(
        client=client,
uuid=uuid,
step_order_number=step_order_number,
part_number=part_number,
process_code=process_code,
revision=revision,
utc_date=utc_date,
sw_version=sw_version,
sw_filename=sw_filename,
process_name=process_name,
measure_name=measure_name,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    uuid: str,
    step_order_number: int,
    part_number: str,
    process_code: int,
    revision: str,
    utc_date: str,
    sw_version: str,
    sw_filename: str,
    process_name: str,
    measure_name: Union[Unset, str] = UNSET,

) -> Response[TSAGetStepDetailsFilterResponse200]:
    """ UUT drilldown to step-details

    Args:
        uuid (str):
        step_order_number (int):
        part_number (str):
        process_code (int):
        revision (str):
        utc_date (str):
        sw_version (str):
        sw_filename (str):
        process_name (str):
        measure_name (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TSAGetStepDetailsFilterResponse200]
     """


    kwargs = _get_kwargs(
        uuid=uuid,
step_order_number=step_order_number,
part_number=part_number,
process_code=process_code,
revision=revision,
utc_date=utc_date,
sw_version=sw_version,
sw_filename=sw_filename,
process_name=process_name,
measure_name=measure_name,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    uuid: str,
    step_order_number: int,
    part_number: str,
    process_code: int,
    revision: str,
    utc_date: str,
    sw_version: str,
    sw_filename: str,
    process_name: str,
    measure_name: Union[Unset, str] = UNSET,

) -> Optional[TSAGetStepDetailsFilterResponse200]:
    """ UUT drilldown to step-details

    Args:
        uuid (str):
        step_order_number (int):
        part_number (str):
        process_code (int):
        revision (str):
        utc_date (str):
        sw_version (str):
        sw_filename (str):
        process_name (str):
        measure_name (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TSAGetStepDetailsFilterResponse200
     """


    return (await asyncio_detailed(
        client=client,
uuid=uuid,
step_order_number=step_order_number,
part_number=part_number,
process_code=process_code,
revision=revision,
utc_date=utc_date,
sw_version=sw_version,
sw_filename=sw_filename,
process_name=process_name,
measure_name=measure_name,

    )).parsed
