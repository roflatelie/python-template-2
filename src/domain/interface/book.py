import uuid
from abc import ABC, abstractmethod

from src.domain.dto.book import BookDTO


class IBookDAO(ABC):
    @abstractmethod
    async def create(self, book_dto: BookDTO) -> BookDTO: ...

    @abstractmethod
    async def exists(self, book_id: uuid.UUID | str) -> bool: ...

    @abstractmethod
    async def get_by_id(self, book_id: uuid.UUID | str) -> BookDTO: ...

    @abstractmethod
    async def update_book(self, book_id: uuid.UUID | str, /, **kwargs) -> None: ...

    @abstractmethod
    async def delete_book(self, book_id: uuid.UUID | str) -> None: ...

    @abstractmethod
    async def get_list_by_category_id(self, category_id: int) -> list[BookDTO]: ...

    @abstractmethod
    async def get_list_by_author_id(self, author_id: int) -> list[BookDTO]: ...
