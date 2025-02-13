import uuid

from app.core.domain.client.entities.entities import Client
from app.core.domain.client.entities.repositories import ClientRepository
from app.core.domain.client.service.dto import ClientDTO


class ClientUsecase:
    def __init__(self, client_repository: ClientRepository) -> None:
        self.repository = client_repository

    async def create_client(self, dto: ClientDTO) -> ClientDTO:
        client = Client(**dto.model_dump())
        client = await self.repository.create_client(client)

        return ClientDTO(**client.model_dump())

    async def get_client(self, client_id: uuid.UUID) -> ClientDTO:
        client = await self.repository.get_client(client_id)

        return ClientDTO(**client.model_dump())
