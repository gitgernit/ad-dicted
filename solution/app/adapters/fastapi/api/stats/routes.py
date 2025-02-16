from dishka.integrations.fastapi import DishkaRoute
import fastapi

stats_router = fastapi.APIRouter(route_class=DishkaRoute)
