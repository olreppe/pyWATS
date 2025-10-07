from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.microsoft_o_data_uri_parser_select_item import MicrosoftODataUriParserSelectItem





T = TypeVar("T", bound="MicrosoftODataUriParserSelectExpandClause")



@_attrs_define
class MicrosoftODataUriParserSelectExpandClause:
    """ 
        Attributes:
            selected_items (Union[Unset, list['MicrosoftODataUriParserSelectItem']]):
            all_selected (Union[Unset, bool]):
     """

    selected_items: Union[Unset, list['MicrosoftODataUriParserSelectItem']] = UNSET
    all_selected: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.microsoft_o_data_uri_parser_select_item import MicrosoftODataUriParserSelectItem
        selected_items: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.selected_items, Unset):
            selected_items = []
            for selected_items_item_data in self.selected_items:
                selected_items_item = selected_items_item_data.to_dict()
                selected_items.append(selected_items_item)



        all_selected = self.all_selected


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if selected_items is not UNSET:
            field_dict["SelectedItems"] = selected_items
        if all_selected is not UNSET:
            field_dict["AllSelected"] = all_selected

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.microsoft_o_data_uri_parser_select_item import MicrosoftODataUriParserSelectItem
        d = dict(src_dict)
        selected_items = []
        _selected_items = d.pop("SelectedItems", UNSET)
        for selected_items_item_data in (_selected_items or []):
            selected_items_item = MicrosoftODataUriParserSelectItem.from_dict(selected_items_item_data)



            selected_items.append(selected_items_item)


        all_selected = d.pop("AllSelected", UNSET)

        microsoft_o_data_uri_parser_select_expand_clause = cls(
            selected_items=selected_items,
            all_selected=all_selected,
        )


        microsoft_o_data_uri_parser_select_expand_clause.additional_properties = d
        return microsoft_o_data_uri_parser_select_expand_clause

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
