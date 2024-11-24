import uuid

import msgspec

from src.domain.dto.author import AuthorDTO
from src.domain.dto.category import CategoryDTO


class BookDTO(msgspec.Struct, kw_only=True):
    id: uuid.UUID
    title: str
    ext: str
    file: str
    cover: str


class BookAggregateDTO(msgspec.Struct, kw_only=True):
    book: BookDTO
    authors: list[AuthorDTO]
    categories: list[CategoryDTO]
    categories_id: list[int]
