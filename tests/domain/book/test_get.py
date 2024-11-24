from src.di.container import Container, UnitOfWork
from src.domain.dto.book import BookAggregateDTO
from src.domain.factory.author import AuthorDTOFactory
from src.domain.factory.book import BookDTOFactory
from src.domain.factory.category import CategoryDTOFactory
from src.domain.services.author import create_author
from src.domain.services.book import get_by_id, get_list_by_author_id, get_list_by_category_id
from src.domain.services.category import create_category
from src.domain.services.m2m import m2m_author_book_create, m2m_category_book_create


async def test_get_book_by_id(pg_container: Container, uow: UnitOfWork) -> None:
    book = BookDTOFactory.create()
    async with uow.connection() as conn, conn.transaction():
        await uow.book.create(book)

    book_aggregate_dto = await get_by_id(book.id)
    assert book_aggregate_dto == BookAggregateDTO(
        book=book,
        authors=[],
        categories=[],
        categories_id=[],
    )


async def test_get_books_by_category(pg_container: Container, uow: UnitOfWork) -> None:
    category = CategoryDTOFactory.create()
    category = await create_category(category.name, category.parent_id)

    book = BookDTOFactory.create()
    async with uow.connection() as conn, conn.transaction():
        await uow.book.create(book)

    await m2m_category_book_create(category.id, book.id)

    books_in_category = await get_list_by_category_id(category.id)
    assert books_in_category == [book]


async def test_get_books_by_author(pg_container: Container, uow: UnitOfWork) -> None:
    book = BookDTOFactory.create()
    async with uow.connection() as conn, conn.transaction():
        await uow.book.create(book)

    author = AuthorDTOFactory.create()
    author = await create_author(author.name)
    await m2m_author_book_create(author.id, book.id)

    books_by_author = await get_list_by_author_id(author.id)
    assert books_by_author == [book]
