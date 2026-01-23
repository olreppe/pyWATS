from uuid import uuid4
from typing import List

import pytest

from pywats.domains.product.enums import ProductState
from pywats.domains.product.models import Product, ProductRevision
from pywats.domains.product import ProductService


class DummyProductRepository:
    """Mock repository for testing ProductService."""
    
    def __init__(self) -> None:
        self.saved_products: List[Product] = []
        self.saved_revisions: List[ProductRevision] = []

    async def get_all(self) -> List[Product]:
        product = Product(part_number="PN-VIEW", name="View Product")
        product.product_id = uuid4()
        product.state = ProductState.ACTIVE
        return [product]

    async def get_by_part_number(self, part_number: str) -> Product:
        product = Product(part_number=part_number)
        product.product_id = uuid4()
        return product

    async def save(self, product: Product) -> Product:
        product.product_id = product.product_id or uuid4()
        self.saved_products.append(product)
        return product

    async def save_revision(self, revision: ProductRevision) -> ProductRevision:
        revision.product_revision_id = revision.product_revision_id or uuid4()
        self.saved_revisions.append(revision)
        return revision


@pytest.fixture
def product_service() -> ProductService:
    repository = DummyProductRepository()
    return ProductService(repository=repository)


@pytest.mark.asyncio
async def test_create_product_persists_via_repository(product_service: ProductService) -> None:
    repo = product_service._repository

    created = await product_service.create_product(
        part_number="PN-999",
        name="Test Product"
    )

    assert created is not None
    assert repo.saved_products[-1] is created
    assert created.product_id is not None


@pytest.mark.asyncio
async def test_create_revision_attaches_product(product_service: ProductService) -> None:
    repository = product_service._repository

    revision = await product_service.create_revision(
        part_number="PN-999",
        revision="R1",
        name="Revision 1"
    )

    assert revision is not None
    assert repository.saved_revisions
    stored_revision = repository.saved_revisions[-1]
    assert revision.product_id == stored_revision.product_id
    assert revision.product_id is not None


@pytest.mark.asyncio
async def test_get_products_returns_views(product_service: ProductService) -> None:
    views = await product_service.get_products()

    assert len(views) == 1
    assert views[0].part_number == "PN-VIEW"
