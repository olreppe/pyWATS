from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.system_xml_linq_x_document_node_type import SystemXmlLinqXDocumentNodeType
from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.system_xml_linq_x_document_type import SystemXmlLinqXDocumentType
  from ..models.system_xml_linq_x_element import SystemXmlLinqXElement
  from ..models.system_xml_linq_x_node import SystemXmlLinqXNode
  from ..models.system_xml_linq_x_declaration import SystemXmlLinqXDeclaration





T = TypeVar("T", bound="SystemXmlLinqXDocument")



@_attrs_define
class SystemXmlLinqXDocument:
    """ 
        Attributes:
            declaration (Union[Unset, SystemXmlLinqXDeclaration]):
            document_type (Union[Unset, SystemXmlLinqXDocumentType]):
            node_type (Union[Unset, SystemXmlLinqXDocumentNodeType]):
            root (Union[Unset, SystemXmlLinqXElement]):
            first_node (Union[Unset, SystemXmlLinqXNode]):
            last_node (Union[Unset, SystemXmlLinqXNode]):
            next_node (Union[Unset, SystemXmlLinqXNode]):
            previous_node (Union[Unset, SystemXmlLinqXNode]):
            base_uri (Union[Unset, str]):
            document (Union[Unset, SystemXmlLinqXDocument]):
            parent (Union[Unset, SystemXmlLinqXElement]):
     """

    declaration: Union[Unset, 'SystemXmlLinqXDeclaration'] = UNSET
    document_type: Union[Unset, 'SystemXmlLinqXDocumentType'] = UNSET
    node_type: Union[Unset, SystemXmlLinqXDocumentNodeType] = UNSET
    root: Union[Unset, 'SystemXmlLinqXElement'] = UNSET
    first_node: Union[Unset, 'SystemXmlLinqXNode'] = UNSET
    last_node: Union[Unset, 'SystemXmlLinqXNode'] = UNSET
    next_node: Union[Unset, 'SystemXmlLinqXNode'] = UNSET
    previous_node: Union[Unset, 'SystemXmlLinqXNode'] = UNSET
    base_uri: Union[Unset, str] = UNSET
    document: Union[Unset, 'SystemXmlLinqXDocument'] = UNSET
    parent: Union[Unset, 'SystemXmlLinqXElement'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.system_xml_linq_x_document_type import SystemXmlLinqXDocumentType
        from ..models.system_xml_linq_x_element import SystemXmlLinqXElement
        from ..models.system_xml_linq_x_node import SystemXmlLinqXNode
        from ..models.system_xml_linq_x_declaration import SystemXmlLinqXDeclaration
        declaration: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.declaration, Unset):
            declaration = self.declaration.to_dict()

        document_type: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.document_type, Unset):
            document_type = self.document_type.to_dict()

        node_type: Union[Unset, int] = UNSET
        if not isinstance(self.node_type, Unset):
            node_type = self.node_type.value


        root: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.root, Unset):
            root = self.root.to_dict()

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
        if declaration is not UNSET:
            field_dict["Declaration"] = declaration
        if document_type is not UNSET:
            field_dict["DocumentType"] = document_type
        if node_type is not UNSET:
            field_dict["NodeType"] = node_type
        if root is not UNSET:
            field_dict["Root"] = root
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
        from ..models.system_xml_linq_x_document_type import SystemXmlLinqXDocumentType
        from ..models.system_xml_linq_x_element import SystemXmlLinqXElement
        from ..models.system_xml_linq_x_node import SystemXmlLinqXNode
        from ..models.system_xml_linq_x_declaration import SystemXmlLinqXDeclaration
        d = dict(src_dict)
        _declaration = d.pop("Declaration", UNSET)
        declaration: Union[Unset, SystemXmlLinqXDeclaration]
        if isinstance(_declaration,  Unset):
            declaration = UNSET
        else:
            declaration = SystemXmlLinqXDeclaration.from_dict(_declaration)




        _document_type = d.pop("DocumentType", UNSET)
        document_type: Union[Unset, SystemXmlLinqXDocumentType]
        if isinstance(_document_type,  Unset):
            document_type = UNSET
        else:
            document_type = SystemXmlLinqXDocumentType.from_dict(_document_type)




        _node_type = d.pop("NodeType", UNSET)
        node_type: Union[Unset, SystemXmlLinqXDocumentNodeType]
        if isinstance(_node_type,  Unset):
            node_type = UNSET
        else:
            node_type = SystemXmlLinqXDocumentNodeType(_node_type)




        _root = d.pop("Root", UNSET)
        root: Union[Unset, SystemXmlLinqXElement]
        if isinstance(_root,  Unset):
            root = UNSET
        else:
            root = SystemXmlLinqXElement.from_dict(_root)




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




        system_xml_linq_x_document = cls(
            declaration=declaration,
            document_type=document_type,
            node_type=node_type,
            root=root,
            first_node=first_node,
            last_node=last_node,
            next_node=next_node,
            previous_node=previous_node,
            base_uri=base_uri,
            document=document,
            parent=parent,
        )


        system_xml_linq_x_document.additional_properties = d
        return system_xml_linq_x_document

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
