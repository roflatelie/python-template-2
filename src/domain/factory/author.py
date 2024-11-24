import factory

from src.domain.dto.author import AuthorDTO


class AuthorDTOFactory(factory.Factory):
    class Meta:
        model = AuthorDTO

    id = factory.Sequence(int)
    name = factory.Sequence(str)
