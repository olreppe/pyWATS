from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_controllers_api_app_public_wats_filter_date_grouping import VirincoWATSWebDashboardControllersApiAppPublicWatsFilterDateGrouping
from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
import datetime






T = TypeVar("T", bound="VirincoWATSWebDashboardControllersApiAppPublicWatsFilter")



@_attrs_define
class VirincoWATSWebDashboardControllersApiAppPublicWatsFilter:
    """ Wats filter exposed in rest API

        Attributes:
            serial_number (Union[Unset, str]):
            part_number (Union[Unset, str]):
            revision (Union[Unset, str]):
            batch_number (Union[Unset, str]):
            station_name (Union[Unset, str]):
            test_operation (Union[Unset, str]):
            status (Union[Unset, str]):
            yield_ (Union[Unset, int]):
            misc_description (Union[Unset, str]):
            misc_value (Union[Unset, str]):
            product_group (Union[Unset, str]):
            level (Union[Unset, str]):
            sw_filename (Union[Unset, str]):
            sw_version (Union[Unset, str]):
            socket (Union[Unset, str]):
            date_from (Union[Unset, datetime.datetime]):
            date_to (Union[Unset, datetime.datetime]):
            date_grouping (Union[Unset, VirincoWATSWebDashboardControllersApiAppPublicWatsFilterDateGrouping]):
            period_count (Union[Unset, int]):
            include_current_period (Union[Unset, bool]):
            max_count (Union[Unset, int]):
            min_count (Union[Unset, int]):
            top_count (Union[Unset, int]):
            dimensions (Union[Unset, str]):
     """

    serial_number: Union[Unset, str] = UNSET
    part_number: Union[Unset, str] = UNSET
    revision: Union[Unset, str] = UNSET
    batch_number: Union[Unset, str] = UNSET
    station_name: Union[Unset, str] = UNSET
    test_operation: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    yield_: Union[Unset, int] = UNSET
    misc_description: Union[Unset, str] = UNSET
    misc_value: Union[Unset, str] = UNSET
    product_group: Union[Unset, str] = UNSET
    level: Union[Unset, str] = UNSET
    sw_filename: Union[Unset, str] = UNSET
    sw_version: Union[Unset, str] = UNSET
    socket: Union[Unset, str] = UNSET
    date_from: Union[Unset, datetime.datetime] = UNSET
    date_to: Union[Unset, datetime.datetime] = UNSET
    date_grouping: Union[Unset, VirincoWATSWebDashboardControllersApiAppPublicWatsFilterDateGrouping] = UNSET
    period_count: Union[Unset, int] = UNSET
    include_current_period: Union[Unset, bool] = UNSET
    max_count: Union[Unset, int] = UNSET
    min_count: Union[Unset, int] = UNSET
    top_count: Union[Unset, int] = UNSET
    dimensions: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        serial_number = self.serial_number

        part_number = self.part_number

        revision = self.revision

        batch_number = self.batch_number

        station_name = self.station_name

        test_operation = self.test_operation

        status = self.status

        yield_ = self.yield_

        misc_description = self.misc_description

        misc_value = self.misc_value

        product_group = self.product_group

        level = self.level

        sw_filename = self.sw_filename

        sw_version = self.sw_version

        socket = self.socket

        date_from: Union[Unset, str] = UNSET
        if not isinstance(self.date_from, Unset):
            date_from = self.date_from.isoformat()

        date_to: Union[Unset, str] = UNSET
        if not isinstance(self.date_to, Unset):
            date_to = self.date_to.isoformat()

        date_grouping: Union[Unset, int] = UNSET
        if not isinstance(self.date_grouping, Unset):
            date_grouping = self.date_grouping.value


        period_count = self.period_count

        include_current_period = self.include_current_period

        max_count = self.max_count

        min_count = self.min_count

        top_count = self.top_count

        dimensions = self.dimensions


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if serial_number is not UNSET:
            field_dict["serialNumber"] = serial_number
        if part_number is not UNSET:
            field_dict["partNumber"] = part_number
        if revision is not UNSET:
            field_dict["revision"] = revision
        if batch_number is not UNSET:
            field_dict["batchNumber"] = batch_number
        if station_name is not UNSET:
            field_dict["stationName"] = station_name
        if test_operation is not UNSET:
            field_dict["testOperation"] = test_operation
        if status is not UNSET:
            field_dict["status"] = status
        if yield_ is not UNSET:
            field_dict["yield"] = yield_
        if misc_description is not UNSET:
            field_dict["miscDescription"] = misc_description
        if misc_value is not UNSET:
            field_dict["miscValue"] = misc_value
        if product_group is not UNSET:
            field_dict["productGroup"] = product_group
        if level is not UNSET:
            field_dict["level"] = level
        if sw_filename is not UNSET:
            field_dict["swFilename"] = sw_filename
        if sw_version is not UNSET:
            field_dict["swVersion"] = sw_version
        if socket is not UNSET:
            field_dict["socket"] = socket
        if date_from is not UNSET:
            field_dict["dateFrom"] = date_from
        if date_to is not UNSET:
            field_dict["dateTo"] = date_to
        if date_grouping is not UNSET:
            field_dict["dateGrouping"] = date_grouping
        if period_count is not UNSET:
            field_dict["periodCount"] = period_count
        if include_current_period is not UNSET:
            field_dict["includeCurrentPeriod"] = include_current_period
        if max_count is not UNSET:
            field_dict["maxCount"] = max_count
        if min_count is not UNSET:
            field_dict["minCount"] = min_count
        if top_count is not UNSET:
            field_dict["topCount"] = top_count
        if dimensions is not UNSET:
            field_dict["dimensions"] = dimensions

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        serial_number = d.pop("serialNumber", UNSET)

        part_number = d.pop("partNumber", UNSET)

        revision = d.pop("revision", UNSET)

        batch_number = d.pop("batchNumber", UNSET)

        station_name = d.pop("stationName", UNSET)

        test_operation = d.pop("testOperation", UNSET)

        status = d.pop("status", UNSET)

        yield_ = d.pop("yield", UNSET)

        misc_description = d.pop("miscDescription", UNSET)

        misc_value = d.pop("miscValue", UNSET)

        product_group = d.pop("productGroup", UNSET)

        level = d.pop("level", UNSET)

        sw_filename = d.pop("swFilename", UNSET)

        sw_version = d.pop("swVersion", UNSET)

        socket = d.pop("socket", UNSET)

        _date_from = d.pop("dateFrom", UNSET)
        date_from: Union[Unset, datetime.datetime]
        if isinstance(_date_from,  Unset):
            date_from = UNSET
        else:
            date_from = isoparse(_date_from)




        _date_to = d.pop("dateTo", UNSET)
        date_to: Union[Unset, datetime.datetime]
        if isinstance(_date_to,  Unset):
            date_to = UNSET
        else:
            date_to = isoparse(_date_to)




        _date_grouping = d.pop("dateGrouping", UNSET)
        date_grouping: Union[Unset, VirincoWATSWebDashboardControllersApiAppPublicWatsFilterDateGrouping]
        if isinstance(_date_grouping,  Unset):
            date_grouping = UNSET
        else:
            date_grouping = VirincoWATSWebDashboardControllersApiAppPublicWatsFilterDateGrouping(_date_grouping)




        period_count = d.pop("periodCount", UNSET)

        include_current_period = d.pop("includeCurrentPeriod", UNSET)

        max_count = d.pop("maxCount", UNSET)

        min_count = d.pop("minCount", UNSET)

        top_count = d.pop("topCount", UNSET)

        dimensions = d.pop("dimensions", UNSET)

        virinco_wats_web_dashboard_controllers_api_app_public_wats_filter = cls(
            serial_number=serial_number,
            part_number=part_number,
            revision=revision,
            batch_number=batch_number,
            station_name=station_name,
            test_operation=test_operation,
            status=status,
            yield_=yield_,
            misc_description=misc_description,
            misc_value=misc_value,
            product_group=product_group,
            level=level,
            sw_filename=sw_filename,
            sw_version=sw_version,
            socket=socket,
            date_from=date_from,
            date_to=date_to,
            date_grouping=date_grouping,
            period_count=period_count,
            include_current_period=include_current_period,
            max_count=max_count,
            min_count=min_count,
            top_count=top_count,
            dimensions=dimensions,
        )


        virinco_wats_web_dashboard_controllers_api_app_public_wats_filter.additional_properties = d
        return virinco_wats_web_dashboard_controllers_api_app_public_wats_filter

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
