# pylint: disable=c-extension-no-member
import dataclasses
from contextlib import asynccontextmanager
# import os
# import pathlib
from typing import Any

from dependency_injector import containers, providers

from .file_storage import FileStorageContainer
from .author import AuthorRepositoryContainer
from .book import BookRepositoryContainer
from .category import CategoryRepositoryContainer
from .m2m_author_book import M2MAuthorBookRepositoryContainer
from .m2m_category_book import M2MCategoryBookRepositoryContainer
from src.di.sqlalchemy_asyncpg import AsyncpgSQLAContainer, config as pg_config
from src.domain.interface.author import IAuthorDAO
from src.domain.interface.book import IBookDAO
from src.domain.interface.category import ICategoryDAO
from src.domain.interface.m2m_author_book import IM2MAuthorBookDAO
from src.domain.interface.m2m_category_book import IM2MCategoryBookDAO
from src.domain.interface.storage import IStorageDAO
from src.vars import PGConnection


@dataclasses.dataclass
class UnitOfWork:
    pg_pool: Any
    book: IBookDAO
    author: IAuthorDAO
    category: ICategoryDAO
    m2m_author_book: IM2MAuthorBookDAO
    m2m_category_book: IM2MCategoryBookDAO
    storage: IStorageDAO

    @asynccontextmanager
    async def connection(self):
        async with self.pg_pool.acquire(timeout=pg_config.POOL_TIMEOUT) as conn:
            _token = PGConnection.set(conn)
            yield conn
            PGConnection.reset(_token)


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "src.domain",
        ],
    )

    _pg_connection_pool = providers.Container(
        AsyncpgSQLAContainer,
    )

    _book_repository = providers.Container(BookRepositoryContainer)
    _author_repository = providers.Container(AuthorRepositoryContainer)
    _category_repository = providers.Container(CategoryRepositoryContainer)
    _m2m_author_book_repository = providers.Container(M2MAuthorBookRepositoryContainer)
    _m2m_category_book_repository = providers.Container(M2MCategoryBookRepositoryContainer)
    _file_storage = providers.Container(FileStorageContainer)

    uow = providers.Factory(
        UnitOfWork,
        pg_pool=_pg_connection_pool.pool,
        book=_book_repository.repository,
        author=_author_repository.repository,
        category=_category_repository.repository,
        m2m_author_book=_m2m_author_book_repository.repository,
        m2m_category_book=_m2m_category_book_repository.repository,
        storage=_file_storage.repository,
    )


async def init_container(**kwargs) -> Container:
    defaults = {
        **kwargs,
    }
    container = Container(**defaults)
    await container.init_resources()
    return container
