from dependency_injector import containers, providers

from src.infra.dao.asyncpg_sqla.author import AuthorAsyncpgSQLADAO
from src.infra.repository.author import AuthorRepository


class AuthorRepositoryContainer(containers.DeclarativeContainer):
    _dao = providers.Singleton(
        AuthorAsyncpgSQLADAO,
    )
    repository = providers.Singleton(
        AuthorRepository,
        dao=_dao,
    )
