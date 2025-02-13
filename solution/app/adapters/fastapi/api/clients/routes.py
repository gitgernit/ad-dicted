from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
import fastapi

from app.adapters.fastapi.api.clients.schemas import ClientSchema
from app.core.domain.client.service.dto import ClientDTO
from app.core.domain.client.service.usecases import ClientUsecase

client_router = fastapi.APIRouter(route_class=DishkaRoute)


@client_router.post('/bulk')
async def bulk_create_clients(
    usecase: FromDishka[ClientUsecase],
    clients: list[ClientSchema],
) -> list[ClientSchema]:
    created: list[ClientDTO] = []

    for client in clients:
        dto = ClientDTO(
            id=client.client_id,
            login=client.login,
            age=client.age,
            location=client.location,
            gender=client.gender,
        )

        created_dto = await usecase.create_client(dto, overwrite=True)
        created.append(created_dto)

    output = []

    for dto in created:
        schema = ClientSchema(
            client_id=dto.id,
            login=dto.login,
            age=dto.age,
            location=dto.location,
            gender=dto.gender,
        )
        output.append(schema)

    return output
