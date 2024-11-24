import uuid

import sqlalchemy.dialects.postgresql as pg_sa

from src.domain.interface.m2m_author_book import IM2MAuthorBookDAO
from src.infra.dao.asyncpg_sqla.db import execute
from src.infra.db.postgresql.public import m2m_author_book
from src.vars import PGConnection


class M2MAuthorBookAsyncpgSQLADAO(IM2MAuthorBookDAO):
    async def create(self, author_id: int, book_id: uuid.UUID | str) -> None:
        conn = PGConnection.get()
        stmt = (
            pg_sa.insert(m2m_author_book)
            .on_conflict_do_nothing(index_elements=["author_id", "book_id"])
            .values(author_id=author_id, book_id=book_id)
        )
        await execute(stmt)

    async def delete(self, author_id: int, book_id: uuid.UUID | str) -> None:
        raise NotImplementedError(self.delete)
