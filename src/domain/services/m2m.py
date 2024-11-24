import uuid

from dependency_injector.wiring import Provide, inject

from src.di.container import UnitOfWork


@inject
async def m2m_author_book_create(
    author_id: int,
    book_id: uuid.UUID | str,
    uow: UnitOfWork = Provide["uow"],
) -> None:
    async with uow.connection() as conn, conn.transaction():
        return await uow.m2m_author_book.create(author_id, book_id)


@inject
async def m2m_author_book_delete(
    author_id: int,
    book_id: uuid.UUID | str,
    uow: UnitOfWork = Provide["uow"],
) -> None:
    async with uow.connection() as conn, conn.transaction():
        return await uow.m2m_author_book.delete(author_id, book_id)


@inject
async def m2m_category_book_create(
    category_id: int,
    book_id: uuid.UUID | str,
    uow: UnitOfWork = Provide["uow"],
) -> None:
    async with uow.connection() as conn, conn.transaction():
        return await uow.m2m_category_book.create(category_id, book_id)


@inject
async def m2m_category_book_delete(
    category_id: int,
    book_id: uuid.UUID | str,
    uow: UnitOfWork = Provide["uow"],
) -> None:
    async with uow.connection() as conn, conn.transaction():
        return await uow.m2m_category_book.delete(category_id, book_id)


@inject
async def set_categories_for_book(
    book_id: uuid.UUID | str,
    categories: list[int],
    uow: UnitOfWork = Provide["uow"],
):
    async with uow.connection() as conn, conn.transaction():
        return await uow.m2m_category_book.set_categories_for_book(
            book_id,
            categories,
        )
