import uuid

import msgspec
import sqlalchemy as sa
from sqlalchemy.exc import NoResultFound

from src.domain.dto.book import BookDTO
from src.domain.interface.book import IBookDAO
from src.infra.dao.asyncpg_sqla.db import execute, fetch, fetchrow, fetchval
from src.infra.db.postgresql.public import book, m2m_author_book, m2m_category_book
from src.vars import PGConnection


class BookAsyncpgSQLADAO(IBookDAO):
    async def create(self, book_dto: BookDTO) -> BookDTO:
        stmt = (
            sa.insert(book)
            .values(**msgspec.to_builtins(book_dto))
        )
        await execute(stmt)

        return book_dto

    async def update_book(self, book_id: uuid.UUID | str, /, **kwargs) -> None:
        stmt = (
            sa.update(book)
            .where(book.c.id == book_id)
            .values(**kwargs)
        )
        await execute(stmt)

    async def exists(self, book_id: uuid.UUID | str) -> bool:
        stmt = (
            sa.select(
                sa.exists()
                .where(book.c.id == book_id)
            )
        )
        return await fetchval(stmt)

    async def get_by_id(self, book_id: uuid.UUID | str) -> BookDTO:
        stmt = (
            sa.select(book)
            .where(book.c.id == book_id)
            .limit(1)
        )
        row = await fetchrow(stmt)
        if row is None:
            raise NoResultFound
        return msgspec.convert(row, BookDTO)

    async def delete_book(self, book_id: uuid.UUID | str) -> None:
        stmt = (
            sa.delete(book)
            .where(book.c.id == book_id)
        )
        await execute(stmt)

    async def get_list_by_author_id(self, author_id: int) -> list[BookDTO]:
        stmt = (
            sa.select(book)
            .join(m2m_author_book, m2m_author_book.c.book_id == book.c.id)
            .where(m2m_author_book.c.author_id == author_id)
            .order_by(book.c.title)
        )
        rows = await fetch(stmt)
        return msgspec.convert(rows, list[BookDTO])

    async def get_list_by_category_id(self, category_id: int) -> list[BookDTO]:
        stmt = (
            sa.select(book)
            .join(m2m_category_book, m2m_category_book.c.book_id == book.c.id)
            .order_by(book.c.title)
            .where(m2m_category_book.c.category_id == category_id)
        )
        rows = await fetch(stmt)
        return msgspec.convert(rows, list[BookDTO])
