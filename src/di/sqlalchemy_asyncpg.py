from dependency_injector import containers, providers
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Tuple

import asyncpg
from sqlalchemy import ClauseElement
from sqlalchemy.dialects.postgresql.asyncpg import PGDialect_asyncpg
from src.settings import settings


class AsyncpgSqlaConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ASYNCPG_", env_file=".env", extra="ignore")
    DSN: str
    CONNECTION_TIMEOUT: float = 0.200  # 200ms
    MIN_POOL_SIZE: int = 1
    MAX_POOL_SIZE: int = 5
    POOL_TIMEOUT: float = 0.200  # 200ms


config = AsyncpgSqlaConfig()


async def _init_pg_pool():
    pool = await asyncpg.create_pool(
        # connection settings
        dsn=config.DSN,
        timeout=config.CONNECTION_TIMEOUT,
        connection_class=SQLAConnection,
        # pool settings
        min_size=config.MIN_POOL_SIZE,
        max_size=config.MAX_POOL_SIZE,
        # connection params
        server_settings={
            "application_name": settings.app.NAME,
            "timezone": "utc",
        },
    )
    yield pool

    await pool.close()


class AsyncpgSQLAContainer(containers.DeclarativeContainer):
    pool = providers.Resource(
        _init_pg_pool,
    )


def _compile(stmt: ClauseElement, dialect=PGDialect_asyncpg()) -> Tuple[str, list]:
    c = stmt.compile(dialect=dialect, compile_kwargs={"render_postcompile": True})
    return c.string, list(map(lambda key: c.params[key], c.positiontup))


class SQLAConnection(asyncpg.Connection):
    async def fetchval(self, query, *args, column=0, timeout=None):
        if isinstance(query, ClauseElement):
            query, args = _compile(query)
        return await super().fetchval(query, *args, timeout=timeout)

    async def fetchrow(self, query, *args, timeout=None, record_class=None):
        if isinstance(query, ClauseElement):
            query, args = _compile(query)
        return await super().fetchrow(query, *args, timeout=timeout, record_class=record_class)

    async def fetch(self, query: str | ClauseElement, *args, timeout=None, record_class=None) -> list:
        if isinstance(query, ClauseElement):
            query, args = _compile(query)
        return await super().fetch(query, *args, timeout=timeout, record_class=record_class)

    async def execute(self, query: str | ClauseElement, *args, timeout: float = None) -> str:
        if isinstance(query, ClauseElement):
            query, args = _compile(query)
        return await super().execute(query, *args, timeout=timeout)

    def cursor(
        self,
        query,
        *args,
        prefetch=None,
        timeout=None,
        record_class=None
    ):
        if isinstance(query, ClauseElement):
            query, args = _compile(query)
        return super().cursor(query, *args, prefetch=prefetch, timeout=timeout, record_class=record_class)
