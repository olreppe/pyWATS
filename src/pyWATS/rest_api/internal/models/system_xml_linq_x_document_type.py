from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.system_xml_linq_x_document_type_node_type import SystemXmlLinqXDocumentTypeNodeType
from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.system_xml_linq_x_document import SystemXmlLinqXDocument
  from ..models.system_xml_linq_x_element import SystemXmlLinqXElement
  from ..models.system_xml_linq_x_node import SystemXmlLinqXNode





T = TypeVar("T", bound="SystemXmlLinqXDocumentType")



@_attrs_define
class SystemXmlLinqXDocumentType:
    """ 
        Attributes:
            internal_subset (Union[Unset, str]):
            name (Union[Unset, str]):
            node_type (Union[Unset, SystemXmlLinqXDocumentTypeNodeType]):
            public_id (Union[Unset, str]):
            system_id (Union[Unset, str]):
            next_node (Union[Unset, SystemXmlLinqXNode]):
            previous_node (Union[Unset, SystemXmlLinqXNode]):
            base_uri (Union[Unset, str]):
            document (Union[Unset, SystemXmlLinqXDocument]):
            parent (Union[Unset, SystemXmlLinqXElement]):
     """

    internal_subset: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    node_type: Union[Unset, SystemXmlLinqXDocumentTypeNodeType] = UNSET
    public_id: Union[Unset, str] = UNSET
    system_id: Union[Unset, str] = UNSET
    next_node: Union[Unset, 'SystemXmlLinqXNode'] = UNSET
    previous_node: Union[Unset, 'SystemXmlLinqXNode'] = UNSET
    base_uri: Union[Unset, str] = UNSET
    document: Union[Unset, 'SystemXmlLinqXDocument'] = UNSET
    parent: Union[Unset, 'SystemXmlLinqXElement'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.system_xml_linq_x_document import SystemXmlLinqXDocument
        from ..models.system_xml_linq_x_element import SystemXmlLinqXElement
        from ..models.system_xml_linq_x_node import SystemXmlLinqXNode
        internal_subset = self.internal_subset

        name = self.name

        node_type: Union[Unset, int] = UNSET
        if not isinstance(self.node_type, Unset):
            node_type = self.node_type.value


        public_id = self.public_id

        system_id = self.system_id

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
        if internal_subset is not UNSET:
            field_dict["InternalSubset"] = internal_subset
        if name is not UNSET:
            field_dict["Name"] = name
        if node_type is not UNSET:
            field_dict["NodeType"] = node_type
        if public_id is not UNSET:
            field_dict["PublicId"] = public_id
        if system_id is not UNSET:
            field_dict["SystemId"] = system_id
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
        from ..models.system_xml_linq_x_element import SystemXmlLinqXElement
        from ..models.system_xml_linq_x_node import SystemXmlLinqXNode
        d = dict(src_dict)
        internal_subset = d.pop("InternalSubset", UNSET)

        name = d.pop("Name", UNSET)

        _node_type = d.pop("NodeType", UNSET)
        node_type: Union[Unset, SystemXmlLinqXDocumentTypeNodeType]
        if isinstance(_node_type,  Unset):
            node_type = UNSET
        else:
            node_type = SystemXmlLinqXDocumentTypeNodeType(_node_type)




        public_id = d.pop("PublicId", UNSET)

        system_id = d.pop("SystemId", UNSET)

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




        system_xml_linq_x_document_type = cls(
            internal_subset=internal_subset,
            name=name,
            node_type=node_type,
            public_id=public_id,
            system_id=system_id,
            next_node=next_node,
            previous_node=previous_node,
            base_uri=base_uri,
            document=document,
            parent=parent,
        )


        system_xml_linq_x_document_type.additional_properties = d
        return system_xml_linq_x_document_type

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
