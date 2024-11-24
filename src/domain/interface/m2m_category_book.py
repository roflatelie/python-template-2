import uuid
from abc import ABC, abstractmethod


class IM2MCategoryBookDAO(ABC):
    @abstractmethod
    async def create(self, category_id: int, book_id: uuid.UUID | str) -> None: ...

    @abstractmethod
    async def delete(self, category_id: int, book_id: uuid.UUID | str) -> None: ...

    @abstractmethod
    async def set_categories_for_book(self, book_id: uuid.UUID | str, categories: list[int]) -> None: ...
