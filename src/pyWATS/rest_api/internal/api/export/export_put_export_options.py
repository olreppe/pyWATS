from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.export_put_export_options_response_200 import ExportPutExportOptionsResponse200
from ...models.virinco_wats_web_dashboard_models_export_wizard_export_options import VirincoWATSWebDashboardModelsExportWizardExportOptions
from typing import cast



def _get_kwargs(
    *,
    body: Union[
        VirincoWATSWebDashboardModelsExportWizardExportOptions,
        VirincoWATSWebDashboardModelsExportWizardExportOptions,
        VirincoWATSWebDashboardModelsExportWizardExportOptions,
    ],

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/internal/Export/Options",
    }

    if isinstance(body, VirincoWATSWebDashboardModelsExportWizardExportOptions):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, VirincoWATSWebDashboardModelsExportWizardExportOptions):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, VirincoWATSWebDashboardModelsExportWizardExportOptions):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ExportPutExportOptionsResponse200]:
    if response.status_code == 200:
        response_200 = ExportPutExportOptionsResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ExportPutExportOptionsResponse200]:
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
        VirincoWATSWebDashboardModelsExportWizardExportOptions,
        VirincoWATSWebDashboardModelsExportWizardExportOptions,
        VirincoWATSWebDashboardModelsExportWizardExportOptions,
    ],

) -> Response[ExportPutExportOptionsResponse200]:
    """ 
    Args:
        body (VirincoWATSWebDashboardModelsExportWizardExportOptions):
        body (VirincoWATSWebDashboardModelsExportWizardExportOptions):
        body (VirincoWATSWebDashboardModelsExportWizardExportOptions):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExportPutExportOptionsResponse200]
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
        VirincoWATSWebDashboardModelsExportWizardExportOptions,
        VirincoWATSWebDashboardModelsExportWizardExportOptions,
        VirincoWATSWebDashboardModelsExportWizardExportOptions,
    ],

) -> Optional[ExportPutExportOptionsResponse200]:
    """ 
    Args:
        body (VirincoWATSWebDashboardModelsExportWizardExportOptions):
        body (VirincoWATSWebDashboardModelsExportWizardExportOptions):
        body (VirincoWATSWebDashboardModelsExportWizardExportOptions):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExportPutExportOptionsResponse200
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardModelsExportWizardExportOptions,
        VirincoWATSWebDashboardModelsExportWizardExportOptions,
        VirincoWATSWebDashboardModelsExportWizardExportOptions,
    ],

) -> Response[ExportPutExportOptionsResponse200]:
    """ 
    Args:
        body (VirincoWATSWebDashboardModelsExportWizardExportOptions):
        body (VirincoWATSWebDashboardModelsExportWizardExportOptions):
        body (VirincoWATSWebDashboardModelsExportWizardExportOptions):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExportPutExportOptionsResponse200]
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
        VirincoWATSWebDashboardModelsExportWizardExportOptions,
        VirincoWATSWebDashboardModelsExportWizardExportOptions,
        VirincoWATSWebDashboardModelsExportWizardExportOptions,
    ],

) -> Optional[ExportPutExportOptionsResponse200]:
    """ 
    Args:
        body (VirincoWATSWebDashboardModelsExportWizardExportOptions):
        body (VirincoWATSWebDashboardModelsExportWizardExportOptions):
        body (VirincoWATSWebDashboardModelsExportWizardExportOptions):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExportPutExportOptionsResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
