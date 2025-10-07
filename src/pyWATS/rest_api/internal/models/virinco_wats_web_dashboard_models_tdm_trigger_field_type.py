from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_tdm_operator import VirincoWATSWebDashboardModelsTdmOperator





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsTdmTriggerFieldType")



@_attrs_define
class VirincoWATSWebDashboardModelsTdmTriggerFieldType:
    """ 
        Attributes:
            id (Union[Unset, int]):
            name (Union[Unset, str]):
            description (Union[Unset, str]):
            allow_and (Union[Unset, bool]):
            allow_or (Union[Unset, bool]):
            data_type (Union[Unset, str]):
            identifier (Union[Unset, str]):
            input_type (Union[Unset, str]):
            type_ (Union[Unset, int]):
            category (Union[Unset, str]):
            operators (Union[Unset, list['VirincoWATSWebDashboardModelsTdmOperator']]):
            sort_order (Union[Unset, int]):
     """

    id: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    allow_and: Union[Unset, bool] = UNSET
    allow_or: Union[Unset, bool] = UNSET
    data_type: Union[Unset, str] = UNSET
    identifier: Union[Unset, str] = UNSET
    input_type: Union[Unset, str] = UNSET
    type_: Union[Unset, int] = UNSET
    category: Union[Unset, str] = UNSET
    operators: Union[Unset, list['VirincoWATSWebDashboardModelsTdmOperator']] = UNSET
    sort_order: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_tdm_operator import VirincoWATSWebDashboardModelsTdmOperator
        id = self.id

        name = self.name

        description = self.description

        allow_and = self.allow_and

        allow_or = self.allow_or

        data_type = self.data_type

        identifier = self.identifier

        input_type = self.input_type

        type_ = self.type_

        category = self.category

        operators: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.operators, Unset):
            operators = []
            for operators_item_data in self.operators:
                operators_item = operators_item_data.to_dict()
                operators.append(operators_item)



        sort_order = self.sort_order


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if allow_and is not UNSET:
            field_dict["allowAnd"] = allow_and
        if allow_or is not UNSET:
            field_dict["allowOr"] = allow_or
        if data_type is not UNSET:
            field_dict["dataType"] = data_type
        if identifier is not UNSET:
            field_dict["identifier"] = identifier
        if input_type is not UNSET:
            field_dict["inputType"] = input_type
        if type_ is not UNSET:
            field_dict["type"] = type_
        if category is not UNSET:
            field_dict["category"] = category
        if operators is not UNSET:
            field_dict["operators"] = operators
        if sort_order is not UNSET:
            field_dict["sortOrder"] = sort_order

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_tdm_operator import VirincoWATSWebDashboardModelsTdmOperator
        d = dict(src_dict)
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        allow_and = d.pop("allowAnd", UNSET)

        allow_or = d.pop("allowOr", UNSET)

        data_type = d.pop("dataType", UNSET)

        identifier = d.pop("identifier", UNSET)

        input_type = d.pop("inputType", UNSET)

        type_ = d.pop("type", UNSET)

        category = d.pop("category", UNSET)

        operators = []
        _operators = d.pop("operators", UNSET)
        for operators_item_data in (_operators or []):
            operators_item = VirincoWATSWebDashboardModelsTdmOperator.from_dict(operators_item_data)



            operators.append(operators_item)


        sort_order = d.pop("sortOrder", UNSET)

        virinco_wats_web_dashboard_models_tdm_trigger_field_type = cls(
            id=id,
            name=name,
            description=description,
            allow_and=allow_and,
            allow_or=allow_or,
            data_type=data_type,
            identifier=identifier,
            input_type=input_type,
            type_=type_,
            category=category,
            operators=operators,
            sort_order=sort_order,
        )


        virinco_wats_web_dashboard_models_tdm_trigger_field_type.additional_properties = d
        return virinco_wats_web_dashboard_models_tdm_trigger_field_type

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
