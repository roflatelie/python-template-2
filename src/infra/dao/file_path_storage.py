import shutil
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from src.domain.interface.storage import IStorageDAO


class FilePathStorageConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="FP_STORAGE_", env_file=".env", extra="ignore")
    ROOT: str = "/www/media"


_config = FilePathStorageConfig()
_root = Path(_config.ROOT)


class FilePathStorageDAO(IStorageDAO):
    async def exists(self, key: str) -> bool:
        return Path(f"{_root}/{key}").exists()

    async def save_file(self, file: Path, bucket: str, key: str) -> str:
        shutil.copy(
            file,
            _root / bucket / key,
        )
        return f"/{bucket}/{key}"

    async def delete(self, key: str) -> None:
        if await self.exists(key):
            Path(f"{_root}/{key}").unlink()
