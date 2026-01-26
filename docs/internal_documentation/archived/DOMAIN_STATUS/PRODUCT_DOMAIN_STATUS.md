# PRODUCT Domain Status

> Based on `TEMPLATE_DOMAIN_STATUS.md` and updated for `pywats.domains.product`.

## 1. Service Functions
- **Overview:** `ProductService` orchestrates catalog workflows (CRUD, revisions, BOM, grouping, tags) by translating caller-friendly parameters into `ProductRepository` payloads. It keeps state guards minimal while deferring API call orchestration (e.g., WSBF generation) to the repository.
- **Key Operations:**
  - Product lifecycle helpers (`get_products`, `get_products_full`, `get_product`, `create_product`, `update_product`, `bulk_save_products`).
  - Revision management (`get_revision`, `get_revisions`, `create_revision`, `update_revision`, `bulk_save_revisions`).
  - Bill of Materials helpers (`get_bom`, `get_bom_items`, `update_bom`) that manage WSBF XML strings and reuse XML parsing helpers (`_parse_wsbf_xml`, `_generate_wsbf_xml`).
  - Product grouping (`get_groups`, `get_groups_for_product`) and tag management (`get_product_tags`, `set_product_tags`).
- **Open Questions:** Should the BOM-parsing logic move into a dedicated `BomParser` so `ProductService` can remain focused on orchestration and the XML helpers can be reused by internal tooling?

## 2. Model Surface
- **Model Files:**
  - `models.py` – defines `Product`, `ProductRevision`, `ProductView`, `ProductGroup`, `ProductCategory`, `BomItem`, `ProductRevisionRelation`, plus supporting helpers for alias-heavy WATS schemas.
- **Class Summary:**
  - `Product` – root catalog entity with basic metadata, state, `revisions`, and `tags`.
  - `ProductRevision` – revision metadata with `product_id` links, `xml_data`, and state control.
  - `ProductRevisionRelation` – describes parent/child revision templates, including wildcards and mask matching logic.
  - `BomItem` – WSBF component metadata (part numbers, descriptions, vendor info) used during BOM updates and imports.
  - `ProductView`, `ProductGroup`, `ProductCategory` – simplified DTOs for list views and grouping.
- **Model Quality Notes:** All classes are co-located in `models.py`, which now exceeds 400 lines; consider splitting BOM helpers (`BomItem`, XML helpers) into `bom.py` and moving relation/masking logic to `relation.py` so each file stays focused on one concept.

## 3. Architecture & Diagrams
- **Class Relationships:**

```
ProductService --> ProductRepository --> HttpClient
ProductService --> Product / ProductRevision / ProductGroup models
ProductRevisionRelation --> ProductRevision (mask helpers)
```

- **Refactor Ideas:** The `ProductRepository` currently contains XML generation/parsing helpers. Moving them into a `BomXmlService` (shared with internal service) would make BOM updates easier to test and allow the public repository to focus on request shaping.

## 4. Inline Documentation
- **Domain Knowledge Additions:** The repository cautions about dot-containing revisions and WSBF expectations, which should be mirrored in service docstrings so callers know why `get_revision` uses query params.
- **Doc Gaps:** `create_revision` silently returns `None` when the parent product is missing; an inline note about the expected caller flow would reduce the risk of silent failures.

## 5. Acceptance Testing
- **Test Scenarios:**
  1. `test_create_product_persists_via_repository` – verifies the service builds the product payload, triggers `save`, and surfaces the repository-assigned `product_id` ([tests/acceptance/product/test_product_acceptance.py](tests/acceptance/product/test_product_acceptance.py)).
  2. `test_create_revision_attaches_product` – ensures the service refuses to create revisions without an existing product and that the stored revision contains the parent `product_id`.
  3. `test_get_products_returns_views` – confirms the simplified view conversion (`ProductView`) is consistent with `ProductRepository.get_all` payloads.
- **Data Setup Notes:** Use stub repositories that pre-populate products and capture saved revisions; create BOM helpers only for future tests.
- **Verification Steps:** Assert the stub repository’s saved lists (products, revisions) grow as expected and that returned DTOs share the traceable `part_number`.

## 6. Pending Work
- **Next Steps:** Add acceptance coverage for BOM serialization (`get_bom_items`/`update_bom`) and tag manipulations (`set_product_tags`).
- **Blockers:** Need a shared WSBF fixture or XML builder so BOM tests can assert well-formed WSBF without duplicating XML strings.
