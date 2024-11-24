import pytest

from src.di.container import Container, UnitOfWork
from src.domain.dto.book import BookDTO
from src.domain.factory.book import BookDTOFactory


async def test_create_book_dao(pg_container: Container) -> None:
    uow: UnitOfWork = await pg_container.uow()
    book: BookDTO = BookDTOFactory.create()
    async with uow.connection() as conn, conn.transaction():
        await uow.book._dao.create(book)
        new_book = await uow.book._dao.get_by_id(book.id)
    assert book == new_book


@pytest.mark.skip("TODO:")
async def test_recreate_book_dao(pg_container: Container) -> None: ...


@pytest.mark.skip("TODO:")
async def test_update_book_dao(pg_container: Container) -> None: ...


@pytest.mark.skip("TODO:")
async def test_delete_book_dao(pg_container: Container) -> None: ...


@pytest.mark.skip("TODO:")
async def test_get_list_book_dao(pg_container: Container) -> None: ...


@pytest.mark.skip("TODO:")
async def test_get_list_by_author_dao(pg_container: Container) -> None: ...


@pytest.mark.skip("TODO:")
async def test_get_list_by_category_dao(pg_container: Container) -> None: ...
