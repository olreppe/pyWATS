from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_tdm_widget import VirincoWATSWebDashboardModelsTdmWidget





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmDashboard")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmDashboard:
    """ Represents data for a single dashboard.

        Attributes:
            dashboard_id (Union[Unset, int]):
            title (Union[Unset, str]): The title of the dashboard.
            filter_ (Union[Unset, str]): The global filter to apply to the dashboard.
            quick_date_type (Union[Unset, int]): The currently chosen quick date type. The type of chosen quick date forms
                the basis of the from to date of the filter, unless
                the quick date is set to custom, in which case the from and to dates should be used as is.
            parent_folder_id (Union[Unset, UUID]): The folder this dashboard resides in in the menu. Example:
                00000000-0000-0000-0000-000000000000.
            is_public (Union[Unset, bool]): Determines if the dashboard is public or private.
            is_read_only (Union[Unset, bool]): Determines if the dashboard can only be viewed and not edited by this user.
            custom_filter_dates (Union[Unset, str]): The custom date formats defined by the user.
            owner (Union[Unset, str]): The username of the user which created the dashboard.
            create_date (Union[Unset, datetime.datetime]): The date/time when the dashboard was created.
            refresh_interval (Union[Unset, int]): The date/time when the dashboard was created.
            is_default (Union[Unset, bool]): Is this the default dashboard for the user?
            is_hidden (Union[Unset, bool]): Determines if the dashboard is hidden in the menu for the current user.
            is_shared_with_user (Union[Unset, bool]): Determines if the dashboard is shared with the current user. <seealso
                cref="P:Virinco.WATS.Web.Dashboard.Models.Tdm.Dashboard.SharedThroughRole" />
            share_data_id (Union[Unset, int]): If the dashboard is shared with the user this property holds the share data
                id.
            shared_through_role (Union[Unset, str]): If the dashboard is shared with the user through a role, this property
                contains the role name. <seealso cref="P:Virinco.WATS.Web.Dashboard.Models.Tdm.Dashboard.IsSharedWithUser" />
            is_shared_with_anyone (Union[Unset, bool]): Determines if the dashboard is shared with any user or role.
            widgets (Union[Unset, list['VirincoWATSWebDashboardModelsTdmWidget']]): A list of the widgets contained in this
                dashboard.
     """

    dashboard_id: Union[Unset, int] = UNSET
    title: Union[Unset, str] = UNSET
    filter_: Union[Unset, str] = UNSET
    quick_date_type: Union[Unset, int] = UNSET
    parent_folder_id: Union[Unset, UUID] = UNSET
    is_public: Union[Unset, bool] = UNSET
    is_read_only: Union[Unset, bool] = UNSET
    custom_filter_dates: Union[Unset, str] = UNSET
    owner: Union[Unset, str] = UNSET
    create_date: Union[Unset, datetime.datetime] = UNSET
    refresh_interval: Union[Unset, int] = UNSET
    is_default: Union[Unset, bool] = UNSET
    is_hidden: Union[Unset, bool] = UNSET
    is_shared_with_user: Union[Unset, bool] = UNSET
    share_data_id: Union[Unset, int] = UNSET
    shared_through_role: Union[Unset, str] = UNSET
    is_shared_with_anyone: Union[Unset, bool] = UNSET
    widgets: Union[Unset, list['VirincoWATSWebDashboardModelsTdmWidget']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_tdm_widget import VirincoWATSWebDashboardModelsTdmWidget
        dashboard_id = self.dashboard_id

        title = self.title

        filter_ = self.filter_

        quick_date_type = self.quick_date_type

        parent_folder_id: Union[Unset, str] = UNSET
        if not isinstance(self.parent_folder_id, Unset):
            parent_folder_id = str(self.parent_folder_id)

        is_public = self.is_public

        is_read_only = self.is_read_only

        custom_filter_dates = self.custom_filter_dates

        owner = self.owner

        create_date: Union[Unset, str] = UNSET
        if not isinstance(self.create_date, Unset):
            create_date = self.create_date.isoformat()

        refresh_interval = self.refresh_interval

        is_default = self.is_default

        is_hidden = self.is_hidden

        is_shared_with_user = self.is_shared_with_user

        share_data_id = self.share_data_id

        shared_through_role = self.shared_through_role

        is_shared_with_anyone = self.is_shared_with_anyone

        widgets: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.widgets, Unset):
            widgets = []
            for widgets_item_data in self.widgets:
                widgets_item = widgets_item_data.to_dict()
                widgets.append(widgets_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if dashboard_id is not UNSET:
            field_dict["dashboardId"] = dashboard_id
        if title is not UNSET:
            field_dict["title"] = title
        if filter_ is not UNSET:
            field_dict["filter"] = filter_
        if quick_date_type is not UNSET:
            field_dict["quickDateType"] = quick_date_type
        if parent_folder_id is not UNSET:
            field_dict["parentFolderId"] = parent_folder_id
        if is_public is not UNSET:
            field_dict["isPublic"] = is_public
        if is_read_only is not UNSET:
            field_dict["isReadOnly"] = is_read_only
        if custom_filter_dates is not UNSET:
            field_dict["customFilterDates"] = custom_filter_dates
        if owner is not UNSET:
            field_dict["owner"] = owner
        if create_date is not UNSET:
            field_dict["createDate"] = create_date
        if refresh_interval is not UNSET:
            field_dict["refreshInterval"] = refresh_interval
        if is_default is not UNSET:
            field_dict["isDefault"] = is_default
        if is_hidden is not UNSET:
            field_dict["isHidden"] = is_hidden
        if is_shared_with_user is not UNSET:
            field_dict["isSharedWithUser"] = is_shared_with_user
        if share_data_id is not UNSET:
            field_dict["shareDataId"] = share_data_id
        if shared_through_role is not UNSET:
            field_dict["sharedThroughRole"] = shared_through_role
        if is_shared_with_anyone is not UNSET:
            field_dict["isSharedWithAnyone"] = is_shared_with_anyone
        if widgets is not UNSET:
            field_dict["widgets"] = widgets

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_tdm_widget import VirincoWATSWebDashboardModelsTdmWidget
        d = dict(src_dict)
        dashboard_id = d.pop("dashboardId", UNSET)

        title = d.pop("title", UNSET)

        filter_ = d.pop("filter", UNSET)

        quick_date_type = d.pop("quickDateType", UNSET)

        _parent_folder_id = d.pop("parentFolderId", UNSET)
        parent_folder_id: Union[Unset, UUID]
        if isinstance(_parent_folder_id,  Unset):
            parent_folder_id = UNSET
        else:
            parent_folder_id = UUID(_parent_folder_id)




        is_public = d.pop("isPublic", UNSET)

        is_read_only = d.pop("isReadOnly", UNSET)

        custom_filter_dates = d.pop("customFilterDates", UNSET)

        owner = d.pop("owner", UNSET)

        _create_date = d.pop("createDate", UNSET)
        create_date: Union[Unset, datetime.datetime]
        if isinstance(_create_date,  Unset):
            create_date = UNSET
        else:
            create_date = isoparse(_create_date)




        refresh_interval = d.pop("refreshInterval", UNSET)

        is_default = d.pop("isDefault", UNSET)

        is_hidden = d.pop("isHidden", UNSET)

        is_shared_with_user = d.pop("isSharedWithUser", UNSET)

        share_data_id = d.pop("shareDataId", UNSET)

        shared_through_role = d.pop("sharedThroughRole", UNSET)

        is_shared_with_anyone = d.pop("isSharedWithAnyone", UNSET)

        widgets = []
        _widgets = d.pop("widgets", UNSET)
        for widgets_item_data in (_widgets or []):
            widgets_item = VirincoWATSWebDashboardModelsTdmWidget.from_dict(widgets_item_data)



            widgets.append(widgets_item)


        virinco_wats_web_dashboard_models_tdm_dashboard = cls(
            dashboard_id=dashboard_id,
            title=title,
            filter_=filter_,
            quick_date_type=quick_date_type,
            parent_folder_id=parent_folder_id,
            is_public=is_public,
            is_read_only=is_read_only,
            custom_filter_dates=custom_filter_dates,
            owner=owner,
            create_date=create_date,
            refresh_interval=refresh_interval,
            is_default=is_default,
            is_hidden=is_hidden,
            is_shared_with_user=is_shared_with_user,
            share_data_id=share_data_id,
            shared_through_role=shared_through_role,
            is_shared_with_anyone=is_shared_with_anyone,
            widgets=widgets,
        )


        virinco_wats_web_dashboard_models_tdm_dashboard.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_dashboard

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
