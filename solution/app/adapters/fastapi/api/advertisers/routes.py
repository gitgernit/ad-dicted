import dishka.integrations.fastapi
import fastapi

advertisers_router = fastapi.APIRouter(
    route_class=dishka.integrations.fastapi.DishkaRoute,
)
