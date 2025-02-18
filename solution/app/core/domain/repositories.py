import abc


class StorageRepository(abc.ABC):
    @abc.abstractmethod
    def upload_file(
        self,
        content: bytes,
        content_type: str = 'application/octet-stream',
    ) -> str:
        pass

    @abc.abstractmethod
    def download_file(self, file_id: str) -> tuple[bytes, str]:
        pass
