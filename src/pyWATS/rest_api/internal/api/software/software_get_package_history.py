from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.software_get_package_history_status import SoftwareGetPackageHistoryStatus
from ...models.virinco_wats_web_dashboard_models_mes_software_package import VirincoWATSWebDashboardModelsMesSoftwarePackage
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    tags: str,
    status: Union[Unset, SoftwareGetPackageHistoryStatus] = UNSET,
    all_versions: Union[Unset, bool] = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["tags"] = tags

    json_status: Union[Unset, int] = UNSET
    if not isinstance(status, Unset):
        json_status = status.value

    params["status"] = json_status

    params["allVersions"] = all_versions


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/internal/Software/GetPackageHistory",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[list['VirincoWATSWebDashboardModelsMesSoftwarePackage']]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            response_200_item = VirincoWATSWebDashboardModelsMesSoftwarePackage.from_dict(response_200_item_data)



            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[list['VirincoWATSWebDashboardModelsMesSoftwarePackage']]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    tags: str,
    status: Union[Unset, SoftwareGetPackageHistoryStatus] = UNSET,
    all_versions: Union[Unset, bool] = UNSET,

) -> Response[list['VirincoWATSWebDashboardModelsMesSoftwarePackage']]:
    """ Get list of packages with matching tag

    Args:
        tags (str):
        status (Union[Unset, SoftwareGetPackageHistoryStatus]):
        all_versions (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VirincoWATSWebDashboardModelsMesSoftwarePackage']]
     """


    kwargs = _get_kwargs(
        tags=tags,
status=status,
all_versions=all_versions,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    tags: str,
    status: Union[Unset, SoftwareGetPackageHistoryStatus] = UNSET,
    all_versions: Union[Unset, bool] = UNSET,

) -> Optional[list['VirincoWATSWebDashboardModelsMesSoftwarePackage']]:
    """ Get list of packages with matching tag

    Args:
        tags (str):
        status (Union[Unset, SoftwareGetPackageHistoryStatus]):
        all_versions (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VirincoWATSWebDashboardModelsMesSoftwarePackage']
     """


    return sync_detailed(
        client=client,
tags=tags,
status=status,
all_versions=all_versions,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    tags: str,
    status: Union[Unset, SoftwareGetPackageHistoryStatus] = UNSET,
    all_versions: Union[Unset, bool] = UNSET,

) -> Response[list['VirincoWATSWebDashboardModelsMesSoftwarePackage']]:
    """ Get list of packages with matching tag

    Args:
        tags (str):
        status (Union[Unset, SoftwareGetPackageHistoryStatus]):
        all_versions (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VirincoWATSWebDashboardModelsMesSoftwarePackage']]
     """


    kwargs = _get_kwargs(
        tags=tags,
status=status,
all_versions=all_versions,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    tags: str,
    status: Union[Unset, SoftwareGetPackageHistoryStatus] = UNSET,
    all_versions: Union[Unset, bool] = UNSET,

) -> Optional[list['VirincoWATSWebDashboardModelsMesSoftwarePackage']]:
    """ Get list of packages with matching tag

    Args:
        tags (str):
        status (Union[Unset, SoftwareGetPackageHistoryStatus]):
        all_versions (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VirincoWATSWebDashboardModelsMesSoftwarePackage']
     """


    return (await asyncio_detailed(
        client=client,
tags=tags,
status=status,
all_versions=all_versions,

    )).parsed
