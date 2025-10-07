from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.workflow_public_start_test_response_200 import WorkflowPublicStartTestResponse200
from ...models.workflow_public_start_test_status import WorkflowPublicStartTestStatus
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    serial_number: str,
    part_number: str,
    operator_name: Union[Unset, str] = UNSET,
    station_name: Union[Unset, str] = UNSET,
    status: Union[Unset, WorkflowPublicStartTestStatus] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["serialNumber"] = serial_number

    params["partNumber"] = part_number

    params["operatorName"] = operator_name

    params["stationName"] = station_name

    json_status: Union[Unset, int] = UNSET
    if not isinstance(status, Unset):
        json_status = status.value

    params["status"] = json_status


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/Workflow/StartTest",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[WorkflowPublicStartTestResponse200]:
    if response.status_code == 200:
        response_200 = WorkflowPublicStartTestResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[WorkflowPublicStartTestResponse200]:
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
    operator_name: Union[Unset, str] = UNSET,
    station_name: Union[Unset, str] = UNSET,
    status: Union[Unset, WorkflowPublicStartTestStatus] = UNSET,

) -> Response[WorkflowPublicStartTestResponse200]:
    """ Start workflow test activity

     <ul>
      <li>Unit must exist in WATS MES</li>
      <li>Workflow must be initialized on the unit before use (e.g. via Operator Interface or WATS MES
    API) with same status (see 'status' parameter)</li>
      <li>Current activity type in the unit's workflow must equal to 'Test', or else 'false' will be
    returned by the method</li>
    </ul>

    Args:
        serial_number (str):
        part_number (str):
        operator_name (Union[Unset, str]):
        station_name (Union[Unset, str]):
        status (Union[Unset, WorkflowPublicStartTestStatus]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WorkflowPublicStartTestResponse200]
     """


    kwargs = _get_kwargs(
        serial_number=serial_number,
part_number=part_number,
operator_name=operator_name,
station_name=station_name,
status=status,

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
    operator_name: Union[Unset, str] = UNSET,
    station_name: Union[Unset, str] = UNSET,
    status: Union[Unset, WorkflowPublicStartTestStatus] = UNSET,

) -> Optional[WorkflowPublicStartTestResponse200]:
    """ Start workflow test activity

     <ul>
      <li>Unit must exist in WATS MES</li>
      <li>Workflow must be initialized on the unit before use (e.g. via Operator Interface or WATS MES
    API) with same status (see 'status' parameter)</li>
      <li>Current activity type in the unit's workflow must equal to 'Test', or else 'false' will be
    returned by the method</li>
    </ul>

    Args:
        serial_number (str):
        part_number (str):
        operator_name (Union[Unset, str]):
        station_name (Union[Unset, str]):
        status (Union[Unset, WorkflowPublicStartTestStatus]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WorkflowPublicStartTestResponse200
     """


    return sync_detailed(
        client=client,
serial_number=serial_number,
part_number=part_number,
operator_name=operator_name,
station_name=station_name,
status=status,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    serial_number: str,
    part_number: str,
    operator_name: Union[Unset, str] = UNSET,
    station_name: Union[Unset, str] = UNSET,
    status: Union[Unset, WorkflowPublicStartTestStatus] = UNSET,

) -> Response[WorkflowPublicStartTestResponse200]:
    """ Start workflow test activity

     <ul>
      <li>Unit must exist in WATS MES</li>
      <li>Workflow must be initialized on the unit before use (e.g. via Operator Interface or WATS MES
    API) with same status (see 'status' parameter)</li>
      <li>Current activity type in the unit's workflow must equal to 'Test', or else 'false' will be
    returned by the method</li>
    </ul>

    Args:
        serial_number (str):
        part_number (str):
        operator_name (Union[Unset, str]):
        station_name (Union[Unset, str]):
        status (Union[Unset, WorkflowPublicStartTestStatus]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WorkflowPublicStartTestResponse200]
     """


    kwargs = _get_kwargs(
        serial_number=serial_number,
part_number=part_number,
operator_name=operator_name,
station_name=station_name,
status=status,

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
    operator_name: Union[Unset, str] = UNSET,
    station_name: Union[Unset, str] = UNSET,
    status: Union[Unset, WorkflowPublicStartTestStatus] = UNSET,

) -> Optional[WorkflowPublicStartTestResponse200]:
    """ Start workflow test activity

     <ul>
      <li>Unit must exist in WATS MES</li>
      <li>Workflow must be initialized on the unit before use (e.g. via Operator Interface or WATS MES
    API) with same status (see 'status' parameter)</li>
      <li>Current activity type in the unit's workflow must equal to 'Test', or else 'false' will be
    returned by the method</li>
    </ul>

    Args:
        serial_number (str):
        part_number (str):
        operator_name (Union[Unset, str]):
        station_name (Union[Unset, str]):
        status (Union[Unset, WorkflowPublicStartTestStatus]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WorkflowPublicStartTestResponse200
     """


    return (await asyncio_detailed(
        client=client,
serial_number=serial_number,
part_number=part_number,
operator_name=operator_name,
station_name=station_name,
status=status,

    )).parsed
