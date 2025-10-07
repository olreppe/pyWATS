from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.upgrade_upgrade_tdm_response_200 import UpgradeUpgradeTDMResponse200
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    old_mes_con_str: Union[Unset, str] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["oldMesConStr"] = old_mes_con_str


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Upgrade/UpgradeTDM",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[UpgradeUpgradeTDMResponse200]:
    if response.status_code == 200:
        response_200 = UpgradeUpgradeTDMResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[UpgradeUpgradeTDMResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    old_mes_con_str: Union[Unset, str] = UNSET,

) -> Response[UpgradeUpgradeTDMResponse200]:
    """ 
    Args:
        old_mes_con_str (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpgradeUpgradeTDMResponse200]
     """


    kwargs = _get_kwargs(
        old_mes_con_str=old_mes_con_str,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    old_mes_con_str: Union[Unset, str] = UNSET,

) -> Optional[UpgradeUpgradeTDMResponse200]:
    """ 
    Args:
        old_mes_con_str (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UpgradeUpgradeTDMResponse200
     """


    return sync_detailed(
        client=client,
old_mes_con_str=old_mes_con_str,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    old_mes_con_str: Union[Unset, str] = UNSET,

) -> Response[UpgradeUpgradeTDMResponse200]:
    """ 
    Args:
        old_mes_con_str (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpgradeUpgradeTDMResponse200]
     """


    kwargs = _get_kwargs(
        old_mes_con_str=old_mes_con_str,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    old_mes_con_str: Union[Unset, str] = UNSET,

) -> Optional[UpgradeUpgradeTDMResponse200]:
    """ 
    Args:
        old_mes_con_str (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UpgradeUpgradeTDMResponse200
     """


    return (await asyncio_detailed(
        client=client,
old_mes_con_str=old_mes_con_str,

    )).parsed
