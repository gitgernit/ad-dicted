import dishka.integrations.fastapi
import fastapi

import app.adapters.fastapi.api.advertisers.routes
import app.adapters.fastapi.api.clients.routes

api_router = fastapi.APIRouter(
    route_class=dishka.integrations.fastapi.DishkaRoute,
)

api_router.include_router(
    app.adapters.fastapi.api.clients.routes.clients_router,
    prefix='/clients',
)
api_router.include_router(
    app.adapters.fastapi.api.advertisers.routes.advertisers_router,
    prefix='/advertisers',
)
