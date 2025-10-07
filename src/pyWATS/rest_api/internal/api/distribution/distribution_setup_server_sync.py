from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.distribution_setup_server_sync_response_200 import DistributionSetupServerSyncResponse200
from ...models.virinco_wats_web_dashboard_models_mes_distribution_config import VirincoWATSWebDashboardModelsMesDistributionConfig
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        VirincoWATSWebDashboardModelsMesDistributionConfig,
        VirincoWATSWebDashboardModelsMesDistributionConfig,
        VirincoWATSWebDashboardModelsMesDistributionConfig,
    ],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/internal/Distribution/Setup",
    }

    if isinstance(body, VirincoWATSWebDashboardModelsMesDistributionConfig):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, VirincoWATSWebDashboardModelsMesDistributionConfig):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, VirincoWATSWebDashboardModelsMesDistributionConfig):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[DistributionSetupServerSyncResponse200]:
    if response.status_code == 200:
        response_200 = DistributionSetupServerSyncResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[DistributionSetupServerSyncResponse200]:
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
        VirincoWATSWebDashboardModelsMesDistributionConfig,
        VirincoWATSWebDashboardModelsMesDistributionConfig,
        VirincoWATSWebDashboardModelsMesDistributionConfig,
    ],

) -> Response[DistributionSetupServerSyncResponse200]:
    """ Needs to be called on all servers involved in the sync.

    The server needs to know its own site code, and if it is a source server or involved in two way sync
    (unit sync), it needs to know the destination servers' site codes.

    The server needs to know if it wins or loses a change conflict (unit sync).

    The server needs to know for which tables to log changes. Client, report, repository files, and unit
    process phase change sync does not log changes.

    Logging changes starts after Setup has been run; InitializeSync will log changes for the existing
    data.

    In addition to calling this method, a token with LocalServer permission is required, and transfer
    rules must be created for report transfer.

    Args:
        body (VirincoWATSWebDashboardModelsMesDistributionConfig):
        body (VirincoWATSWebDashboardModelsMesDistributionConfig):
        body (VirincoWATSWebDashboardModelsMesDistributionConfig):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DistributionSetupServerSyncResponse200]
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
    body: Union[
        VirincoWATSWebDashboardModelsMesDistributionConfig,
        VirincoWATSWebDashboardModelsMesDistributionConfig,
        VirincoWATSWebDashboardModelsMesDistributionConfig,
    ],

) -> Optional[DistributionSetupServerSyncResponse200]:
    """ Needs to be called on all servers involved in the sync.

    The server needs to know its own site code, and if it is a source server or involved in two way sync
    (unit sync), it needs to know the destination servers' site codes.

    The server needs to know if it wins or loses a change conflict (unit sync).

    The server needs to know for which tables to log changes. Client, report, repository files, and unit
    process phase change sync does not log changes.

    Logging changes starts after Setup has been run; InitializeSync will log changes for the existing
    data.

    In addition to calling this method, a token with LocalServer permission is required, and transfer
    rules must be created for report transfer.

    Args:
        body (VirincoWATSWebDashboardModelsMesDistributionConfig):
        body (VirincoWATSWebDashboardModelsMesDistributionConfig):
        body (VirincoWATSWebDashboardModelsMesDistributionConfig):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DistributionSetupServerSyncResponse200
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsMesDistributionConfig,
        VirincoWATSWebDashboardModelsMesDistributionConfig,
        VirincoWATSWebDashboardModelsMesDistributionConfig,
    ],

) -> Response[DistributionSetupServerSyncResponse200]:
    """ Needs to be called on all servers involved in the sync.

    The server needs to know its own site code, and if it is a source server or involved in two way sync
    (unit sync), it needs to know the destination servers' site codes.

    The server needs to know if it wins or loses a change conflict (unit sync).

    The server needs to know for which tables to log changes. Client, report, repository files, and unit
    process phase change sync does not log changes.

    Logging changes starts after Setup has been run; InitializeSync will log changes for the existing
    data.

    In addition to calling this method, a token with LocalServer permission is required, and transfer
    rules must be created for report transfer.

    Args:
        body (VirincoWATSWebDashboardModelsMesDistributionConfig):
        body (VirincoWATSWebDashboardModelsMesDistributionConfig):
        body (VirincoWATSWebDashboardModelsMesDistributionConfig):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DistributionSetupServerSyncResponse200]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsMesDistributionConfig,
        VirincoWATSWebDashboardModelsMesDistributionConfig,
        VirincoWATSWebDashboardModelsMesDistributionConfig,
    ],

) -> Optional[DistributionSetupServerSyncResponse200]:
    """ Needs to be called on all servers involved in the sync.

    The server needs to know its own site code, and if it is a source server or involved in two way sync
    (unit sync), it needs to know the destination servers' site codes.

    The server needs to know if it wins or loses a change conflict (unit sync).

    The server needs to know for which tables to log changes. Client, report, repository files, and unit
    process phase change sync does not log changes.

    Logging changes starts after Setup has been run; InitializeSync will log changes for the existing
    data.

    In addition to calling this method, a token with LocalServer permission is required, and transfer
    rules must be created for report transfer.

    Args:
        body (VirincoWATSWebDashboardModelsMesDistributionConfig):
        body (VirincoWATSWebDashboardModelsMesDistributionConfig):
        body (VirincoWATSWebDashboardModelsMesDistributionConfig):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DistributionSetupServerSyncResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
