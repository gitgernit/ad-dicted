from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
import fastapi

from app.adapters.fastapi.api.advertisers.schemas import AdvertiserSchema
from app.core.domain.advertiser.service.dto import AdvertiserDTO
from app.core.domain.advertiser.service.usecases import AdvertiserUsecase

advertisers_router = fastapi.APIRouter(
    route_class=DishkaRoute,
)


@advertisers_router.post('/bulk', status_code=fastapi.status.HTTP_201_CREATED)
async def bulk_create_advertisers(
    usecase: FromDishka[AdvertiserUsecase],
    advertisers: list[AdvertiserSchema],
) -> list[AdvertiserSchema]:
    dtos: list[AdvertiserDTO] = []

    for advertiser in advertisers:
        dto = AdvertiserDTO(
            id=advertiser.advertiser_id,
            name=advertiser.name,
        )

        new_dto = await usecase.create_advertiser(dto, overwrite=True)
        dtos.append(new_dto)

    return [
        AdvertiserSchema(
            advertiser_id=dto.id,
            name=dto.name,
        )
        for dto in dtos
    ]
