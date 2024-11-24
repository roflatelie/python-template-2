from dependency_injector import containers, providers

from src.infra.dao.asyncpg_sqla.m2m_category_book import M2MCategoryBookAsyncpgSQLADAO
from src.infra.repository.m2m_category_book import M2MCategoryBookRepository


class M2MCategoryBookRepositoryContainer(containers.DeclarativeContainer):
    _dao = providers.Singleton(
        M2MCategoryBookAsyncpgSQLADAO,
    )
    repository = providers.Singleton(
        M2MCategoryBookRepository,
        dao=_dao,
    )
