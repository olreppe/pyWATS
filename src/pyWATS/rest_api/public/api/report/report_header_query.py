from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.virinco_wats_web_dashboard_models_o_data_report_header import VirincoWATSWebDashboardModelsODataReportHeader
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/Report/Query/Header",
    }


    return _kwargs



def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[list['VirincoWATSWebDashboardModelsODataReportHeader']]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            response_200_item = VirincoWATSWebDashboardModelsODataReportHeader.from_dict(response_200_item_data)



            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[list['VirincoWATSWebDashboardModelsODataReportHeader']]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[list['VirincoWATSWebDashboardModelsODataReportHeader']]:
    """ Returns a list of most recent reports matching the specified filter.

     The Query action supports OData query options for filtering and paging.

    It supports:
    - $filter: string functions, and/or/not logic operators, and eq/ne/gt/ge/lt/le/in comparison
    operators
    - $top: max 10000 (use paging with $skip to get more over multiple queries)
    - $orderby: only start, uuid, serialNumber, and timestamp
    - $skip
    - $select
    - $expand

    It does not support:
    - $filter:  arithmetic, number, and date functions, arithmetic operators and 'has' logic operator
    - $count

    By default top 10 reports are returned and they are ordered by report start date/time (most recent
    first).


    Examples:

    Restrict to a specified part number:

    https://your-server-address/api/report/query/header?$filter=partNumber eq 'XYZ123'


    Top 1 reports ordered by start filtered by a specified serial number and part number:

    https://your-server-address/api/report/query/header?$top=1&amp;$orderby=start
    desc&amp;$filter=serialNumber eq '123-45678' and partNumber eq 'XYZ123'


    Get reports filtered by serial number, with all available expanded data:

    https://your-server-address/api/report/query/header?$filter=serialNumber eq
    'XY123'&amp;$expand=subunits,miscinfo,assets,attachments,uurSubUnits,uurMiscInfo,uurAttachments

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VirincoWATSWebDashboardModelsODataReportHeader']]
     """


    kwargs = _get_kwargs(
        
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[list['VirincoWATSWebDashboardModelsODataReportHeader']]:
    """ Returns a list of most recent reports matching the specified filter.

     The Query action supports OData query options for filtering and paging.

    It supports:
    - $filter: string functions, and/or/not logic operators, and eq/ne/gt/ge/lt/le/in comparison
    operators
    - $top: max 10000 (use paging with $skip to get more over multiple queries)
    - $orderby: only start, uuid, serialNumber, and timestamp
    - $skip
    - $select
    - $expand

    It does not support:
    - $filter:  arithmetic, number, and date functions, arithmetic operators and 'has' logic operator
    - $count

    By default top 10 reports are returned and they are ordered by report start date/time (most recent
    first).


    Examples:

    Restrict to a specified part number:

    https://your-server-address/api/report/query/header?$filter=partNumber eq 'XYZ123'


    Top 1 reports ordered by start filtered by a specified serial number and part number:

    https://your-server-address/api/report/query/header?$top=1&amp;$orderby=start
    desc&amp;$filter=serialNumber eq '123-45678' and partNumber eq 'XYZ123'


    Get reports filtered by serial number, with all available expanded data:

    https://your-server-address/api/report/query/header?$filter=serialNumber eq
    'XY123'&amp;$expand=subunits,miscinfo,assets,attachments,uurSubUnits,uurMiscInfo,uurAttachments

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VirincoWATSWebDashboardModelsODataReportHeader']
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[list['VirincoWATSWebDashboardModelsODataReportHeader']]:
    """ Returns a list of most recent reports matching the specified filter.

     The Query action supports OData query options for filtering and paging.

    It supports:
    - $filter: string functions, and/or/not logic operators, and eq/ne/gt/ge/lt/le/in comparison
    operators
    - $top: max 10000 (use paging with $skip to get more over multiple queries)
    - $orderby: only start, uuid, serialNumber, and timestamp
    - $skip
    - $select
    - $expand

    It does not support:
    - $filter:  arithmetic, number, and date functions, arithmetic operators and 'has' logic operator
    - $count

    By default top 10 reports are returned and they are ordered by report start date/time (most recent
    first).


    Examples:

    Restrict to a specified part number:

    https://your-server-address/api/report/query/header?$filter=partNumber eq 'XYZ123'


    Top 1 reports ordered by start filtered by a specified serial number and part number:

    https://your-server-address/api/report/query/header?$top=1&amp;$orderby=start
    desc&amp;$filter=serialNumber eq '123-45678' and partNumber eq 'XYZ123'


    Get reports filtered by serial number, with all available expanded data:

    https://your-server-address/api/report/query/header?$filter=serialNumber eq
    'XY123'&amp;$expand=subunits,miscinfo,assets,attachments,uurSubUnits,uurMiscInfo,uurAttachments

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['VirincoWATSWebDashboardModelsODataReportHeader']]
     """


    kwargs = _get_kwargs(
        
    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[list['VirincoWATSWebDashboardModelsODataReportHeader']]:
    """ Returns a list of most recent reports matching the specified filter.

     The Query action supports OData query options for filtering and paging.

    It supports:
    - $filter: string functions, and/or/not logic operators, and eq/ne/gt/ge/lt/le/in comparison
    operators
    - $top: max 10000 (use paging with $skip to get more over multiple queries)
    - $orderby: only start, uuid, serialNumber, and timestamp
    - $skip
    - $select
    - $expand

    It does not support:
    - $filter:  arithmetic, number, and date functions, arithmetic operators and 'has' logic operator
    - $count

    By default top 10 reports are returned and they are ordered by report start date/time (most recent
    first).


    Examples:

    Restrict to a specified part number:

    https://your-server-address/api/report/query/header?$filter=partNumber eq 'XYZ123'


    Top 1 reports ordered by start filtered by a specified serial number and part number:

    https://your-server-address/api/report/query/header?$top=1&amp;$orderby=start
    desc&amp;$filter=serialNumber eq '123-45678' and partNumber eq 'XYZ123'


    Get reports filtered by serial number, with all available expanded data:

    https://your-server-address/api/report/query/header?$filter=serialNumber eq
    'XY123'&amp;$expand=subunits,miscinfo,assets,attachments,uurSubUnits,uurMiscInfo,uurAttachments

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['VirincoWATSWebDashboardModelsODataReportHeader']
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
