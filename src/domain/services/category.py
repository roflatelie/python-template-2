from dependency_injector.wiring import Provide, inject

from src.di.container import UnitOfWork
from src.domain.dto.category import CategoryDTO


@inject
async def create_category(
    name: str,
    parent_id: int = None,
    uow: UnitOfWork = Provide["uow"],
) -> CategoryDTO:
    async with uow.connection():
        return await uow.category.create(name, parent_id)


@inject
async def get_category_list(
    uow: UnitOfWork = Provide["uow"],
) -> list[CategoryDTO]:
    async with uow.connection() as conn:
        async with conn.transaction():
            return await uow.category.get_list()


@inject
async def get_default_category(
    uow: UnitOfWork = Provide["uow"],
) -> int:
    async with uow.connection():
        return await uow.category.get_default_category_id()
