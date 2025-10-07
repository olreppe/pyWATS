from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.system_xml_linq_x_attribute_node_type import SystemXmlLinqXAttributeNodeType
from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.system_xml_linq_x_document import SystemXmlLinqXDocument
  from ..models.system_xml_linq_x_attribute_name import SystemXmlLinqXAttributeName
  from ..models.system_xml_linq_x_element import SystemXmlLinqXElement





T = TypeVar("T", bound="SystemXmlLinqXAttribute")



@_attrs_define
class SystemXmlLinqXAttribute:
    """ 
        Attributes:
            is_namespace_declaration (Union[Unset, bool]):
            name (Union[Unset, SystemXmlLinqXAttributeName]):
            next_attribute (Union[Unset, SystemXmlLinqXAttribute]):
            node_type (Union[Unset, SystemXmlLinqXAttributeNodeType]):
            previous_attribute (Union[Unset, SystemXmlLinqXAttribute]):
            value (Union[Unset, str]):
            base_uri (Union[Unset, str]):
            document (Union[Unset, SystemXmlLinqXDocument]):
            parent (Union[Unset, SystemXmlLinqXElement]):
     """

    is_namespace_declaration: Union[Unset, bool] = UNSET
    name: Union[Unset, 'SystemXmlLinqXAttributeName'] = UNSET
    next_attribute: Union[Unset, 'SystemXmlLinqXAttribute'] = UNSET
    node_type: Union[Unset, SystemXmlLinqXAttributeNodeType] = UNSET
    previous_attribute: Union[Unset, 'SystemXmlLinqXAttribute'] = UNSET
    value: Union[Unset, str] = UNSET
    base_uri: Union[Unset, str] = UNSET
    document: Union[Unset, 'SystemXmlLinqXDocument'] = UNSET
    parent: Union[Unset, 'SystemXmlLinqXElement'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.system_xml_linq_x_document import SystemXmlLinqXDocument
        from ..models.system_xml_linq_x_attribute_name import SystemXmlLinqXAttributeName
        from ..models.system_xml_linq_x_element import SystemXmlLinqXElement
        is_namespace_declaration = self.is_namespace_declaration

        name: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.name, Unset):
            name = self.name.to_dict()

        next_attribute: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.next_attribute, Unset):
            next_attribute = self.next_attribute.to_dict()

        node_type: Union[Unset, int] = UNSET
        if not isinstance(self.node_type, Unset):
            node_type = self.node_type.value


        previous_attribute: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.previous_attribute, Unset):
            previous_attribute = self.previous_attribute.to_dict()

        value = self.value

        base_uri = self.base_uri

        document: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.document, Unset):
            document = self.document.to_dict()

        parent: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.parent, Unset):
            parent = self.parent.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if is_namespace_declaration is not UNSET:
            field_dict["IsNamespaceDeclaration"] = is_namespace_declaration
        if name is not UNSET:
            field_dict["Name"] = name
        if next_attribute is not UNSET:
            field_dict["NextAttribute"] = next_attribute
        if node_type is not UNSET:
            field_dict["NodeType"] = node_type
        if previous_attribute is not UNSET:
            field_dict["PreviousAttribute"] = previous_attribute
        if value is not UNSET:
            field_dict["Value"] = value
        if base_uri is not UNSET:
            field_dict["BaseUri"] = base_uri
        if document is not UNSET:
            field_dict["Document"] = document
        if parent is not UNSET:
            field_dict["Parent"] = parent

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.system_xml_linq_x_document import SystemXmlLinqXDocument
        from ..models.system_xml_linq_x_attribute_name import SystemXmlLinqXAttributeName
        from ..models.system_xml_linq_x_element import SystemXmlLinqXElement
        d = dict(src_dict)
        is_namespace_declaration = d.pop("IsNamespaceDeclaration", UNSET)

        _name = d.pop("Name", UNSET)
        name: Union[Unset, SystemXmlLinqXAttributeName]
        if isinstance(_name,  Unset):
            name = UNSET
        else:
            name = SystemXmlLinqXAttributeName.from_dict(_name)




        _next_attribute = d.pop("NextAttribute", UNSET)
        next_attribute: Union[Unset, SystemXmlLinqXAttribute]
        if isinstance(_next_attribute,  Unset):
            next_attribute = UNSET
        else:
            next_attribute = SystemXmlLinqXAttribute.from_dict(_next_attribute)




        _node_type = d.pop("NodeType", UNSET)
        node_type: Union[Unset, SystemXmlLinqXAttributeNodeType]
        if isinstance(_node_type,  Unset):
            node_type = UNSET
        else:
            node_type = SystemXmlLinqXAttributeNodeType(_node_type)




        _previous_attribute = d.pop("PreviousAttribute", UNSET)
        previous_attribute: Union[Unset, SystemXmlLinqXAttribute]
        if isinstance(_previous_attribute,  Unset):
            previous_attribute = UNSET
        else:
            previous_attribute = SystemXmlLinqXAttribute.from_dict(_previous_attribute)




        value = d.pop("Value", UNSET)

        base_uri = d.pop("BaseUri", UNSET)

        _document = d.pop("Document", UNSET)
        document: Union[Unset, SystemXmlLinqXDocument]
        if isinstance(_document,  Unset):
            document = UNSET
        else:
            document = SystemXmlLinqXDocument.from_dict(_document)




        _parent = d.pop("Parent", UNSET)
        parent: Union[Unset, SystemXmlLinqXElement]
        if isinstance(_parent,  Unset):
            parent = UNSET
        else:
            parent = SystemXmlLinqXElement.from_dict(_parent)




        system_xml_linq_x_attribute = cls(
            is_namespace_declaration=is_namespace_declaration,
            name=name,
            next_attribute=next_attribute,
            node_type=node_type,
            previous_attribute=previous_attribute,
            value=value,
            base_uri=base_uri,
            document=document,
            parent=parent,
        )


        system_xml_linq_x_attribute.additional_properties = d
        return system_xml_linq_x_attribute

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
