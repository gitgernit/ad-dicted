from dishka.integrations.fastapi import DishkaRoute
from dishka.integrations.fastapi import FromDishka
import fastapi

from app.adapters.fastapi.api.time.schemas import AdvanceSchema
from app.core.domain.options.service.dto import AvailableOptionsDTO
from app.core.domain.options.service.dto import OptionDTO
from app.core.domain.options.service.usecases import InvalidDayError
from app.core.domain.options.service.usecases import OptionsUsecase

time_router = fastapi.APIRouter(route_class=DishkaRoute)


@time_router.post('/advance')
async def advance_day(
    usecase: FromDishka[OptionsUsecase],
    advance_schema: AdvanceSchema,
) -> AdvanceSchema:
    dto = OptionDTO(
        option=AvailableOptionsDTO.DAY,
        value=str(advance_schema.current_date),
    )

    try:
        await usecase.set_option(dto)

    except InvalidDayError as error:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail='Invalid date passed.',
        ) from error

    return advance_schema
