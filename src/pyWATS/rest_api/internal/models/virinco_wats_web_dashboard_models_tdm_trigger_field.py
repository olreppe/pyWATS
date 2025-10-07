from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_tdm_trigger_field_type import VirincoWATSWebDashboardModelsTdmTriggerFieldType
  from ..models.virinco_wats_web_dashboard_models_tdm_operator import VirincoWATSWebDashboardModelsTdmOperator





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmTriggerField")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmTriggerField:
    """ 
        Attributes:
            id (Union[Unset, int]):
            trigger_id (Union[Unset, int]):
            trigger_field_type_id (Union[Unset, int]):
            trigger_field_type (Union[Unset, VirincoWATSWebDashboardModelsTdmTriggerFieldType]):
            trigger_field_section_id (Union[Unset, int]):
            operator_id (Union[Unset, int]):
            operator (Union[Unset, VirincoWATSWebDashboardModelsTdmOperator]):
            available_operators (Union[Unset, list['VirincoWATSWebDashboardModelsTdmOperator']]):
            value (Union[Unset, str]):
            type_ (Union[Unset, int]):
            is_new (Union[Unset, bool]):
     """

    id: Union[Unset, int] = UNSET
    trigger_id: Union[Unset, int] = UNSET
    trigger_field_type_id: Union[Unset, int] = UNSET
    trigger_field_type: Union[Unset, 'VirincoWATSWebDashboardModelsTdmTriggerFieldType'] = UNSET
    trigger_field_section_id: Union[Unset, int] = UNSET
    operator_id: Union[Unset, int] = UNSET
    operator: Union[Unset, 'VirincoWATSWebDashboardModelsTdmOperator'] = UNSET
    available_operators: Union[Unset, list['VirincoWATSWebDashboardModelsTdmOperator']] = UNSET
    value: Union[Unset, str] = UNSET
    type_: Union[Unset, int] = UNSET
    is_new: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_tdm_trigger_field_type import VirincoWATSWebDashboardModelsTdmTriggerFieldType
        from ..models.virinco_wats_web_dashboard_models_tdm_operator import VirincoWATSWebDashboardModelsTdmOperator
        id = self.id

        trigger_id = self.trigger_id

        trigger_field_type_id = self.trigger_field_type_id

        trigger_field_type: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.trigger_field_type, Unset):
            trigger_field_type = self.trigger_field_type.to_dict()

        trigger_field_section_id = self.trigger_field_section_id

        operator_id = self.operator_id

        operator: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.operator, Unset):
            operator = self.operator.to_dict()

        available_operators: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.available_operators, Unset):
            available_operators = []
            for available_operators_item_data in self.available_operators:
                available_operators_item = available_operators_item_data.to_dict()
                available_operators.append(available_operators_item)



        value = self.value

        type_ = self.type_

        is_new = self.is_new


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if trigger_id is not UNSET:
            field_dict["triggerId"] = trigger_id
        if trigger_field_type_id is not UNSET:
            field_dict["triggerFieldTypeId"] = trigger_field_type_id
        if trigger_field_type is not UNSET:
            field_dict["triggerFieldType"] = trigger_field_type
        if trigger_field_section_id is not UNSET:
            field_dict["triggerFieldSectionId"] = trigger_field_section_id
        if operator_id is not UNSET:
            field_dict["operatorId"] = operator_id
        if operator is not UNSET:
            field_dict["operator"] = operator
        if available_operators is not UNSET:
            field_dict["availableOperators"] = available_operators
        if value is not UNSET:
            field_dict["value"] = value
        if type_ is not UNSET:
            field_dict["type"] = type_
        if is_new is not UNSET:
            field_dict["IsNew"] = is_new

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_tdm_trigger_field_type import VirincoWATSWebDashboardModelsTdmTriggerFieldType
        from ..models.virinco_wats_web_dashboard_models_tdm_operator import VirincoWATSWebDashboardModelsTdmOperator
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        trigger_id = d.pop("triggerId", UNSET)

        trigger_field_type_id = d.pop("triggerFieldTypeId", UNSET)

        _trigger_field_type = d.pop("triggerFieldType", UNSET)
        trigger_field_type: Union[Unset, VirincoWATSWebDashboardModelsTdmTriggerFieldType]
        if isinstance(_trigger_field_type,  Unset):
            trigger_field_type = UNSET
        else:
            trigger_field_type = VirincoWATSWebDashboardModelsTdmTriggerFieldType.from_dict(_trigger_field_type)




        trigger_field_section_id = d.pop("triggerFieldSectionId", UNSET)

        operator_id = d.pop("operatorId", UNSET)

        _operator = d.pop("operator", UNSET)
        operator: Union[Unset, VirincoWATSWebDashboardModelsTdmOperator]
        if isinstance(_operator,  Unset):
            operator = UNSET
        else:
            operator = VirincoWATSWebDashboardModelsTdmOperator.from_dict(_operator)




        available_operators = []
        _available_operators = d.pop("availableOperators", UNSET)
        for available_operators_item_data in (_available_operators or []):
            available_operators_item = VirincoWATSWebDashboardModelsTdmOperator.from_dict(available_operators_item_data)



            available_operators.append(available_operators_item)


        value = d.pop("value", UNSET)

        type_ = d.pop("type", UNSET)

        is_new = d.pop("IsNew", UNSET)

        virinco_wats_web_dashboard_models_tdm_trigger_field = cls(
            id=id,
            trigger_id=trigger_id,
            trigger_field_type_id=trigger_field_type_id,
            trigger_field_type=trigger_field_type,
            trigger_field_section_id=trigger_field_section_id,
            operator_id=operator_id,
            operator=operator,
            available_operators=available_operators,
            value=value,
            type_=type_,
            is_new=is_new,
        )


        virinco_wats_web_dashboard_models_tdm_trigger_field.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_trigger_field

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
