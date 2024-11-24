import uuid

from src.domain.dto.author import AuthorDTO
from src.domain.interface.author import IAuthorDAO


class AuthorRepository(IAuthorDAO):
    def __init__(self, dao: IAuthorDAO):
        self._dao = dao

    async def create(self, name: str) -> AuthorDTO:
        return await self._dao.create(name)

    async def get_list_by_book_id(self, book_id: uuid.UUID | str) -> list[AuthorDTO]:
        return await self._dao.get_list_by_book_id(book_id)
