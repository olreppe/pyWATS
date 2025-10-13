from http import HTTPStatus
from typing import Any, Optional, Union, cast, Dict

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.virinco_wats_models_store_insert_report_result import VirincoWATSModelsStoreInsertReportResult
from typing import cast


def _get_kwargs(
    *,
    body: Dict[str, Any],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/Report/WSJF",
        "json": body,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[VirincoWATSModelsStoreInsertReportResult]:
    if response.status_code == 200:
        response_200 = VirincoWATSModelsStoreInsertReportResult.from_dict(response.json())
        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[VirincoWATSModelsStoreInsertReportResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Dict[str, Any],
) -> Response[VirincoWATSModelsStoreInsertReportResult]:
    """Submit a report in WSJF format
    
    Args:
        body (Dict[str, Any]): The report data in WSJF (WATS Standard JSON Format)
        
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
        
    Returns:
        Response[VirincoWATSModelsStoreInsertReportResult]
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
    body: Dict[str, Any],
) -> Optional[VirincoWATSModelsStoreInsertReportResult]:
    """Submit a report in WSJF format
    
    Args:
        body (Dict[str, Any]): The report data in WSJF (WATS Standard JSON Format)
        
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
        
    Returns:
        VirincoWATSModelsStoreInsertReportResult
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Dict[str, Any],
) -> Response[VirincoWATSModelsStoreInsertReportResult]:
    """Submit a report in WSJF format
    
    Args:
        body (Dict[str, Any]): The report data in WSJF (WATS Standard JSON Format)
        
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
        
    Returns:
        Response[VirincoWATSModelsStoreInsertReportResult]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Dict[str, Any],
) -> Optional[VirincoWATSModelsStoreInsertReportResult]:
    """Submit a report in WSJF format
    
    Args:
        body (Dict[str, Any]): The report data in WSJF (WATS Standard JSON Format)
        
    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.
        
    Returns:
        VirincoWATSModelsStoreInsertReportResult
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
