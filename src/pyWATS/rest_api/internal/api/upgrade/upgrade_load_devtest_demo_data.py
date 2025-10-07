from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.upgrade_load_devtest_demo_data_response_200 import UpgradeLoadDevtestDemoDataResponse200
from typing import cast



def _get_kwargs(
    *,
    package: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["package"] = package


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Upgrade/LoadDevtestDemoData",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[UpgradeLoadDevtestDemoDataResponse200]:
    if response.status_code == 200:
        response_200 = UpgradeLoadDevtestDemoDataResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[UpgradeLoadDevtestDemoDataResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    package: str,

) -> Response[UpgradeLoadDevtestDemoDataResponse200]:
    """ Loads demodata package from storage starting from 1 month ago. Meta data must already exist.
    Requires LoadDemoData in cfg.Settings.

    Args:
        package (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpgradeLoadDevtestDemoDataResponse200]
     """


    kwargs = _get_kwargs(
        package=package,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    package: str,

) -> Optional[UpgradeLoadDevtestDemoDataResponse200]:
    """ Loads demodata package from storage starting from 1 month ago. Meta data must already exist.
    Requires LoadDemoData in cfg.Settings.

    Args:
        package (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UpgradeLoadDevtestDemoDataResponse200
     """


    return sync_detailed(
        client=client,
package=package,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    package: str,

) -> Response[UpgradeLoadDevtestDemoDataResponse200]:
    """ Loads demodata package from storage starting from 1 month ago. Meta data must already exist.
    Requires LoadDemoData in cfg.Settings.

    Args:
        package (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UpgradeLoadDevtestDemoDataResponse200]
     """


    kwargs = _get_kwargs(
        package=package,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    package: str,

) -> Optional[UpgradeLoadDevtestDemoDataResponse200]:
    """ Loads demodata package from storage starting from 1 month ago. Meta data must already exist.
    Requires LoadDemoData in cfg.Settings.

    Args:
        package (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UpgradeLoadDevtestDemoDataResponse200
     """


    return (await asyncio_detailed(
        client=client,
package=package,

    )).parsed
