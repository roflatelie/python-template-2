import msgspec


class AuthorDTO(msgspec.Struct, kw_only=True):
    id: int
    name: str
