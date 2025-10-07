from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.upgrade_create_deployment_script_response_200 import UpgradeCreateDeploymentScriptResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    profile: Union[Unset, str] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["profile"] = profile


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Upgrade/CreateDeploymentScript",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[UpgradeCreateDeploymentScriptResponse200]:
    if response.status_code == 200:
        response_200 = UpgradeCreateDeploymentScriptResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[UpgradeCreateDeploymentScriptResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    profile: Union[Unset, str] = UNSET,

) -> Response[UpgradeCreateDeploymentScriptResponse200]:
    """ profile == migration or dropmissing

    Args:
        profile (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpgradeCreateDeploymentScriptResponse200]
     """


    kwargs = _get_kwargs(
        profile=profile,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    profile: Union[Unset, str] = UNSET,

) -> Optional[UpgradeCreateDeploymentScriptResponse200]:
    """ profile == migration or dropmissing

    Args:
        profile (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UpgradeCreateDeploymentScriptResponse200
     """


    return sync_detailed(
        client=client,
profile=profile,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    profile: Union[Unset, str] = UNSET,

) -> Response[UpgradeCreateDeploymentScriptResponse200]:
    """ profile == migration or dropmissing

    Args:
        profile (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpgradeCreateDeploymentScriptResponse200]
     """


    kwargs = _get_kwargs(
        profile=profile,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    profile: Union[Unset, str] = UNSET,

) -> Optional[UpgradeCreateDeploymentScriptResponse200]:
    """ profile == migration or dropmissing

    Args:
        profile (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UpgradeCreateDeploymentScriptResponse200
     """


    return (await asyncio_detailed(
        client=client,
profile=profile,

    )).parsed
