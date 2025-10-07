from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmWidget")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmWidget:
    """ 
        Attributes:
            widget_id (Union[Unset, int]):
            widget_type (Union[Unset, int]): Reference to the widget type. Data defined in angular module
            dashboard_id (Union[Unset, int]): The dashboard this widget belongs to
            x_position (Union[Unset, int]): Horizontal position in grid
            y_position (Union[Unset, int]): Vertical position in grid
            width (Union[Unset, int]): Width in number of grid squares
            height (Union[Unset, int]): Height in number of grid squares
            filter_ (Union[Unset, str]): JSON representation of the WATS filter
            period_type (Union[Unset, int]): The type of period used to determine the from and to dates of the widgets data
                range in time.
            common_settings (Union[Unset, str]): Settings for widget
            settings (Union[Unset, str]): Settings for widget (unique for widget type)
            instance_data (Union[Unset, str]): Custom widget settings
            to_be_added (Union[Unset, bool]): Determines if the widget is only partially created because it was added from
                another part of wats instead of inside the dashboard
     """

    widget_id: Union[Unset, int] = UNSET
    widget_type: Union[Unset, int] = UNSET
    dashboard_id: Union[Unset, int] = UNSET
    x_position: Union[Unset, int] = UNSET
    y_position: Union[Unset, int] = UNSET
    width: Union[Unset, int] = UNSET
    height: Union[Unset, int] = UNSET
    filter_: Union[Unset, str] = UNSET
    period_type: Union[Unset, int] = UNSET
    common_settings: Union[Unset, str] = UNSET
    settings: Union[Unset, str] = UNSET
    instance_data: Union[Unset, str] = UNSET
    to_be_added: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        widget_id = self.widget_id

        widget_type = self.widget_type

        dashboard_id = self.dashboard_id

        x_position = self.x_position

        y_position = self.y_position

        width = self.width

        height = self.height

        filter_ = self.filter_

        period_type = self.period_type

        common_settings = self.common_settings

        settings = self.settings

        instance_data = self.instance_data

        to_be_added = self.to_be_added


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if widget_id is not UNSET:
            field_dict["widgetId"] = widget_id
        if widget_type is not UNSET:
            field_dict["widgetType"] = widget_type
        if dashboard_id is not UNSET:
            field_dict["dashboardId"] = dashboard_id
        if x_position is not UNSET:
            field_dict["xPosition"] = x_position
        if y_position is not UNSET:
            field_dict["yPosition"] = y_position
        if width is not UNSET:
            field_dict["width"] = width
        if height is not UNSET:
            field_dict["height"] = height
        if filter_ is not UNSET:
            field_dict["filter"] = filter_
        if period_type is not UNSET:
            field_dict["periodType"] = period_type
        if common_settings is not UNSET:
            field_dict["commonSettings"] = common_settings
        if settings is not UNSET:
            field_dict["settings"] = settings
        if instance_data is not UNSET:
            field_dict["instanceData"] = instance_data
        if to_be_added is not UNSET:
            field_dict["toBeAdded"] = to_be_added

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        widget_id = d.pop("widgetId", UNSET)

        widget_type = d.pop("widgetType", UNSET)

        dashboard_id = d.pop("dashboardId", UNSET)

        x_position = d.pop("xPosition", UNSET)

        y_position = d.pop("yPosition", UNSET)

        width = d.pop("width", UNSET)

        height = d.pop("height", UNSET)

        filter_ = d.pop("filter", UNSET)

        period_type = d.pop("periodType", UNSET)

        common_settings = d.pop("commonSettings", UNSET)

        settings = d.pop("settings", UNSET)

        instance_data = d.pop("instanceData", UNSET)

        to_be_added = d.pop("toBeAdded", UNSET)

        virinco_wats_web_dashboard_models_tdm_widget = cls(
            widget_id=widget_id,
            widget_type=widget_type,
            dashboard_id=dashboard_id,
            x_position=x_position,
            y_position=y_position,
            width=width,
            height=height,
            filter_=filter_,
            period_type=period_type,
            common_settings=common_settings,
            settings=settings,
            instance_data=instance_data,
            to_be_added=to_be_added,
        )


        virinco_wats_web_dashboard_models_tdm_widget.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_widget

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
