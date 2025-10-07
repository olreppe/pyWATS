from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.microsoft_asp_net_o_data_query_validators_skip_token_query_validator import MicrosoftAspNetODataQueryValidatorsSkipTokenQueryValidator
  from ..models.microsoft_asp_net_o_data_query_o_data_query_settings import MicrosoftAspNetODataQueryODataQuerySettings
  from ..models.microsoft_asp_net_o_data_query_o_data_query_options import MicrosoftAspNetODataQueryODataQueryOptions
  from ..models.microsoft_asp_net_o_data_o_data_query_context import MicrosoftAspNetODataODataQueryContext





T = TypeVar("T", bound="MicrosoftAspNetODataQuerySkipTokenQueryOption")



@_attrs_define
class MicrosoftAspNetODataQuerySkipTokenQueryOption:
    """ 
        Attributes:
            raw_value (Union[Unset, str]):
            context (Union[Unset, MicrosoftAspNetODataODataQueryContext]):
            validator (Union[Unset, MicrosoftAspNetODataQueryValidatorsSkipTokenQueryValidator]):
            query_settings (Union[Unset, MicrosoftAspNetODataQueryODataQuerySettings]):
            query_options (Union[Unset, MicrosoftAspNetODataQueryODataQueryOptions]):
     """

    raw_value: Union[Unset, str] = UNSET
    context: Union[Unset, 'MicrosoftAspNetODataODataQueryContext'] = UNSET
    validator: Union[Unset, 'MicrosoftAspNetODataQueryValidatorsSkipTokenQueryValidator'] = UNSET
    query_settings: Union[Unset, 'MicrosoftAspNetODataQueryODataQuerySettings'] = UNSET
    query_options: Union[Unset, 'MicrosoftAspNetODataQueryODataQueryOptions'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.microsoft_asp_net_o_data_query_validators_skip_token_query_validator import MicrosoftAspNetODataQueryValidatorsSkipTokenQueryValidator
        from ..models.microsoft_asp_net_o_data_query_o_data_query_settings import MicrosoftAspNetODataQueryODataQuerySettings
        from ..models.microsoft_asp_net_o_data_query_o_data_query_options import MicrosoftAspNetODataQueryODataQueryOptions
        from ..models.microsoft_asp_net_o_data_o_data_query_context import MicrosoftAspNetODataODataQueryContext
        raw_value = self.raw_value

        context: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.context, Unset):
            context = self.context.to_dict()

        validator: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.validator, Unset):
            validator = self.validator.to_dict()

        query_settings: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.query_settings, Unset):
            query_settings = self.query_settings.to_dict()

        query_options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.query_options, Unset):
            query_options = self.query_options.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if raw_value is not UNSET:
            field_dict["RawValue"] = raw_value
        if context is not UNSET:
            field_dict["Context"] = context
        if validator is not UNSET:
            field_dict["Validator"] = validator
        if query_settings is not UNSET:
            field_dict["QuerySettings"] = query_settings
        if query_options is not UNSET:
            field_dict["QueryOptions"] = query_options

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.microsoft_asp_net_o_data_query_validators_skip_token_query_validator import MicrosoftAspNetODataQueryValidatorsSkipTokenQueryValidator
        from ..models.microsoft_asp_net_o_data_query_o_data_query_settings import MicrosoftAspNetODataQueryODataQuerySettings
        from ..models.microsoft_asp_net_o_data_query_o_data_query_options import MicrosoftAspNetODataQueryODataQueryOptions
        from ..models.microsoft_asp_net_o_data_o_data_query_context import MicrosoftAspNetODataODataQueryContext
        d = dict(src_dict)
        raw_value = d.pop("RawValue", UNSET)

        _context = d.pop("Context", UNSET)
        context: Union[Unset, MicrosoftAspNetODataODataQueryContext]
        if isinstance(_context,  Unset):
            context = UNSET
        else:
            context = MicrosoftAspNetODataODataQueryContext.from_dict(_context)




        _validator = d.pop("Validator", UNSET)
        validator: Union[Unset, MicrosoftAspNetODataQueryValidatorsSkipTokenQueryValidator]
        if isinstance(_validator,  Unset):
            validator = UNSET
        else:
            validator = MicrosoftAspNetODataQueryValidatorsSkipTokenQueryValidator.from_dict(_validator)




        _query_settings = d.pop("QuerySettings", UNSET)
        query_settings: Union[Unset, MicrosoftAspNetODataQueryODataQuerySettings]
        if isinstance(_query_settings,  Unset):
            query_settings = UNSET
        else:
            query_settings = MicrosoftAspNetODataQueryODataQuerySettings.from_dict(_query_settings)




        _query_options = d.pop("QueryOptions", UNSET)
        query_options: Union[Unset, MicrosoftAspNetODataQueryODataQueryOptions]
        if isinstance(_query_options,  Unset):
            query_options = UNSET
        else:
            query_options = MicrosoftAspNetODataQueryODataQueryOptions.from_dict(_query_options)




        microsoft_asp_net_o_data_query_skip_token_query_option = cls(
            raw_value=raw_value,
            context=context,
            validator=validator,
            query_settings=query_settings,
            query_options=query_options,
        )


        microsoft_asp_net_o_data_query_skip_token_query_option.additional_properties = d
        return microsoft_asp_net_o_data_query_skip_token_query_option

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
