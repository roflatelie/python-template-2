from dependency_injector import containers, providers

from src.infra.dao.asyncpg_sqla.category import CategoryAsyncpgSQLADAO
from src.infra.repository.category import CategoryRepository


class CategoryRepositoryContainer(containers.DeclarativeContainer):
    _dao = providers.Singleton(
        CategoryAsyncpgSQLADAO,
    )
    repository = providers.Singleton(
        CategoryRepository,
        dao=_dao,
    )
