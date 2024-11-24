from src.vars import PGConnection


async def fetch(stmt):
    conn = PGConnection.get()
    return await conn.fetch(stmt)


async def fetchval(stmt):
    conn = PGConnection.get()
    return await conn.fetchval(stmt)


async def fetchrow(stmt):
    conn = PGConnection.get()
    return await conn.fetchrow(stmt)


async def execute(stmt):
    conn = PGConnection.get()
    # prevent autocommit
    assert conn.is_in_transaction()
    return await conn.execute(stmt)

# async def executemany(stmt):
#     conn = PGConnection.get()
#     assert conn.is_in_transaction()
#     return await conn.executemany(stmt)
