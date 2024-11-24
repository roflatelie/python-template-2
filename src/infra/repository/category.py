import uuid

from src.domain.dto.category import CategoryDTO
from src.domain.interface.category import ICategoryDAO


class CategoryRepository(ICategoryDAO):
    def __init__(self, dao: ICategoryDAO):
        self._dao = dao

    async def create(self, name: str, parent_id: int | None = None) -> CategoryDTO:
        return await self._dao.create(name, parent_id)

    async def get_list(self) -> list[CategoryDTO]:
        return await self._dao.get_list()

    async def get_list_by_book_id(self, book_id: uuid.UUID | str) -> list[CategoryDTO]:
        return await self._dao.get_list_by_book_id(book_id)

    async def get_default_category_id(self) -> int:
        return await self._dao.get_default_category_id()
