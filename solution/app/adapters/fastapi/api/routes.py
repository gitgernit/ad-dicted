from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
import fastapi

import app.adapters.fastapi.api.advertisers.routes
import app.adapters.fastapi.api.clients.routes
from app.adapters.fastapi.api.schemas import ScoreSchema
import app.adapters.fastapi.api.time.routes
from app.core.domain.score.service.dto import ScoreDTO
from app.core.domain.score.service.usecases import AdvertiserNotFoundError
from app.core.domain.score.service.usecases import ClientNotFoundError
from app.core.domain.score.service.usecases import ScoreUsecase

api_router = fastapi.APIRouter(
    route_class=DishkaRoute,
)

api_router.include_router(
    app.adapters.fastapi.api.clients.routes.clients_router,
    prefix='/clients',
)
api_router.include_router(
    app.adapters.fastapi.api.advertisers.routes.advertisers_router,
    prefix='/advertisers',
)
api_router.include_router(
    app.adapters.fastapi.api.time.routes.time_router,
    prefix='/time',
)


@api_router.post('/ml-scores')
async def create_score(
    usecase: FromDishka[ScoreUsecase],
    score: ScoreSchema,
) -> None:
    dto = ScoreDTO(
        client_id=score.client_id,
        advertiser_id=score.advertiser_id,
        score=score.score,
    )

    try:
        await usecase.create_score(dto, overwrite=True)

    except ClientNotFoundError as error:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail='No such client.',
        ) from error

    except AdvertiserNotFoundError as error:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail='No such advertiser.',
        ) from error
