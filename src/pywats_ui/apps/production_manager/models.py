"""Sequence data model for the designer.

Represents a manual inspection sequence as a tree of steps.
This is the in-memory model that drives both the visual editor
and serialization to/from the WATS API.
"""
from __future__ import annotations

import logging
import uuid
import xml.etree.ElementTree as ET
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional

from PySide6.QtCore import QObject, Signal

logger = logging.getLogger(__name__)


class StepType(Enum):
    """Available step types in a manual inspection sequence.

    Values match the WATS StepType codes where applicable.
    """
    SEQUENCE = "Sequence"
    GLOBAL_SEQUENCE = "GlobalSequence"
    NUMERIC_LIMIT = "NumericLimit"
    PASS_FAIL = "PassFail"
    STRING_VALUE = "StringValue"
    WAIT = "Wait"
    SET_UNIT_PROCESS = "SetUnitProcess"
    ATTACH_FILE = "AttachFile"
    MESSAGE_BOX = "MessageBox"
    ADD_SUBUNIT = "AddSubunit"


class StepStatus(IntEnum):
    """Execution status of a step."""
    NONE = 0
    PASSED = 1
    FAILED = 2
    SKIPPED = 3
    ERROR = 4


# Visual metadata for step types — used by the canvas and toolbox
STEP_META: Dict[StepType, Dict[str, Any]] = {
    StepType.SEQUENCE: {
        "label": "Sequence",
        "color": "#f5deb3",         # wheat / warm yellow
        "icon": "sequence",
        "is_container": True,
    },
    StepType.GLOBAL_SEQUENCE: {
        "label": "Global Sequence",
        "color": "#d4edda",         # light green
        "icon": "global_sequence",
        "is_container": False,
    },
    StepType.NUMERIC_LIMIT: {
        "label": "Numeric Limit",
        "color": "#cce5ff",         # light blue
        "icon": "numeric_limit",
        "is_container": False,
    },
    StepType.PASS_FAIL: {
        "label": "Pass/Fail",
        "color": "#d4edda",         # light green
        "icon": "pass_fail",
        "is_container": False,
    },
    StepType.STRING_VALUE: {
        "label": "String Value",
        "color": "#e2d5f1",         # light purple
        "icon": "string_value",
        "is_container": False,
    },
    StepType.WAIT: {
        "label": "Wait",
        "color": "#fff3cd",         # light yellow
        "icon": "wait",
        "is_container": False,
    },
    StepType.SET_UNIT_PROCESS: {
        "label": "Set Unit Process",
        "color": "#d6d8db",         # light gray
        "icon": "set_unit_process",
        "is_container": False,
    },
    StepType.ATTACH_FILE: {
        "label": "Attach File",
        "color": "#d6d8db",
        "icon": "attach_file",
        "is_container": False,
    },
    StepType.MESSAGE_BOX: {
        "label": "Message Box",
        "color": "#f8d7da",         # light red/pink
        "icon": "message_box",
        "is_container": False,
    },
    StepType.ADD_SUBUNIT: {
        "label": "Add Subunit",
        "color": "#d6d8db",
        "icon": "add_subunit",
        "is_container": False,
    },
}


