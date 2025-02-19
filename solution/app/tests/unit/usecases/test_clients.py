import uuid

import pytest
from app.core.domain.client.service.usecases import ClientUsecase
from app.core.domain.client.service.dto import ClientDTO, Gender


@pytest.mark.asyncio
class TestClientsUsecase:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, client_usecase: ClientUsecase):
        self.usecase = client_usecase

    async def test_create_client(self):
        client_dto = ClientDTO(
            id=uuid.uuid4(),
            login='john_doe',
            age=16,
            location='Moscow',
            gender=Gender.MALE,
        )

        await self.usecase.create_client(client_dto)
        client = await self.usecase.get_client(client_dto.id)

        assert client is not None
        assert client.login == client_dto.login
        assert client.age == client_dto.age
        assert client.location == client_dto.location
        assert client.gender == client_dto.gender
