import hashlib
import os.path
from abc import ABC, abstractmethod
from pathlib import Path


class IStorageDAO(ABC):
    @abstractmethod
    async def save_file(self, file: Path, bucket: str, key: str) -> str: ...

    @abstractmethod
    async def delete(self, key: str) -> None: ...

    @abstractmethod
    async def exists(self, key: str) -> bool: ...

    async def get_file_ext(self, file: Path) -> str:
        _, ext = os.path.splitext(file)
        return ext

    async def generate_hash(self, file: Path) -> str:
        # TODO: you don't belong here
        md5sum = hashlib.md5()
        with open(file, "rb") as fp:
            while chunk := fp.read(4096):
                md5sum.update(chunk)
        return md5sum.hexdigest()
