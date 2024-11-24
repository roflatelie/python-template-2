from pathlib import Path

from src.domain.interface.storage import IStorageDAO


class StorageRepository(IStorageDAO):
    def __init__(self, dao: IStorageDAO):
        self._dao = dao

    async def save_file(self, file: Path, bucket: str, key: str) -> str:
        return await self._dao.save_file(file, bucket, key)

    async def exists(self, key: str) -> bool:
        return await self._dao.exists(key)

    async def delete(self, key: str) -> None:
        return await self._dao.delete(key)

    async def generate_hash(self, file: Path) -> str:
        return await self._dao.generate_hash(file)

    async def get_file_ext(self, file: Path) -> str:
        return await self._dao.get_file_ext(file)
