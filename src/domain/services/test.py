from dependency_injector.wiring import Provide, inject

from src.di.container import UnitOfWork


@inject
async def blahblah(
    uow: UnitOfWork = Provide["uow"],
):
    async with uow.connection() as conn:
        async with conn.transaction():
            await conn.execute('select 1;')
