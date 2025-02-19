import os
import uuid
import aiofiles
from app.core.infra.storage.s3.repository import StorageRepository


class FilesystemStorageRepository(StorageRepository):
    def __init__(self, base_path: str) -> None:
        self.base_path = base_path

        os.makedirs(self.base_path, exist_ok=True)

    async def upload_file(self, content: bytes, content_type: str = 'application/octet-stream') -> str:
        file_id = str(uuid.uuid4())
        file_path = os.path.join(self.base_path, file_id)

        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)

        return file_id

    async def download_file(self, file_id: str) -> tuple[bytes, str]:
        file_path = os.path.join(self.base_path, file_id)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File with ID {file_id} not found.")

        async with aiofiles.open(file_path, 'rb') as f:
            content = await f.read()

        return content, 'application/octet-stream'
