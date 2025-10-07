from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.system_xml_linq_x_element_node_type import SystemXmlLinqXElementNodeType
from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.system_xml_linq_x_document import SystemXmlLinqXDocument
  from ..models.system_xml_linq_x_attribute import SystemXmlLinqXAttribute
  from ..models.system_xml_linq_x_node import SystemXmlLinqXNode
  from ..models.system_xml_linq_x_element_name import SystemXmlLinqXElementName





T = TypeVar("T", bound="SystemXmlLinqXElement")



@_attrs_define
class SystemXmlLinqXElement:
    """ 
        Attributes:
            first_attribute (Union[Unset, SystemXmlLinqXAttribute]):
            has_attributes (Union[Unset, bool]):
            has_elements (Union[Unset, bool]):
            is_empty (Union[Unset, bool]):
            last_attribute (Union[Unset, SystemXmlLinqXAttribute]):
            name (Union[Unset, SystemXmlLinqXElementName]):
            node_type (Union[Unset, SystemXmlLinqXElementNodeType]):
            value (Union[Unset, str]):
            first_node (Union[Unset, SystemXmlLinqXNode]):
            last_node (Union[Unset, SystemXmlLinqXNode]):
            next_node (Union[Unset, SystemXmlLinqXNode]):
            previous_node (Union[Unset, SystemXmlLinqXNode]):
            base_uri (Union[Unset, str]):
            document (Union[Unset, SystemXmlLinqXDocument]):
            parent (Union[Unset, SystemXmlLinqXElement]):
     """

    first_attribute: Union[Unset, 'SystemXmlLinqXAttribute'] = UNSET
    has_attributes: Union[Unset, bool] = UNSET
    has_elements: Union[Unset, bool] = UNSET
    is_empty: Union[Unset, bool] = UNSET
    last_attribute: Union[Unset, 'SystemXmlLinqXAttribute'] = UNSET
    name: Union[Unset, 'SystemXmlLinqXElementName'] = UNSET
    node_type: Union[Unset, SystemXmlLinqXElementNodeType] = UNSET
    value: Union[Unset, str] = UNSET
    first_node: Union[Unset, 'SystemXmlLinqXNode'] = UNSET
    last_node: Union[Unset, 'SystemXmlLinqXNode'] = UNSET
    next_node: Union[Unset, 'SystemXmlLinqXNode'] = UNSET
    previous_node: Union[Unset, 'SystemXmlLinqXNode'] = UNSET
    base_uri: Union[Unset, str] = UNSET
    document: Union[Unset, 'SystemXmlLinqXDocument'] = UNSET
    parent: Union[Unset, 'SystemXmlLinqXElement'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.system_xml_linq_x_document import SystemXmlLinqXDocument
        from ..models.system_xml_linq_x_attribute import SystemXmlLinqXAttribute
        from ..models.system_xml_linq_x_node import SystemXmlLinqXNode
        from ..models.system_xml_linq_x_element_name import SystemXmlLinqXElementName
        first_attribute: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.first_attribute, Unset):
            first_attribute = self.first_attribute.to_dict()

        has_attributes = self.has_attributes

        has_elements = self.has_elements

        is_empty = self.is_empty

        last_attribute: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.last_attribute, Unset):
            last_attribute = self.last_attribute.to_dict()

        name: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.name, Unset):
            name = self.name.to_dict()

        node_type: Union[Unset, int] = UNSET
        if not isinstance(self.node_type, Unset):
            node_type = self.node_type.value


        value = self.value

        first_node: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.first_node, Unset):
            first_node = self.first_node.to_dict()

        last_node: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.last_node, Unset):
            last_node = self.last_node.to_dict()

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

        parent: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.parent, Unset):
            parent = self.parent.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if first_attribute is not UNSET:
            field_dict["FirstAttribute"] = first_attribute
        if has_attributes is not UNSET:
            field_dict["HasAttributes"] = has_attributes
        if has_elements is not UNSET:
            field_dict["HasElements"] = has_elements
        if is_empty is not UNSET:
            field_dict["IsEmpty"] = is_empty
        if last_attribute is not UNSET:
            field_dict["LastAttribute"] = last_attribute
        if name is not UNSET:
            field_dict["Name"] = name
        if node_type is not UNSET:
            field_dict["NodeType"] = node_type
        if value is not UNSET:
            field_dict["Value"] = value
        if first_node is not UNSET:
            field_dict["FirstNode"] = first_node
        if last_node is not UNSET:
            field_dict["LastNode"] = last_node
        if next_node is not UNSET:
            field_dict["NextNode"] = next_node
        if previous_node is not UNSET:
            field_dict["PreviousNode"] = previous_node
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
        from ..models.system_xml_linq_x_attribute import SystemXmlLinqXAttribute
        from ..models.system_xml_linq_x_node import SystemXmlLinqXNode
        from ..models.system_xml_linq_x_element_name import SystemXmlLinqXElementName
        d = dict(src_dict)
        _first_attribute = d.pop("FirstAttribute", UNSET)
        first_attribute: Union[Unset, SystemXmlLinqXAttribute]
        if isinstance(_first_attribute,  Unset):
            first_attribute = UNSET
        else:
            first_attribute = SystemXmlLinqXAttribute.from_dict(_first_attribute)




        has_attributes = d.pop("HasAttributes", UNSET)

        has_elements = d.pop("HasElements", UNSET)

        is_empty = d.pop("IsEmpty", UNSET)

        _last_attribute = d.pop("LastAttribute", UNSET)
        last_attribute: Union[Unset, SystemXmlLinqXAttribute]
        if isinstance(_last_attribute,  Unset):
            last_attribute = UNSET
        else:
            last_attribute = SystemXmlLinqXAttribute.from_dict(_last_attribute)




        _name = d.pop("Name", UNSET)
        name: Union[Unset, SystemXmlLinqXElementName]
        if isinstance(_name,  Unset):
            name = UNSET
        else:
            name = SystemXmlLinqXElementName.from_dict(_name)




        _node_type = d.pop("NodeType", UNSET)
        node_type: Union[Unset, SystemXmlLinqXElementNodeType]
        if isinstance(_node_type,  Unset):
            node_type = UNSET
        else:
            node_type = SystemXmlLinqXElementNodeType(_node_type)




        value = d.pop("Value", UNSET)

        _first_node = d.pop("FirstNode", UNSET)
        first_node: Union[Unset, SystemXmlLinqXNode]
        if isinstance(_first_node,  Unset):
            first_node = UNSET
        else:
            first_node = SystemXmlLinqXNode.from_dict(_first_node)




        _last_node = d.pop("LastNode", UNSET)
        last_node: Union[Unset, SystemXmlLinqXNode]
        if isinstance(_last_node,  Unset):
            last_node = UNSET
        else:
            last_node = SystemXmlLinqXNode.from_dict(_last_node)




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




        _parent = d.pop("Parent", UNSET)
        parent: Union[Unset, SystemXmlLinqXElement]
        if isinstance(_parent,  Unset):
            parent = UNSET
        else:
            parent = SystemXmlLinqXElement.from_dict(_parent)




        system_xml_linq_x_element = cls(
            first_attribute=first_attribute,
            has_attributes=has_attributes,
            has_elements=has_elements,
            is_empty=is_empty,
            last_attribute=last_attribute,
            name=name,
            node_type=node_type,
            value=value,
            first_node=first_node,
            last_node=last_node,
            next_node=next_node,
            previous_node=previous_node,
            base_uri=base_uri,
            document=document,
            parent=parent,
        )


        system_xml_linq_x_element.additional_properties = d
        return system_xml_linq_x_element

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
