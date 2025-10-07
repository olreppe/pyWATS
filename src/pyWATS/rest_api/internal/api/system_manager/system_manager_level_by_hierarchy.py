from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.system_manager_level_by_hierarchy_response_200 import SystemManagerLevelByHierarchyResponse200
from typing import cast



def _get_kwargs(
    *,
    hierarchy: list[str],

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_hierarchy = hierarchy


    params["hierarchy"] = json_hierarchy


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/SystemManager/Level",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[SystemManagerLevelByHierarchyResponse200]:
    if response.status_code == 200:
        response_200 = SystemManagerLevelByHierarchyResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[SystemManagerLevelByHierarchyResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    hierarchy: list[str],

) -> Response[SystemManagerLevelByHierarchyResponse200]:
    """ Get level by hierarchy.
    Each element in sequence must map to a level in the system manager hierarchy.
    Topmost level specified in first position.

    Returns: Leaf-level's id or null if the hierarchy is missing.

    Please note: this endpoint doesn't work for level restricted users.

    Args:
        hierarchy (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SystemManagerLevelByHierarchyResponse200]
     """


    kwargs = _get_kwargs(
        hierarchy=hierarchy,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    hierarchy: list[str],

) -> Optional[SystemManagerLevelByHierarchyResponse200]:
    """ Get level by hierarchy.
    Each element in sequence must map to a level in the system manager hierarchy.
    Topmost level specified in first position.

    Returns: Leaf-level's id or null if the hierarchy is missing.

    Please note: this endpoint doesn't work for level restricted users.

    Args:
        hierarchy (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SystemManagerLevelByHierarchyResponse200
     """


    return sync_detailed(
        client=client,
hierarchy=hierarchy,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    hierarchy: list[str],

) -> Response[SystemManagerLevelByHierarchyResponse200]:
    """ Get level by hierarchy.
    Each element in sequence must map to a level in the system manager hierarchy.
    Topmost level specified in first position.

    Returns: Leaf-level's id or null if the hierarchy is missing.

    Please note: this endpoint doesn't work for level restricted users.

    Args:
        hierarchy (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SystemManagerLevelByHierarchyResponse200]
     """


    kwargs = _get_kwargs(
        hierarchy=hierarchy,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    hierarchy: list[str],

) -> Optional[SystemManagerLevelByHierarchyResponse200]:
    """ Get level by hierarchy.
    Each element in sequence must map to a level in the system manager hierarchy.
    Topmost level specified in first position.

    Returns: Leaf-level's id or null if the hierarchy is missing.

    Please note: this endpoint doesn't work for level restricted users.

    Args:
        hierarchy (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SystemManagerLevelByHierarchyResponse200
     """


    return (await asyncio_detailed(
        client=client,
hierarchy=hierarchy,

    )).parsed
