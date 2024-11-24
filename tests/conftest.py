import pytest
from alembic.command import downgrade as alembic_downgrade
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig

from src.di.container import Container, UnitOfWork, init_container


@pytest.fixture
async def pg_container(event_loop, container: Container) -> Container:  # pylint: disable=unused-argument
    """Fixture for migrations."""
    config = AlembicConfig("alembic.ini")
    alembic_upgrade(config, "head")

    container = await init_container()

    yield container

    await container.shutdown_resources()

    alembic_downgrade(config, "base")


@pytest.fixture
async def container() -> Container:
    container = await init_container()
    yield container
    await container.shutdown_resources()


@pytest.fixture
async def uow(container: Container) -> UnitOfWork:
    return await container.uow()
