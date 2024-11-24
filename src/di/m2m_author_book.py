from dependency_injector import containers, providers

from src.infra.dao.asyncpg_sqla.m2m_author_book import M2MAuthorBookAsyncpgSQLADAO
from src.infra.repository.m2m_author_book import M2MAuthorBookRepository


class M2MAuthorBookRepositoryContainer(containers.DeclarativeContainer):
    _dao = providers.Singleton(
        M2MAuthorBookAsyncpgSQLADAO,
    )
    repository = providers.Singleton(
        M2MAuthorBookRepository,
        dao=_dao,
    )
