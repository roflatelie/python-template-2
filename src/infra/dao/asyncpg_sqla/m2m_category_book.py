import uuid

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg_sa

from src.domain.interface.m2m_category_book import IM2MCategoryBookDAO
from src.infra.dao.asyncpg_sqla.db import execute
from src.infra.db.postgresql.public import m2m_category_book
from src.vars import PGConnection


class M2MCategoryBookAsyncpgSQLADAO(IM2MCategoryBookDAO):
    async def set_categories_for_book(
        self,
        book_id: uuid.UUID | str,
        categories: list[int],
    ) -> None:
        rm_stmt = (
            sa.delete(m2m_category_book)
            .where(
                sa.and_(
                    m2m_category_book.c.book_id == book_id,
                    m2m_category_book.c.category_id.notin_(categories),
                ),
            )
        )
        await execute(rm_stmt)

        if categories:
            add_stmt = (
                pg_sa.insert(m2m_category_book)
                .on_conflict_do_nothing(index_elements=["book_id", "category_id"])
                .values(
                    [
                        {"book_id": book_id, "category_id": category_id}
                        for category_id in categories
                    ]
                )
            )
            await execute(add_stmt)

    async def create(self, category_id: int, book_id: uuid.UUID | str) -> None:
        stmt = (
            pg_sa.insert(m2m_category_book)
            .values(category_id=category_id, book_id=book_id)
            .on_conflict_do_nothing(index_elements=["category_id", "book_id"])
        )
        await execute(stmt)

    async def delete(self, category_id: int, book_id: uuid.UUID | str) -> None:
        raise NotImplementedError(self.delete)
