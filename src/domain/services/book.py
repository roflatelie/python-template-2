import uuid
from pathlib import Path

from dependency_injector.wiring import Provide, inject
from sqlalchemy.exc import NoResultFound

from src.di.container import UnitOfWork
from src.domain.dto.book import BookAggregateDTO, BookDTO


async def create_aggregate(book_id: uuid.UUID | str, uow: UnitOfWork) -> BookAggregateDTO:
    book = await uow.book.get_by_id(book_id)
    authors = await uow.author.get_list_by_book_id(book_id)
    categories = await uow.category.get_list_by_book_id(book_id)
    categories_ids = [i.id for i in categories]
    return BookAggregateDTO(
        book=book,
        authors=authors,
        categories=categories,
        categories_id=categories_ids,
    )


@inject
async def create_book(
    file: Path,
    cover: Path,
    uow: UnitOfWork = Provide["uow"],
) -> BookDTO:
    book_id = await uow.storage.generate_hash(file)
    file_ext = await uow.storage.get_file_ext(file)
    cover_ext = await uow.storage.get_file_ext(cover)
    async with uow.connection() as conn:
        if await uow.book.exists(book_id):
            return await uow.book.get_by_id(book_id)

        file_key = await uow.storage.save_file(file, "files", f"{book_id}{file_ext}")
        cover_key = await uow.storage.save_file(cover, "files", f"{book_id}{cover_ext}")
        async with conn.transaction():
            new_book = await uow.book.create(
                BookDTO(
                    id=uuid.UUID(book_id),
                    title=book_id,
                    file=file_key,
                    cover=cover_key,
                    ext=file_ext,
                ),
            )
            default_category_id = await uow.category.get_default_category_id()
            await uow.m2m_category_book.create(default_category_id, book_id)
    return new_book


@inject
async def update_book(
    book_id: uuid.UUID | str,
    *,
    uow: UnitOfWork = Provide["uow"],
    **kwargs,
) -> BookAggregateDTO:
    async with uow.connection() as conn, conn.transaction():
        await uow.book.update_book(book_id, **kwargs)
        return await create_aggregate(book_id, uow)


@inject
async def delete_book(
    book_id: uuid.UUID | str,
    uow: UnitOfWork = Provide["uow"],
) -> None:
    async with uow.connection() as conn:
        try:
            book = await uow.book.get_by_id(book_id)
        except NoResultFound:
            return
        await uow.storage.delete(book.cover)
        await uow.storage.delete(book.file)
        async with conn.transaction():
            await uow.book.delete_book(book_id)


@inject
async def get_by_id(
    book_id: uuid.UUID | str,
    uow: UnitOfWork = Provide["uow"],
) -> BookAggregateDTO:
    async with uow.connection():
        return await create_aggregate(book_id, uow)


@inject
async def get_list_by_category_id(
    category_id: int,
    uow: UnitOfWork = Provide["uow"],
) -> list[BookDTO]:
    async with uow.connection():
        return await uow.book.get_list_by_category_id(category_id)


@inject
async def get_list_by_author_id(
    author_id: int,
    uow: UnitOfWork = Provide["uow"],
) -> list[BookDTO]:
    async with uow.connection():
        return await uow.book.get_list_by_author_id(author_id)
