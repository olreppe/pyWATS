from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_mes_property_set import VirincoWATSWebDashboardModelsMesPropertySet
  from ..models.virinco_wats_web_dashboard_models_mes_property_display_value import VirincoWATSWebDashboardModelsMesPropertyDisplayValue





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesProperty")



@_attrs_define
class VirincoWATSWebDashboardModelsMesProperty:
    """ Model which represents either a software file or folder.

        Attributes:
            property_set (Union[Unset, VirincoWATSWebDashboardModelsMesPropertySet]):
            full_property_path (Union[Unset, str]): The full path of the property.
                example: RunState.Sequence.Main.Numeric Limit Test.Limits.Low
            type_ (Union[Unset, str]): The datatype of the property value, values: String,Boolean,Number
            display_type (Union[Unset, str]): The datatype that must be used when editing the property.
                For example it may be necessary to store a number in a string property
                and by having a Display Type separated from the actual property datatype
                it is possible to ensure that only numbers are entered in the property value editor.
                Currently the following types are supported: values: String,Boolean,Number
            grouping (Union[Unset, str]): Makes it possible to group more than one property as a set of properties that are
                logically connected.
            step_name (Union[Unset, str]): Property StepName
            step_type (Union[Unset, str]): Property StepType
            alias (Union[Unset, str]): Any alias added to the individual properties during the export process.
            full_property_path_key (Union[Unset, str]): internal use (column key)
            value (Union[Unset, str]): The actual value of the property at the time of export. The field can contain any XML
                representation
                of the “Type” field for each property. Data is flattened to XML using Labview standard scheme.
            display_value (Union[Unset, VirincoWATSWebDashboardModelsMesPropertyDisplayValue]):
     """

    property_set: Union[Unset, 'VirincoWATSWebDashboardModelsMesPropertySet'] = UNSET
    full_property_path: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    display_type: Union[Unset, str] = UNSET
    grouping: Union[Unset, str] = UNSET
    step_name: Union[Unset, str] = UNSET
    step_type: Union[Unset, str] = UNSET
    alias: Union[Unset, str] = UNSET
    full_property_path_key: Union[Unset, str] = UNSET
    value: Union[Unset, str] = UNSET
    display_value: Union[Unset, 'VirincoWATSWebDashboardModelsMesPropertyDisplayValue'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_property_set import VirincoWATSWebDashboardModelsMesPropertySet
        from ..models.virinco_wats_web_dashboard_models_mes_property_display_value import VirincoWATSWebDashboardModelsMesPropertyDisplayValue
        property_set: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.property_set, Unset):
            property_set = self.property_set.to_dict()

        full_property_path = self.full_property_path

        type_ = self.type_

        display_type = self.display_type

        grouping = self.grouping

        step_name = self.step_name

        step_type = self.step_type

        alias = self.alias

        full_property_path_key = self.full_property_path_key

        value = self.value

        display_value: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.display_value, Unset):
            display_value = self.display_value.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if property_set is not UNSET:
            field_dict["propertySet"] = property_set
        if full_property_path is not UNSET:
            field_dict["fullPropertyPath"] = full_property_path
        if type_ is not UNSET:
            field_dict["type"] = type_
        if display_type is not UNSET:
            field_dict["displayType"] = display_type
        if grouping is not UNSET:
            field_dict["grouping"] = grouping
        if step_name is not UNSET:
            field_dict["stepName"] = step_name
        if step_type is not UNSET:
            field_dict["stepType"] = step_type
        if alias is not UNSET:
            field_dict["alias"] = alias
        if full_property_path_key is not UNSET:
            field_dict["fullPropertyPathKey"] = full_property_path_key
        if value is not UNSET:
            field_dict["value"] = value
        if display_value is not UNSET:
            field_dict["displayValue"] = display_value

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_property_set import VirincoWATSWebDashboardModelsMesPropertySet
        from ..models.virinco_wats_web_dashboard_models_mes_property_display_value import VirincoWATSWebDashboardModelsMesPropertyDisplayValue
        d = dict(src_dict)
        _property_set = d.pop("propertySet", UNSET)
        property_set: Union[Unset, VirincoWATSWebDashboardModelsMesPropertySet]
        if isinstance(_property_set,  Unset):
            property_set = UNSET
        else:
            property_set = VirincoWATSWebDashboardModelsMesPropertySet.from_dict(_property_set)




        full_property_path = d.pop("fullPropertyPath", UNSET)

        type_ = d.pop("type", UNSET)

        display_type = d.pop("displayType", UNSET)

        grouping = d.pop("grouping", UNSET)

        step_name = d.pop("stepName", UNSET)

        step_type = d.pop("stepType", UNSET)

        alias = d.pop("alias", UNSET)

        full_property_path_key = d.pop("fullPropertyPathKey", UNSET)

        value = d.pop("value", UNSET)

        _display_value = d.pop("displayValue", UNSET)
        display_value: Union[Unset, VirincoWATSWebDashboardModelsMesPropertyDisplayValue]
        if isinstance(_display_value,  Unset):
            display_value = UNSET
        else:
            display_value = VirincoWATSWebDashboardModelsMesPropertyDisplayValue.from_dict(_display_value)




        virinco_wats_web_dashboard_models_mes_property = cls(
            property_set=property_set,
            full_property_path=full_property_path,
            type_=type_,
            display_type=display_type,
            grouping=grouping,
            step_name=step_name,
            step_type=step_type,
            alias=alias,
            full_property_path_key=full_property_path_key,
            value=value,
            display_value=display_value,
        )


        virinco_wats_web_dashboard_models_mes_property.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_property

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
