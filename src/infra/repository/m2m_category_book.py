import uuid

from src.domain.interface.m2m_category_book import IM2MCategoryBookDAO


class M2MCategoryBookRepository(IM2MCategoryBookDAO):
    def __init__(self, dao: IM2MCategoryBookDAO):
        self._dao = dao

    async def create(self, category_id: int, book_id: uuid.UUID | str) -> None:
        return await self._dao.create(category_id, book_id)

    async def delete(self, category_id: int, book_id: uuid.UUID | str) -> None:
        return await self._dao.delete(category_id, book_id)

    async def set_categories_for_book(
        self,
        book_id: uuid.UUID | str,
        categories: list[int],
    ) -> None:
        return await self._dao.set_categories_for_book(book_id, categories)
