from dependency_injector import containers, providers

from src.infra.dao.file_path_storage import FilePathStorageDAO
from src.infra.repository.storage import StorageRepository


class FileStorageContainer(containers.DeclarativeContainer):
    _dao = providers.Singleton(
        FilePathStorageDAO,
    )
    repository = providers.Singleton(
        StorageRepository,
        dao=_dao,
    )