class StepNode:
    """A single step in the sequence tree.

    Each node has a type, properties, and an ordered list of children
    (only valid for container types like Sequence).
    """

    def __init__(
        self,
        step_type: StepType,
        name: str = "",
        parent: Optional[StepNode] = None,
    ) -> None:
        self.id: str = str(uuid.uuid4())
        self.step_type = step_type
        self.name = name or STEP_META[step_type]["label"]
        self.parent = parent
        self.children: List[StepNode] = []
        self.properties: Dict[str, Any] = self._default_properties()
        self.status = StepStatus.NONE

    # -- Tree manipulation --

    def add_child(self, child: StepNode, index: int = -1) -> None:
        """Add a child step at the given index (-1 = append)."""
        child.parent = self
        if index < 0 or index >= len(self.children):
            self.children.append(child)
        else:
            self.children.insert(index, child)

    def remove_child(self, child: StepNode) -> None:
        """Remove a child step."""
        if child in self.children:
            self.children.remove(child)
            child.parent = None

    def index_in_parent(self) -> int:
        """Return this node's index within its parent, or -1."""
        if self.parent is None:
            return -1
        return self.parent.children.index(self)

    @property
    def is_container(self) -> bool:
        return STEP_META[self.step_type]["is_container"]

    @property
    def depth(self) -> int:
        """Nesting depth (root = 0)."""
        d = 0
        node = self.parent
        while node is not None:
            d += 1
            node = node.parent
        return d

    # -- Default properties per step type --

    def _default_properties(self) -> Dict[str, Any]:
        """Return sensible defaults for each step type."""
        if self.step_type == StepType.NUMERIC_LIMIT:
            return {
                "units": "",
                "comp_operator": "GELE",
                "low_limit": 0.0,
                "high_limit": 0.0,
            }
        elif self.step_type == StepType.PASS_FAIL:
            return {}
        elif self.step_type == StepType.STRING_VALUE:
            return {
                "comp_operator": "EQ",
                "string_limit": "",
            }
        elif self.step_type == StepType.WAIT:
            return {"duration_seconds": 1.0}
        elif self.step_type == StepType.MESSAGE_BOX:
            return {"message": "", "title": ""}
        elif self.step_type == StepType.SET_UNIT_PROCESS:
            return {"process_code": ""}
        elif self.step_type == StepType.ATTACH_FILE:
            return {"file_path": "", "description": ""}
        elif self.step_type == StepType.GLOBAL_SEQUENCE:
            return {"sequence_name": "", "sequence_version": ""}
        elif self.step_type == StepType.ADD_SUBUNIT:
            return {"part_number": "", "serial_number_source": ""}
        return {}

    # -- Serialization helpers --

    def to_dict(self) -> Dict[str, Any]:
        """Serialize this node (and children) to a dict."""
        return {
            "id": self.id,
            "type": self.step_type.value,
            "name": self.name,
            "properties": dict(self.properties),
            "children": [c.to_dict() for c in self.children],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any], parent: Optional[StepNode] = None) -> StepNode:
        """Deserialize a node from a dict."""
        node = cls(
            step_type=StepType(data["type"]),
            name=data.get("name", ""),
            parent=parent,
        )
        node.id = data.get("id", node.id)
        node.properties = data.get("properties", {})
        for child_data in data.get("children", []):
            child = cls.from_dict(child_data, parent=node)
            node.children.append(child)
        return node

    def __repr__(self) -> str:
        child_count = len(self.children)
        return f"StepNode({self.step_type.value}, {self.name!r}, children={child_count})"


