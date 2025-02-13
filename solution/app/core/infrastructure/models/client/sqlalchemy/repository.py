import uuid

import dishka
from app.core.domain.client.entities.entities import Client
from app.core.domain.client.entities.repositories import ClientRepository

import sqlalchemy.ext.asyncio


class SQLAlchemyClientRepository(ClientRepository):
    def __init__(
        self,
        session_factory: sqlalchemy.ext.asyncio.async_sessionmaker[
            sqlalchemy.ext.asyncio.AsyncSession
        ],
    ) -> None:
        self._session_factory = session_factory

    async def create_client(self, client: Client) -> Client:
        pass

    async def get_client(self, client_id: uuid.UUID) -> Client:
        pass


repository_provider = dishka.Provider(scope=dishka.Scope.REQUEST)
repository_provider.provide(
    SQLAlchemyClientRepository, provides=ClientRepository
)
