import uuid

from src.domain.dto.book import BookDTO
from src.domain.interface.book import IBookDAO


class BookRepository(IBookDAO):
    def __init__(self, dao: IBookDAO):
        self._dao = dao

    async def create(self, book_dto: BookDTO) -> BookDTO:
        return await self._dao.create(book_dto)

    async def exists(self, book_id: uuid.UUID | str) -> bool:
        return await self._dao.exists(book_id)

    async def get_by_id(self, book_id: uuid.UUID | str) -> BookDTO:
        return await self._dao.get_by_id(book_id)

    async def update_book(self, book_id: uuid.UUID | str, /, **kwargs) -> None:
        return await self._dao.update_book(book_id, **kwargs)

    async def delete_book(self, book_id: uuid.UUID | str) -> None:
        return await self._dao.delete_book(book_id)

    async def get_list_by_author_id(self, author_id: int) -> list[BookDTO]:
        return await self._dao.get_list_by_author_id(author_id)

    async def get_list_by_category_id(self, category_id: int) -> list[BookDTO]:
        return await self._dao.get_list_by_category_id(category_id)
