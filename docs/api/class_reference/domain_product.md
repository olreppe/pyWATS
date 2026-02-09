# pywats.domains.product - Class Reference

Auto-generated class reference for `pywats.domains.product`.

---

## `product.async_box_build`

### `AsyncBoxBuildTemplate`

_Async builder class for managing box build templates (product-level definitions)._

**Properties:**
- `has_pending_changes`
- `parent_part_number`
- `parent_revision`
- `parent_revision_id`
- `subunits`

**Methods:**
- `clear_all() -> Any`
- `discard() -> Any`
- `get_matching_subunits(part_number: str) -> List[...]`
- `get_required_parts() -> List[...]`
- `validate_subunit(part_number: str, revision: str) -> bool`

---

## `product.async_repository`

### `AsyncProductRepository`

_Async Product data access layer._

---

## `product.async_service`

### `AsyncProductService`

_Async Product business logic._

**Methods:**
- `is_active(product: Product) -> bool`

---

## `product.box_build`

### `BoxBuildTemplate`

_Builder class for managing box build templates (product-level definitions)._

**Properties:**
- `has_pending_changes`
- `parent_part_number`
- `parent_revision`
- `parent_revision_id`
- `subunits`

**Methods:**
- `add_subunit(part_number: str, revision: str, quantity: int, item_number: Optional[...], revision_mask: Optional[...]) -> Any`
- `clear_all() -> Any`
- `discard() -> Any`
- `get_matching_subunits(part_number: str) -> List[...]`
- `get_required_parts() -> List[...]`
- `reload() -> Any`
- `remove_subunit(part_number: str, revision: str) -> Any`
- `save() -> Any`
- `set_quantity(part_number: str, revision: str, quantity: int) -> Any`
- `update_subunit(part_number: str, revision: str, quantity: Optional[...], item_number: Optional[...], revision_mask: Optional[...]) -> Any`
- `validate_subunit(part_number: str, revision: str) -> bool`

---

## `product.enums`

### `ProductState(IntEnum)`

_Product/Revision state._

**Class Variables:**
- `INACTIVE`
- `ACTIVE`

---

## `product.models`

### `BomItem(PyWATSModel)`

_Represents a Bill of Materials (BOM) item._

**Class Variables:**
- `bom_item_id: Optional[...]`
- `product_revision_id: Optional[...]`
- `component_ref: Optional[...]`
- `part_number: Optional[...]`
- `description: Optional[...]`
- `quantity: int`
- `manufacturer: Optional[...]`
- `manufacturer_pn: Optional[...]`
- `vendor: Optional[...]`
- `vendor_pn: Optional[...]`

---

### `Product(PyWATSModel)`

_Represents a product in WATS._

**Class Variables:**
- `part_number: str`
- `name: Optional[...]`
- `description: Optional[...]`
- `non_serial: bool`
- `state: ProductState`
- `product_id: Optional[...]`
- `xml_data: Optional[...]`
- `product_category_id: Optional[...]`
- `product_category_name: Optional[...]`
- `revisions: List[...]`
- `tags: List[...]`

---

### `ProductCategory(PyWATSModel)`

_Represents a product category._

**Class Variables:**
- `category_id: Optional[...]`
- `name: Optional[...]`
- `description: Optional[...]`

---

### `ProductGroup(PyWATSModel)`

_Represents a product group._

**Class Variables:**
- `product_group_id: Optional[...]`
- `product_group_name: Optional[...]`

**Properties:**
- `name`

---

### `ProductRevision(PyWATSModel)`

_Represents a product revision in WATS._

**Class Variables:**
- `revision: str`
- `name: Optional[...]`
- `description: Optional[...]`
- `state: ProductState`
- `product_revision_id: Optional[...]`
- `product_id: Optional[...]`
- `xml_data: Optional[...]`
- `part_number: Optional[...]`
- `tags: List[...]`

---

### `ProductRevisionRelation(PyWATSModel)`

_Represents a parent-child relationship between product revisions._

**Class Variables:**
- `relation_id: Optional[...]`
- `parent_product_revision_id: UUID`
- `child_product_revision_id: UUID`
- `quantity: int`
- `item_number: Optional[...]`
- `child_part_number: Optional[...]`
- `child_revision: Optional[...]`
- `revision_mask: Optional[...]`

**Methods:**
- `matches_revision(revision: str) -> bool`

---

### `ProductView(PyWATSModel)`

_Simplified product view (used in list views)._

**Class Variables:**
- `part_number: str`
- `name: Optional[...]`
- `category: Optional[...]`
- `non_serial: bool`
- `state: ProductState`

---

## `product.sync_box_build`

### `SyncBoxBuildTemplate`

_Synchronous wrapper for AsyncBoxBuildTemplate._

**Properties:**
- `has_pending_changes`
- `parent_part_number`
- `parent_revision`
- `parent_revision_id`
- `subunits`

**Methods:**
- `add_subunit(part_number: str, revision: str, quantity: int, item_number: Optional[...], revision_mask: Optional[...]) -> Any`
- `clear_all() -> Any`
- `discard() -> Any`
- `get_matching_subunits(part_number: str) -> List[...]`
- `get_required_parts() -> List[...]`
- `reload() -> Any`
- `remove_subunit(part_number: str, revision: str) -> Any`
- `save() -> Any`
- `set_quantity(part_number: str, revision: str, quantity: int) -> Any`
- `update_subunit(part_number: str, revision: str, quantity: Optional[...], item_number: Optional[...], revision_mask: Optional[...]) -> Any`
- `validate_subunit(part_number: str, revision: str) -> bool`

---
