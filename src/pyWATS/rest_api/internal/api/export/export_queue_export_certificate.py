from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.export_queue_export_certificate_response_200 import ExportQueueExportCertificateResponse200
from ...models.virinco_wats_web_dashboard_controllers_api_app_public_wats_filter import VirincoWATSWebDashboardControllersApiAppPublicWatsFilter
from ...types import UNSET, Unset
from typing import cast
from typing import Union



def _get_kwargs(
    *,
    body: Union[
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
    ],
    header_data_only: bool,
    as_individual_files: bool,
    dimensions: Union[Unset, str] = UNSET,
    numeric_format: Union[Unset, str] = UNSET,
    body_footer_tag: Union[Unset, str] = UNSET,
    document_footer_tag: Union[Unset, str] = UNSET,
    email: Union[Unset, str] = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["headerDataOnly"] = header_data_only

    params["asIndividualFiles"] = as_individual_files

    params["dimensions"] = dimensions

    params["numericFormat"] = numeric_format

    params["bodyFooterTag"] = body_footer_tag

    params["documentFooterTag"] = document_footer_tag

    params["email"] = email


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/Export/Certificate",
        "params": params,
    }

    if isinstance(body, VirincoWATSWebDashboardControllersApiAppPublicWatsFilter):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/json"
    if isinstance(body, VirincoWATSWebDashboardControllersApiAppPublicWatsFilter):
        _kwargs["data"] = body.to_dict()

        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if isinstance(body, VirincoWATSWebDashboardControllersApiAppPublicWatsFilter):
        _kwargs["json"] = body.to_dict()


        headers["Content-Type"] = "application/scim+json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[ExportQueueExportCertificateResponse200]:
    if response.status_code == 200:
        response_200 = ExportQueueExportCertificateResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[ExportQueueExportCertificateResponse200]:
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
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
    ],
    header_data_only: bool,
    as_individual_files: bool,
    dimensions: Union[Unset, str] = UNSET,
    numeric_format: Union[Unset, str] = UNSET,
    body_footer_tag: Union[Unset, str] = UNSET,
    document_footer_tag: Union[Unset, str] = UNSET,
    email: Union[Unset, str] = UNSET,

) -> Response[ExportQueueExportCertificateResponse200]:
    """ Queue a background export job exporting UUT certificates.

    You will receive an email with a download link when the export is done. When using a token to
    authenticate, the export has to be downloaded by the same token. The link in the email will only
    work for the user or token that queued the export.

    Alternatively, you can periodically poll GET api/Export/List and wait for the returned
    exportFileName to be in the list, then download the zip from GET api/Export/{filename}.

    Args:
        header_data_only (bool):
        as_individual_files (bool):
        dimensions (Union[Unset, str]):
        numeric_format (Union[Unset, str]):
        body_footer_tag (Union[Unset, str]):
        document_footer_tag (Union[Unset, str]):
        email (Union[Unset, str]):
        body (VirincoWATSWebDashboardControllersApiAppPublicWatsFilter): Wats filter exposed in
            rest API
        body (VirincoWATSWebDashboardControllersApiAppPublicWatsFilter): Wats filter exposed in
            rest API
        body (VirincoWATSWebDashboardControllersApiAppPublicWatsFilter): Wats filter exposed in
            rest API

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExportQueueExportCertificateResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
header_data_only=header_data_only,
as_individual_files=as_individual_files,
dimensions=dimensions,
numeric_format=numeric_format,
body_footer_tag=body_footer_tag,
document_footer_tag=document_footer_tag,
email=email,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
    ],
    header_data_only: bool,
    as_individual_files: bool,
    dimensions: Union[Unset, str] = UNSET,
    numeric_format: Union[Unset, str] = UNSET,
    body_footer_tag: Union[Unset, str] = UNSET,
    document_footer_tag: Union[Unset, str] = UNSET,
    email: Union[Unset, str] = UNSET,

) -> Optional[ExportQueueExportCertificateResponse200]:
    """ Queue a background export job exporting UUT certificates.

    You will receive an email with a download link when the export is done. When using a token to
    authenticate, the export has to be downloaded by the same token. The link in the email will only
    work for the user or token that queued the export.

    Alternatively, you can periodically poll GET api/Export/List and wait for the returned
    exportFileName to be in the list, then download the zip from GET api/Export/{filename}.

    Args:
        header_data_only (bool):
        as_individual_files (bool):
        dimensions (Union[Unset, str]):
        numeric_format (Union[Unset, str]):
        body_footer_tag (Union[Unset, str]):
        document_footer_tag (Union[Unset, str]):
        email (Union[Unset, str]):
        body (VirincoWATSWebDashboardControllersApiAppPublicWatsFilter): Wats filter exposed in
            rest API
        body (VirincoWATSWebDashboardControllersApiAppPublicWatsFilter): Wats filter exposed in
            rest API
        body (VirincoWATSWebDashboardControllersApiAppPublicWatsFilter): Wats filter exposed in
            rest API

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExportQueueExportCertificateResponse200
     """


    return sync_detailed(
        client=client,
body=body,
header_data_only=header_data_only,
as_individual_files=as_individual_files,
dimensions=dimensions,
numeric_format=numeric_format,
body_footer_tag=body_footer_tag,
document_footer_tag=document_footer_tag,
email=email,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
    ],
    header_data_only: bool,
    as_individual_files: bool,
    dimensions: Union[Unset, str] = UNSET,
    numeric_format: Union[Unset, str] = UNSET,
    body_footer_tag: Union[Unset, str] = UNSET,
    document_footer_tag: Union[Unset, str] = UNSET,
    email: Union[Unset, str] = UNSET,

) -> Response[ExportQueueExportCertificateResponse200]:
    """ Queue a background export job exporting UUT certificates.

    You will receive an email with a download link when the export is done. When using a token to
    authenticate, the export has to be downloaded by the same token. The link in the email will only
    work for the user or token that queued the export.

    Alternatively, you can periodically poll GET api/Export/List and wait for the returned
    exportFileName to be in the list, then download the zip from GET api/Export/{filename}.

    Args:
        header_data_only (bool):
        as_individual_files (bool):
        dimensions (Union[Unset, str]):
        numeric_format (Union[Unset, str]):
        body_footer_tag (Union[Unset, str]):
        document_footer_tag (Union[Unset, str]):
        email (Union[Unset, str]):
        body (VirincoWATSWebDashboardControllersApiAppPublicWatsFilter): Wats filter exposed in
            rest API
        body (VirincoWATSWebDashboardControllersApiAppPublicWatsFilter): Wats filter exposed in
            rest API
        body (VirincoWATSWebDashboardControllersApiAppPublicWatsFilter): Wats filter exposed in
            rest API

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ExportQueueExportCertificateResponse200]
     """


    kwargs = _get_kwargs(
        body=body,
header_data_only=header_data_only,
as_individual_files=as_individual_files,
dimensions=dimensions,
numeric_format=numeric_format,
body_footer_tag=body_footer_tag,
document_footer_tag=document_footer_tag,
email=email,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: Union[
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
        VirincoWATSWebDashboardControllersApiAppPublicWatsFilter,
    ],
    header_data_only: bool,
    as_individual_files: bool,
    dimensions: Union[Unset, str] = UNSET,
    numeric_format: Union[Unset, str] = UNSET,
    body_footer_tag: Union[Unset, str] = UNSET,
    document_footer_tag: Union[Unset, str] = UNSET,
    email: Union[Unset, str] = UNSET,

) -> Optional[ExportQueueExportCertificateResponse200]:
    """ Queue a background export job exporting UUT certificates.

    You will receive an email with a download link when the export is done. When using a token to
    authenticate, the export has to be downloaded by the same token. The link in the email will only
    work for the user or token that queued the export.

    Alternatively, you can periodically poll GET api/Export/List and wait for the returned
    exportFileName to be in the list, then download the zip from GET api/Export/{filename}.

    Args:
        header_data_only (bool):
        as_individual_files (bool):
        dimensions (Union[Unset, str]):
        numeric_format (Union[Unset, str]):
        body_footer_tag (Union[Unset, str]):
        document_footer_tag (Union[Unset, str]):
        email (Union[Unset, str]):
        body (VirincoWATSWebDashboardControllersApiAppPublicWatsFilter): Wats filter exposed in
            rest API
        body (VirincoWATSWebDashboardControllersApiAppPublicWatsFilter): Wats filter exposed in
            rest API
        body (VirincoWATSWebDashboardControllersApiAppPublicWatsFilter): Wats filter exposed in
            rest API

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ExportQueueExportCertificateResponse200
     """


    return (await asyncio_detailed(
        client=client,
body=body,
header_data_only=header_data_only,
as_individual_files=as_individual_files,
dimensions=dimensions,
numeric_format=numeric_format,
body_footer_tag=body_footer_tag,
document_footer_tag=document_footer_tag,
email=email,

    )).parsed