class SequenceModel(QObject):
    """Observable model for a complete inspection sequence.

    Wraps a root StepNode (always of type Sequence) and emits signals
    when the structure changes, so the canvas and outline tree can update.
    """

    # Emitted when any structural change occurs (add, remove, move, rename)
    structure_changed = Signal()
    # Emitted when a single step's properties change
    step_changed = Signal(str)  # step id
    # Emitted when the selection changes
    selection_changed = Signal(str)  # step id (empty = deselected)
    # Emitted when the model dirty state changes
    dirty_changed = Signal(bool)

    def __init__(self, name: str = "New Sequence", parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self._root = StepNode(StepType.SEQUENCE, name=name)
        self._selected_id: str = ""
        self._dirty: bool = False
        self._definition_id: Optional[str] = None

    # -- Properties --

    @property
    def root(self) -> StepNode:
        return self._root

    @property
    def name(self) -> str:
        return self._root.name

    @name.setter
    def name(self, value: str) -> None:
        self._root.name = value
        self._mark_dirty()
        self.structure_changed.emit()

    @property
    def definition_id(self) -> Optional[str]:
        return self._definition_id

    @definition_id.setter
    def definition_id(self, value: Optional[str]) -> None:
        self._definition_id = value

    @property
    def is_dirty(self) -> bool:
        return self._dirty

    @property
    def selected_id(self) -> str:
        return self._selected_id

    # -- Dirty tracking --

    def _mark_dirty(self) -> None:
        if not self._dirty:
            self._dirty = True
            self.dirty_changed.emit(True)

    def mark_clean(self) -> None:
        """Mark model as saved / clean."""
        if self._dirty:
            self._dirty = False
            self.dirty_changed.emit(False)

    # -- Selection --

    def select(self, step_id: str) -> None:
        """Select a step by ID."""
        if step_id != self._selected_id:
            self._selected_id = step_id
            self.selection_changed.emit(step_id)

    def deselect(self) -> None:
        """Clear selection."""
        self.select("")

    def selected_node(self) -> Optional[StepNode]:
        """Return the currently selected StepNode, or None."""
        if not self._selected_id:
            return None
        return self.find_node(self._selected_id)

    # -- Node lookup --

    def find_node(self, node_id: str) -> Optional[StepNode]:
        """Find a node by ID anywhere in the tree."""
        return self._find_recursive(self._root, node_id)

    def _find_recursive(self, node: StepNode, node_id: str) -> Optional[StepNode]:
        if node.id == node_id:
            return node
        for child in node.children:
            found = self._find_recursive(child, node_id)
            if found is not None:
                return found
        return None

    # -- Mutation operations --

    def add_step(
        self,
        step_type: StepType,
        parent_id: Optional[str] = None,
        index: int = -1,
        name: str = "",
    ) -> StepNode:
        """Add a new step to the sequence.

        Args:
            step_type: Type of step to create.
            parent_id: ID of the parent container. None = root.
            index: Position within parent (-1 = append).
            name: Optional custom name.

        Returns:
            The newly created StepNode.
        """
        parent = self._root
        if parent_id:
            found = self.find_node(parent_id)
            if found is not None and found.is_container:
                parent = found

        node = StepNode(step_type, name=name)
        parent.add_child(node, index)
        self._mark_dirty()
        self.structure_changed.emit()
        return node

    def remove_step(self, step_id: str) -> bool:
        """Remove a step by ID. Cannot remove the root."""
        node = self.find_node(step_id)
        if node is None or node is self._root:
            return False
        if node.parent is not None:
            node.parent.remove_child(node)
        if self._selected_id == step_id:
            self.deselect()
        self._mark_dirty()
        self.structure_changed.emit()
        return True

    def move_step(self, step_id: str, new_parent_id: str, index: int = -1) -> bool:
        """Move a step to a new parent container."""
        node = self.find_node(step_id)
        new_parent = self.find_node(new_parent_id)
        if node is None or new_parent is None or node is self._root:
            return False
        if not new_parent.is_container:
            return False
        # Prevent moving a node into its own subtree
        check = new_parent
        while check is not None:
            if check is node:
                return False
            check = check.parent
        if node.parent is not None:
            node.parent.remove_child(node)
        new_parent.add_child(node, index)
        self._mark_dirty()
        self.structure_changed.emit()
        return True

    def rename_step(self, step_id: str, new_name: str) -> bool:
        """Rename a step."""
        node = self.find_node(step_id)
        if node is None:
            return False
        node.name = new_name
        self._mark_dirty()
        self.step_changed.emit(step_id)
        return True

    def update_step_properties(self, step_id: str, **props: Any) -> bool:
        """Update properties on a step."""
        node = self.find_node(step_id)
        if node is None:
            return False
        node.properties.update(props)
        self._mark_dirty()
        self.step_changed.emit(step_id)
        return True

    # -- Serialization --

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the full sequence to a dict."""
        return {
            "definition_id": self._definition_id,
            "root": self._root.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SequenceModel:
        """Create a SequenceModel from a serialized dict."""
        root_data = data.get("root", {})
        model = cls(name=root_data.get("name", "Sequence"))
        model._root = StepNode.from_dict(root_data)
        model._definition_id = data.get("definition_id")
        model._dirty = False
        return model

    def clear(self) -> None:
        """Reset to an empty sequence."""
        self._root = StepNode(StepType.SEQUENCE, name="New Sequence")
        self._selected_id = ""
        self._definition_id = None
        self._dirty = False
        self.structure_changed.emit()
        self.dirty_changed.emit(False)


# =====================================================================
# XAML Parser — converts WATS MI XAML into a StepNode tree
# =====================================================================

# Mapping from XAML element local names to StepType
_XAML_TAG_MAP: Dict[str, StepType] = {
    "Sequence": StepType.SEQUENCE,
    "NumericTest": StepType.NUMERIC_LIMIT,
    "PassFailTest": StepType.PASS_FAIL,
    "StringTest": StepType.STRING_VALUE,
    "Wait": StepType.WAIT,
    "AttachFile": StepType.ATTACH_FILE,
    "MessageBox": StepType.MESSAGE_BOX,
    "AddSubUnit": StepType.ADD_SUBUNIT,
}

# Namespaces to strip when comparing element tags
_MI_NS = "clr-namespace:Virinco.WATS.Workflow.Activities.ManualInspection;assembly=Virinco.WATS.Workflow.Activities"
_IGNORED_PREFIXES = (
    "{http://schemas.microsoft.com/",
    "{clr-namespace:Microsoft.",
    "{clr-namespace:System.",
    "{http://schemas.openxmlformats.org/",
)


def _local_tag(tag: str) -> str:
    """Strip namespace from an XML tag, e.g. '{ns}Foo' → 'Foo'."""
    if tag.startswith("{"):
        return tag.split("}", 1)[1]
    return tag


def _is_step_element(tag: str) -> bool:
    """Return True if the element represents an MI step (not metadata)."""
    local = _local_tag(tag)
    if local in _XAML_TAG_MAP:
        return True
    return False


def _parse_comp_operator(raw: str) -> str:
    """Extract operator name from '[CompOperatorType.GELE]' format."""
    if raw.startswith("[") and "." in raw:
        return raw.split(".")[-1].rstrip("]")
    return raw


def _parse_duration(raw: str) -> float:
    """Parse 'HH:MM:SS' duration to seconds."""
    parts = raw.split(":")
    if len(parts) == 3:
        try:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
        except ValueError:
            pass
    return 0.0


def _extract_properties(step_type: StepType, attribs: Dict[str, str]) -> Dict[str, Any]:
    """Extract step properties from XML attributes."""
    props: Dict[str, Any] = {}

    # Common properties
    desc = attribs.get("Description", "")
    if desc and desc != "{x:Null}":
        props["description"] = desc
    allow_skip = attribs.get("AllowSkip", "")
    if allow_skip:
        props["allow_skip"] = allow_skip.lower() == "true"
    media = attribs.get("MediaUrl", "")
    if media:
        props["media_url"] = media
    pdf_page = attribs.get("PdfPageNumber", "")
    if pdf_page and pdf_page != "{x:Null}":
        try:
            props["pdf_page_number"] = int(pdf_page)
        except ValueError:
            pass

    if step_type == StepType.NUMERIC_LIMIT:
        comp = attribs.get("CompOperator", "")
        if comp:
            props["comp_operator"] = _parse_comp_operator(comp)
        try:
            props["low_limit"] = float(attribs.get("LowLimit", "0"))
        except ValueError:
            props["low_limit"] = 0.0
        try:
            props["high_limit"] = float(attribs.get("HighLimit", "0"))
        except ValueError:
            props["high_limit"] = 0.0
        props["units"] = attribs.get("Units", "")

    elif step_type == StepType.STRING_VALUE:
        props["string_limit"] = attribs.get("Limit", "")
        props["limit_is_regex"] = attribs.get("LimitIsRegex", "False").lower() == "true"

    elif step_type == StepType.WAIT:
        duration_str = attribs.get("Duration", "00:00:00")
        props["duration_seconds"] = _parse_duration(duration_str)

    elif step_type == StepType.MESSAGE_BOX:
        options = attribs.get("Options", "")
        if options:
            props["options"] = options.split("\n")
        props["enable_response_text"] = attribs.get(
            "EnableResponseText", "False").lower() == "true"

    elif step_type == StepType.ADD_SUBUNIT:
        pn = attribs.get("PartNumber", "")
        if pn and pn != "{x:Null}":
            props["part_number"] = pn
        rev = attribs.get("Revision", "")
        if rev and rev != "{x:Null}":
            props["revision"] = rev

    return props


def _parse_element(elem: ET.Element, parent: Optional[StepNode] = None) -> Optional[StepNode]:
    """Recursively parse an XML element into a StepNode."""
    local = _local_tag(elem.tag)
    step_type = _XAML_TAG_MAP.get(local)
    if step_type is None:
        return None

    # Clean attributes — strip namespace prefixed attrs
    attribs: Dict[str, str] = {}
    for k, v in elem.attrib.items():
        clean_key = _local_tag(k)
        # Skip WF designer metadata attributes
        if any(k.startswith(p) for p in _IGNORED_PREFIXES):
            continue
        attribs[clean_key] = v

    name = attribs.get("DisplayName", STEP_META[step_type]["label"])
    node = StepNode(step_type, name=name, parent=parent)

    # Use GUID from XAML if available
    guid = attribs.get("GUID", "")
    if guid:
        node.id = guid

    # Extract step-specific properties
    node.properties = _extract_properties(step_type, attribs)

    # Recursively parse children (only for Sequence containers)
    if step_type == StepType.SEQUENCE:
        for child_elem in elem:
            if _is_step_element(child_elem.tag):
                child_node = _parse_element(child_elem, parent=node)
                if child_node is not None:
                    node.children.append(child_node)

    return node


def parse_xaml(xaml_string: str) -> Optional[StepNode]:
    """Parse a WATS MI XAML definition string into a StepNode tree.

    Returns the root Sequence node, or None on parse failure.
    """
    if not xaml_string or not xaml_string.strip():
        return None
    try:
        root_elem = ET.fromstring(xaml_string)
        return _parse_element(root_elem)
    except ET.ParseError as exc:
        logger.error("XAML parse error: %s", exc)
        return None
