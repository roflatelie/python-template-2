import uuid

from src.domain.interface.m2m_author_book import IM2MAuthorBookDAO


class M2MAuthorBookRepository(IM2MAuthorBookDAO):
    def __init__(self, dao: IM2MAuthorBookDAO):
        self._dao = dao

    async def create(self, author_id: int, book_id: uuid.UUID | str) -> None:
        return await self._dao.create(author_id, book_id)

    async def delete(self, author_id: int, book_id: uuid.UUID | str) -> None:
        return await self._dao.delete(author_id, book_id)
