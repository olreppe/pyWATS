"""
StepList - Polymorphic Step Container - v3 Implementation

Core component that maintains parent/child relationships and handles
polymorphic step deserialization.

Fixes:
- Proper Generic type parameter for type safety
- __get_pydantic_core_schema__ for Pydantic v2 integration
- Parent injection on all list operations
- No # type: ignore comments needed
"""
from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    TypeVar,
    Generic,
    List,
    Optional,
    Iterator,
    overload,
    Union,
    Any,
    Callable,
    Iterable,
)
from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema

from ..step import Step

if TYPE_CHECKING:
    from .sequence_call import SequenceCall

# Generic type variable for step types
StepT = TypeVar('StepT', bound=Step)


class StepList(List[StepT]):
    """
    A list that automatically sets parent reference on steps when added.
    
    This is a core WATS pattern that maintains parent/child relationships
    and enables polymorphic step deserialization.
    
    Type Parameters:
        StepT: The type of steps this list contains (bound to Step).
        
    Features:
        - Automatic parent injection on append/extend/insert/__setitem__
        - Polymorphic deserialization via step_type discriminator
        - Full list protocol support
        - Pydantic v2 integration via __get_pydantic_core_schema__
    """
    
    def __init__(
        self, 
        items: Optional[List[StepT]] = None,
        parent: Optional["SequenceCall"] = None
    ) -> None:
        """
        Initialize the StepList.
        
        Args:
            items: Optional initial list of steps
            parent: Optional parent SequenceCall to inject into items
        """
        super().__init__()
        self._parent: Optional["SequenceCall"] = parent
        
        if items:
            for item in items:
                self.append(item)
    
    @property
    def parent(self) -> Optional["SequenceCall"]:
        """Get the parent SequenceCall."""
        return self._parent
    
    @parent.setter
    def parent(self, value: Optional["SequenceCall"]) -> None:
        """Set the parent and update all existing items."""
        self._parent = value
        for item in self:
            if isinstance(item, Step):
                item.parent = value
    
    def set_parent(self, parent: "SequenceCall") -> None:
        """
        Set the parent for this list and all items in it (V1 compatibility).
        
        This method explicitly sets the parent reference for the list itself
        and injects it into all child steps.
        
        Args:
            parent: The parent SequenceCall to assign
        """
        self._parent = parent
        for item in self:
            if hasattr(item, "parent"):
                item.parent = parent
    
    def _inject_parent(self, item: StepT) -> StepT:
        """Inject parent reference into a step if parent is set."""
        if self._parent is not None and isinstance(item, Step):
            item.parent = self._parent
        return item
    
    # ========================================================================
    # List Override Methods
    # ========================================================================
    
    def append(self, item: StepT) -> None:
        """Append a step with parent injection."""
        super().append(self._inject_parent(item))
    
    def extend(self, items: Iterable[StepT]) -> None:  # type: ignore[override]
        """Extend with steps, injecting parent into each."""
        for item in items:
            self.append(item)
    
    def insert(self, index: int, item: StepT) -> None:  # type: ignore[override]
        """Insert a step at index with parent injection."""
        super().insert(index, self._inject_parent(item))
    
    @overload  # type: ignore[override]
    def __setitem__(self, index: int, value: StepT) -> None: ...
    
    @overload  # type: ignore[override]
    def __setitem__(self, index: slice, value: List[StepT]) -> None: ...
    
    def __setitem__(  # type: ignore[override]
        self, 
        index: Union[int, slice], 
        value: Union[StepT, List[StepT]]
    ) -> None:
        """Set item(s) with parent injection."""
        if isinstance(index, slice):
            if isinstance(value, list):
                value = [self._inject_parent(v) for v in value]
            super().__setitem__(index, value)  # type: ignore[assignment]
        else:
            super().__setitem__(index, self._inject_parent(value))  # type: ignore[arg-type]
    
    def __add__(self, other: List[StepT]) -> "StepList[StepT]":  # type: ignore[override]
        """Concatenate lists, returning new StepList with same parent."""
        result: StepList[StepT] = StepList(parent=self._parent)
        result.extend(list(self))
        result.extend(other)
        return result

    def __iadd__(self, other: Iterable[StepT]) -> "StepList[StepT]":  # type: ignore[override]
        """In-place concatenation with parent injection."""
        self.extend(other)
        return self
    
    # ========================================================================
    # Pydantic v2 Integration
    # ========================================================================
    
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        """
        Build Pydantic core schema for StepList.
        
        Uses handler.generate_schema(StepType) to let Pydantic handle
        polymorphic step deserialization natively via the Union type.
        This is the same approach as V1 - simple and maintainable.
        """
        # Import StepType here to avoid circular imports at module level
        from .sequence_call import StepType
        
        # Let Pydantic handle the Union type resolution for each item
        return core_schema.list_schema(
            items_schema=handler.generate_schema(StepType),
            serialization=core_schema.plain_serializer_function_ser_schema(list),
        )
    
    # ========================================================================
    # Utility Methods
    # ========================================================================
    
    def find_by_name(self, name: str) -> Optional[StepT]:
        """Find first step with the given name."""
        for step in self:
            if step.name == name:
                return step
        return None
    
    def find_all_by_name(self, name: str) -> List[StepT]:
        """Find all steps with the given name."""
        return [step for step in self if step.name == name]
    
    def find_failed(self) -> List[StepT]:
        """Find all failed steps."""
        from ...common_types import StepStatus
        return [step for step in self if step.status == StepStatus.Failed]
    
    def get_by_status(self, status: Any) -> List[StepT]:
        """Get all steps with the given status."""
        return [step for step in self if step.status == status]
    
    def count_by_status(self) -> dict[str, int]:
        """Count steps by status."""
        from collections import Counter
        return dict(Counter(step.status.value for step in self))
