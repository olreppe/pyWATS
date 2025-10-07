from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.product_selection_post_kpi_target_response_200 import ProductSelectionPostKpiTargetResponse200
from ...models.virinco_wats_web_dashboard_models_tdm_kpi_target import VirincoWATSWebDashboardModelsTdmKpiTarget
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        VirincoWATSWebDashboardModelsTdmKpiTarget,
        VirincoWATSWebDashboardModelsTdmKpiTarget,
        VirincoWATSWebDashboardModelsTdmKpiTarget,
    ],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/internal/ProductSelection/PostKpiTarget",
    }

    if isinstance(body, VirincoWATSWebDashboardModelsTdmKpiTarget):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, VirincoWATSWebDashboardModelsTdmKpiTarget):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, VirincoWATSWebDashboardModelsTdmKpiTarget):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ProductSelectionPostKpiTargetResponse200]:
    if response.status_code == 200:
        response_200 = ProductSelectionPostKpiTargetResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ProductSelectionPostKpiTargetResponse200]:
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
        VirincoWATSWebDashboardModelsTdmKpiTarget,
        VirincoWATSWebDashboardModelsTdmKpiTarget,
        VirincoWATSWebDashboardModelsTdmKpiTarget,
    ],

) -> Response[ProductSelectionPostKpiTargetResponse200]:
    """ 
    Args:
        body (VirincoWATSWebDashboardModelsTdmKpiTarget):
        body (VirincoWATSWebDashboardModelsTdmKpiTarget):
        body (VirincoWATSWebDashboardModelsTdmKpiTarget):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductSelectionPostKpiTargetResponse200]
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
        VirincoWATSWebDashboardModelsTdmKpiTarget,
        VirincoWATSWebDashboardModelsTdmKpiTarget,
        VirincoWATSWebDashboardModelsTdmKpiTarget,
    ],

) -> Optional[ProductSelectionPostKpiTargetResponse200]:
    """ 
    Args:
        body (VirincoWATSWebDashboardModelsTdmKpiTarget):
        body (VirincoWATSWebDashboardModelsTdmKpiTarget):
        body (VirincoWATSWebDashboardModelsTdmKpiTarget):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductSelectionPostKpiTargetResponse200
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsTdmKpiTarget,
        VirincoWATSWebDashboardModelsTdmKpiTarget,
        VirincoWATSWebDashboardModelsTdmKpiTarget,
    ],

) -> Response[ProductSelectionPostKpiTargetResponse200]:
    """ 
    Args:
        body (VirincoWATSWebDashboardModelsTdmKpiTarget):
        body (VirincoWATSWebDashboardModelsTdmKpiTarget):
        body (VirincoWATSWebDashboardModelsTdmKpiTarget):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ProductSelectionPostKpiTargetResponse200]
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
        VirincoWATSWebDashboardModelsTdmKpiTarget,
        VirincoWATSWebDashboardModelsTdmKpiTarget,
        VirincoWATSWebDashboardModelsTdmKpiTarget,
    ],

) -> Optional[ProductSelectionPostKpiTargetResponse200]:
    """ 
    Args:
        body (VirincoWATSWebDashboardModelsTdmKpiTarget):
        body (VirincoWATSWebDashboardModelsTdmKpiTarget):
        body (VirincoWATSWebDashboardModelsTdmKpiTarget):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ProductSelectionPostKpiTargetResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
