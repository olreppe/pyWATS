from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.system_xml_linq_x_node_node_type import SystemXmlLinqXNodeNodeType
from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.system_xml_linq_x_document import SystemXmlLinqXDocument
  from ..models.system_xml_linq_x_element import SystemXmlLinqXElement





T = TypeVar("T", bound="SystemXmlLinqXNode")



@_attrs_define
class SystemXmlLinqXNode:
    """ 
        Attributes:
            next_node (Union[Unset, SystemXmlLinqXNode]):
            previous_node (Union[Unset, SystemXmlLinqXNode]):
            base_uri (Union[Unset, str]):
            document (Union[Unset, SystemXmlLinqXDocument]):
            node_type (Union[Unset, SystemXmlLinqXNodeNodeType]):
            parent (Union[Unset, SystemXmlLinqXElement]):
     """

    next_node: Union[Unset, 'SystemXmlLinqXNode'] = UNSET
    previous_node: Union[Unset, 'SystemXmlLinqXNode'] = UNSET
    base_uri: Union[Unset, str] = UNSET
    document: Union[Unset, 'SystemXmlLinqXDocument'] = UNSET
    node_type: Union[Unset, SystemXmlLinqXNodeNodeType] = UNSET
    parent: Union[Unset, 'SystemXmlLinqXElement'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.system_xml_linq_x_document import SystemXmlLinqXDocument
        from ..models.system_xml_linq_x_element import SystemXmlLinqXElement
        next_node: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.next_node, Unset):
            next_node = self.next_node.to_dict()

        previous_node: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.previous_node, Unset):
            previous_node = self.previous_node.to_dict()

        base_uri = self.base_uri

        document: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.document, Unset):
            document = self.document.to_dict()

        node_type: Union[Unset, int] = UNSET
        if not isinstance(self.node_type, Unset):
            node_type = self.node_type.value


        parent: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.parent, Unset):
            parent = self.parent.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if next_node is not UNSET:
            field_dict["NextNode"] = next_node
        if previous_node is not UNSET:
            field_dict["PreviousNode"] = previous_node
        if base_uri is not UNSET:
            field_dict["BaseUri"] = base_uri
        if document is not UNSET:
            field_dict["Document"] = document
        if node_type is not UNSET:
            field_dict["NodeType"] = node_type
        if parent is not UNSET:
            field_dict["Parent"] = parent

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.system_xml_linq_x_document import SystemXmlLinqXDocument
        from ..models.system_xml_linq_x_element import SystemXmlLinqXElement
        d = dict(src_dict)
        _next_node = d.pop("NextNode", UNSET)
        next_node: Union[Unset, SystemXmlLinqXNode]
        if isinstance(_next_node,  Unset):
            next_node = UNSET
        else:
            next_node = SystemXmlLinqXNode.from_dict(_next_node)




        _previous_node = d.pop("PreviousNode", UNSET)
        previous_node: Union[Unset, SystemXmlLinqXNode]
        if isinstance(_previous_node,  Unset):
            previous_node = UNSET
        else:
            previous_node = SystemXmlLinqXNode.from_dict(_previous_node)




        base_uri = d.pop("BaseUri", UNSET)

        _document = d.pop("Document", UNSET)
        document: Union[Unset, SystemXmlLinqXDocument]
        if isinstance(_document,  Unset):
            document = UNSET
        else:
            document = SystemXmlLinqXDocument.from_dict(_document)




        _node_type = d.pop("NodeType", UNSET)
        node_type: Union[Unset, SystemXmlLinqXNodeNodeType]
        if isinstance(_node_type,  Unset):
            node_type = UNSET
        else:
            node_type = SystemXmlLinqXNodeNodeType(_node_type)




        _parent = d.pop("Parent", UNSET)
        parent: Union[Unset, SystemXmlLinqXElement]
        if isinstance(_parent,  Unset):
            parent = UNSET
        else:
            parent = SystemXmlLinqXElement.from_dict(_parent)




        system_xml_linq_x_node = cls(
            next_node=next_node,
            previous_node=previous_node,
            base_uri=base_uri,
            document=document,
            node_type=node_type,
            parent=parent,
        )


        system_xml_linq_x_node.additional_properties = d
        return system_xml_linq_x_node

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
