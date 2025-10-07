from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.virinco_wats_web_dashboard_models_tdm_dashboard_share_data_element_access_control import VirincoWATSWebDashboardModelsTdmDashboardShareDataElementAccessControl
from ..models.virinco_wats_web_dashboard_models_tdm_dashboard_share_data_element_change_type import VirincoWATSWebDashboardModelsTdmDashboardShareDataElementChangeType
from ..models.virinco_wats_web_dashboard_models_tdm_dashboard_share_data_element_share_type import VirincoWATSWebDashboardModelsTdmDashboardShareDataElementShareType
from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Union
import datetime






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmDashboardShareDataElement")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmDashboardShareDataElement:
    """ Data pertaining sharing of a dashboard in order to access another users private dashboards.

        Attributes:
            id (Union[Unset, int]):
            dashboard_id (Union[Unset, int]):
            shared_with_id (Union[Unset, str]):
            share_type (Union[Unset, VirincoWATSWebDashboardModelsTdmDashboardShareDataElementShareType]):
            access_control (Union[Unset, VirincoWATSWebDashboardModelsTdmDashboardShareDataElementAccessControl]):
            created_by (Union[Unset, str]):
            created_on (Union[Unset, datetime.datetime]):
            change_type (Union[Unset, VirincoWATSWebDashboardModelsTdmDashboardShareDataElementChangeType]): The type of
                change made to this subscription, if any
     """

    id: Union[Unset, int] = UNSET
    dashboard_id: Union[Unset, int] = UNSET
    shared_with_id: Union[Unset, str] = UNSET
    share_type: Union[Unset, VirincoWATSWebDashboardModelsTdmDashboardShareDataElementShareType] = UNSET
    access_control: Union[Unset, VirincoWATSWebDashboardModelsTdmDashboardShareDataElementAccessControl] = UNSET
    created_by: Union[Unset, str] = UNSET
    created_on: Union[Unset, datetime.datetime] = UNSET
    change_type: Union[Unset, VirincoWATSWebDashboardModelsTdmDashboardShareDataElementChangeType] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        dashboard_id = self.dashboard_id

        shared_with_id = self.shared_with_id

        share_type: Union[Unset, int] = UNSET
        if not isinstance(self.share_type, Unset):
            share_type = self.share_type.value


        access_control: Union[Unset, int] = UNSET
        if not isinstance(self.access_control, Unset):
            access_control = self.access_control.value


        created_by = self.created_by

        created_on: Union[Unset, str] = UNSET
        if not isinstance(self.created_on, Unset):
            created_on = self.created_on.isoformat()

        change_type: Union[Unset, int] = UNSET
        if not isinstance(self.change_type, Unset):
            change_type = self.change_type.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if dashboard_id is not UNSET:
            field_dict["dashboardId"] = dashboard_id
        if shared_with_id is not UNSET:
            field_dict["sharedWithId"] = shared_with_id
        if share_type is not UNSET:
            field_dict["shareType"] = share_type
        if access_control is not UNSET:
            field_dict["accessControl"] = access_control
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if created_on is not UNSET:
            field_dict["createdOn"] = created_on
        if change_type is not UNSET:
            field_dict["changeType"] = change_type

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        dashboard_id = d.pop("dashboardId", UNSET)

        shared_with_id = d.pop("sharedWithId", UNSET)

        _share_type = d.pop("shareType", UNSET)
        share_type: Union[Unset, VirincoWATSWebDashboardModelsTdmDashboardShareDataElementShareType]
        if isinstance(_share_type,  Unset):
            share_type = UNSET
        else:
            share_type = VirincoWATSWebDashboardModelsTdmDashboardShareDataElementShareType(_share_type)




        _access_control = d.pop("accessControl", UNSET)
        access_control: Union[Unset, VirincoWATSWebDashboardModelsTdmDashboardShareDataElementAccessControl]
        if isinstance(_access_control,  Unset):
            access_control = UNSET
        else:
            access_control = VirincoWATSWebDashboardModelsTdmDashboardShareDataElementAccessControl(_access_control)




        created_by = d.pop("createdBy", UNSET)

        _created_on = d.pop("createdOn", UNSET)
        created_on: Union[Unset, datetime.datetime]
        if isinstance(_created_on,  Unset):
            created_on = UNSET
        else:
            created_on = isoparse(_created_on)




        _change_type = d.pop("changeType", UNSET)
        change_type: Union[Unset, VirincoWATSWebDashboardModelsTdmDashboardShareDataElementChangeType]
        if isinstance(_change_type,  Unset):
            change_type = UNSET
        else:
            change_type = VirincoWATSWebDashboardModelsTdmDashboardShareDataElementChangeType(_change_type)




        virinco_wats_web_dashboard_models_tdm_dashboard_share_data_element = cls(
            id=id,
            dashboard_id=dashboard_id,
            shared_with_id=shared_with_id,
            share_type=share_type,
            access_control=access_control,
            created_by=created_by,
            created_on=created_on,
            change_type=change_type,
        )


        virinco_wats_web_dashboard_models_tdm_dashboard_share_data_element.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_dashboard_share_data_element

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
