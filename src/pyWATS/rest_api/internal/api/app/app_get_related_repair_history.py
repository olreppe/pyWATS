from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.app_get_related_repair_history_response_200 import AppGetRelatedRepairHistoryResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    part_number: str,
    revision: str,
    repair_operation_code: Union[Unset, str] = UNSET,
    test_operation_code: Union[Unset, str] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["partNumber"] = part_number

    params["revision"] = revision

    params["repairOperationCode"] = repair_operation_code

    params["testOperationCode"] = test_operation_code


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/App/RelatedRepairHistory",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[AppGetRelatedRepairHistoryResponse200]:
    if response.status_code == 200:
        response_200 = AppGetRelatedRepairHistoryResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[AppGetRelatedRepairHistoryResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    part_number: str,
    revision: str,
    repair_operation_code: Union[Unset, str] = UNSET,
    test_operation_code: Union[Unset, str] = UNSET,

) -> Response[AppGetRelatedRepairHistoryResponse200]:
    """ Get list of repaired failures related to the part number and revision.

    Args:
        part_number (str):
        revision (str):
        repair_operation_code (Union[Unset, str]):
        test_operation_code (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AppGetRelatedRepairHistoryResponse200]
     """


    kwargs = _get_kwargs(
        part_number=part_number,
revision=revision,
repair_operation_code=repair_operation_code,
test_operation_code=test_operation_code,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    part_number: str,
    revision: str,
    repair_operation_code: Union[Unset, str] = UNSET,
    test_operation_code: Union[Unset, str] = UNSET,

) -> Optional[AppGetRelatedRepairHistoryResponse200]:
    """ Get list of repaired failures related to the part number and revision.

    Args:
        part_number (str):
        revision (str):
        repair_operation_code (Union[Unset, str]):
        test_operation_code (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AppGetRelatedRepairHistoryResponse200
     """


    return sync_detailed(
        client=client,
part_number=part_number,
revision=revision,
repair_operation_code=repair_operation_code,
test_operation_code=test_operation_code,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    part_number: str,
    revision: str,
    repair_operation_code: Union[Unset, str] = UNSET,
    test_operation_code: Union[Unset, str] = UNSET,

) -> Response[AppGetRelatedRepairHistoryResponse200]:
    """ Get list of repaired failures related to the part number and revision.

    Args:
        part_number (str):
        revision (str):
        repair_operation_code (Union[Unset, str]):
        test_operation_code (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AppGetRelatedRepairHistoryResponse200]
     """


    kwargs = _get_kwargs(
        part_number=part_number,
revision=revision,
repair_operation_code=repair_operation_code,
test_operation_code=test_operation_code,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    part_number: str,
    revision: str,
    repair_operation_code: Union[Unset, str] = UNSET,
    test_operation_code: Union[Unset, str] = UNSET,

) -> Optional[AppGetRelatedRepairHistoryResponse200]:
    """ Get list of repaired failures related to the part number and revision.

    Args:
        part_number (str):
        revision (str):
        repair_operation_code (Union[Unset, str]):
        test_operation_code (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AppGetRelatedRepairHistoryResponse200
     """


    return (await asyncio_detailed(
        client=client,
part_number=part_number,
revision=revision,
repair_operation_code=repair_operation_code,
test_operation_code=test_operation_code,

    )).parsed
