from dependency_injector import containers, providers

from src.infra.dao.asyncpg_sqla.book import BookAsyncpgSQLADAO
from src.infra.repository.book import BookRepository


class BookRepositoryContainer(containers.DeclarativeContainer):
    _dao = providers.Singleton(
        BookAsyncpgSQLADAO,
    )
    repository = providers.Singleton(
        BookRepository,
        dao=_dao,
    )
