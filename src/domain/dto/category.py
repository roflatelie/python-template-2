import msgspec


class CategoryDTO(msgspec.Struct, kw_only=True):
    id: int
    name: str
    parent_id: int | None = None
