from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.microsoft_asp_net_o_data_query_validators_count_query_validator import MicrosoftAspNetODataQueryValidatorsCountQueryValidator
  from ..models.microsoft_asp_net_o_data_o_data_query_context import MicrosoftAspNetODataODataQueryContext





T = TypeVar("T", bound="MicrosoftAspNetODataQueryCountQueryOption")



@_attrs_define
class MicrosoftAspNetODataQueryCountQueryOption:
    """ 
        Attributes:
            context (Union[Unset, MicrosoftAspNetODataODataQueryContext]):
            raw_value (Union[Unset, str]):
            value (Union[Unset, bool]):
            validator (Union[Unset, MicrosoftAspNetODataQueryValidatorsCountQueryValidator]):
     """

    context: Union[Unset, 'MicrosoftAspNetODataODataQueryContext'] = UNSET
    raw_value: Union[Unset, str] = UNSET
    value: Union[Unset, bool] = UNSET
    validator: Union[Unset, 'MicrosoftAspNetODataQueryValidatorsCountQueryValidator'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.microsoft_asp_net_o_data_query_validators_count_query_validator import MicrosoftAspNetODataQueryValidatorsCountQueryValidator
        from ..models.microsoft_asp_net_o_data_o_data_query_context import MicrosoftAspNetODataODataQueryContext
        context: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.context, Unset):
            context = self.context.to_dict()

        raw_value = self.raw_value

        value = self.value

        validator: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.validator, Unset):
            validator = self.validator.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if context is not UNSET:
            field_dict["Context"] = context
        if raw_value is not UNSET:
            field_dict["RawValue"] = raw_value
        if value is not UNSET:
            field_dict["Value"] = value
        if validator is not UNSET:
            field_dict["Validator"] = validator

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.microsoft_asp_net_o_data_query_validators_count_query_validator import MicrosoftAspNetODataQueryValidatorsCountQueryValidator
        from ..models.microsoft_asp_net_o_data_o_data_query_context import MicrosoftAspNetODataODataQueryContext
        d = dict(src_dict)
        _context = d.pop("Context", UNSET)
        context: Union[Unset, MicrosoftAspNetODataODataQueryContext]
        if isinstance(_context,  Unset):
            context = UNSET
        else:
            context = MicrosoftAspNetODataODataQueryContext.from_dict(_context)




        raw_value = d.pop("RawValue", UNSET)

        value = d.pop("Value", UNSET)

        _validator = d.pop("Validator", UNSET)
        validator: Union[Unset, MicrosoftAspNetODataQueryValidatorsCountQueryValidator]
        if isinstance(_validator,  Unset):
            validator = UNSET
        else:
            validator = MicrosoftAspNetODataQueryValidatorsCountQueryValidator.from_dict(_validator)




        microsoft_asp_net_o_data_query_count_query_option = cls(
            context=context,
            raw_value=raw_value,
            value=value,
            validator=validator,
        )


        microsoft_asp_net_o_data_query_count_query_option.additional_properties = d
        return microsoft_asp_net_o_data_query_count_query_option

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
