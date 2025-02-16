import typing
import uuid

from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
import fastapi

import app.adapters.fastapi.api.advertisers.routes
import app.adapters.fastapi.api.clients.routes
from app.adapters.fastapi.api.schemas import CampaignOutputSchema
from app.adapters.fastapi.api.schemas import ScoreSchema
import app.adapters.fastapi.api.time.routes
from app.core.domain.feed.service.usecases import CampaignNotFoundError
from app.core.domain.feed.service.usecases import FeedUsecase
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


@api_router.get('/ads')
async def get_campaign(
    usecase: FromDishka[FeedUsecase],
    client_id: uuid.UUID,
) -> CampaignOutputSchema:
    try:
        best_campaign_dto = await usecase.get_best_campaign(client_id)

    except ClientNotFoundError as error:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail='Client not found.',
        ) from error

    except CampaignNotFoundError as error:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail='No campaign found.',
        ) from error

    return CampaignOutputSchema(
        ad_id=best_campaign_dto.id,
        advertiser_id=best_campaign_dto.advertiser_id,
        ad_title=best_campaign_dto.ad_title,
        ad_text=best_campaign_dto.ad_text,
    )


@api_router.post('/ads/{adId}/click', status_code=fastapi.status.HTTP_204_NO_CONTENT)
async def click_campaign(
    usecase: FromDishka[FeedUsecase],
    campaign_id: typing.Annotated[uuid.UUID, fastapi.Path(alias='adId')],
    client_id: typing.Annotated[uuid.UUID, fastapi.Body()],
) -> None:
    try:
        await usecase.click_campaign(client_id, campaign_id)

    except ClientNotFoundError as error:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail='Client not found.',
        ) from error

    except CampaignNotFoundError as error:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
            detail='No campaign found.',
        ) from error
