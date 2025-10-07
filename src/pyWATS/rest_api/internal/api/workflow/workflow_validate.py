from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.workflow_validate_data_body import WorkflowValidateDataBody
from ...models.workflow_validate_json_body import WorkflowValidateJsonBody
from ...models.workflow_validate_method import WorkflowValidateMethod
from ...models.workflow_validate_response_200 import WorkflowValidateResponse200
from ...models.workflow_validate_status import WorkflowValidateStatus
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    body: Union[
        WorkflowValidateJsonBody,
        WorkflowValidateDataBody,
    ],
    serial_number: str,
    part_number: str,
    method: WorkflowValidateMethod,
    name: str,
    status: Union[Unset, WorkflowValidateStatus] = UNSET,
    generate_image: Union[Unset, bool] = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["SerialNumber"] = serial_number

    params["PartNumber"] = part_number

    json_method = method.value
    params["Method"] = json_method

    params["Name"] = name

    json_status: Union[Unset, int] = UNSET
    if not isinstance(status, Unset):
        json_status = status.value

    params["Status"] = json_status

    params["GenerateImage"] = generate_image


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/Workflow/Validate",
        "params": params,
    }

    if isinstance(body, WorkflowValidateJsonBody):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, WorkflowValidateDataBody):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[WorkflowValidateResponse200]:
    if response.status_code == 200:
        response_200 = WorkflowValidateResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[WorkflowValidateResponse200]:
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
        WorkflowValidateJsonBody,
        WorkflowValidateDataBody,
    ],
    serial_number: str,
    part_number: str,
    method: WorkflowValidateMethod,
    name: str,
    status: Union[Unset, WorkflowValidateStatus] = UNSET,
    generate_image: Union[Unset, bool] = UNSET,

) -> Response[WorkflowValidateResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        method (WorkflowValidateMethod):
        name (str):
        status (Union[Unset, WorkflowValidateStatus]):
        generate_image (Union[Unset, bool]):
        body (WorkflowValidateJsonBody):
        body (WorkflowValidateDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WorkflowValidateResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
serial_number=serial_number,
part_number=part_number,
method=method,
name=name,
status=status,
generate_image=generate_image,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        WorkflowValidateJsonBody,
        WorkflowValidateDataBody,
    ],
    serial_number: str,
    part_number: str,
    method: WorkflowValidateMethod,
    name: str,
    status: Union[Unset, WorkflowValidateStatus] = UNSET,
    generate_image: Union[Unset, bool] = UNSET,

) -> Optional[WorkflowValidateResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        method (WorkflowValidateMethod):
        name (str):
        status (Union[Unset, WorkflowValidateStatus]):
        generate_image (Union[Unset, bool]):
        body (WorkflowValidateJsonBody):
        body (WorkflowValidateDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WorkflowValidateResponse200
     """


    return sync_detailed(
        client=client,
body=body,
serial_number=serial_number,
part_number=part_number,
method=method,
name=name,
status=status,
generate_image=generate_image,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        WorkflowValidateJsonBody,
        WorkflowValidateDataBody,
    ],
    serial_number: str,
    part_number: str,
    method: WorkflowValidateMethod,
    name: str,
    status: Union[Unset, WorkflowValidateStatus] = UNSET,
    generate_image: Union[Unset, bool] = UNSET,

) -> Response[WorkflowValidateResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        method (WorkflowValidateMethod):
        name (str):
        status (Union[Unset, WorkflowValidateStatus]):
        generate_image (Union[Unset, bool]):
        body (WorkflowValidateJsonBody):
        body (WorkflowValidateDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WorkflowValidateResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
serial_number=serial_number,
part_number=part_number,
method=method,
name=name,
status=status,
generate_image=generate_image,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        WorkflowValidateJsonBody,
        WorkflowValidateDataBody,
    ],
    serial_number: str,
    part_number: str,
    method: WorkflowValidateMethod,
    name: str,
    status: Union[Unset, WorkflowValidateStatus] = UNSET,
    generate_image: Union[Unset, bool] = UNSET,

) -> Optional[WorkflowValidateResponse200]:
    """ 
    Args:
        serial_number (str):
        part_number (str):
        method (WorkflowValidateMethod):
        name (str):
        status (Union[Unset, WorkflowValidateStatus]):
        generate_image (Union[Unset, bool]):
        body (WorkflowValidateJsonBody):
        body (WorkflowValidateDataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WorkflowValidateResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
serial_number=serial_number,
part_number=part_number,
method=method,
name=name,
status=status,
generate_image=generate_image,

    )).parsed
