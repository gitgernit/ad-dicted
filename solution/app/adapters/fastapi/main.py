import contextlib

import dishka.integrations.fastapi
import fastapi

import app.adapters.fastapi.api.routes
import app.core.config
import app.core.domain.client.service.usecases
import app.core.infrastructure.models.client.sqlalchemy.repository as client_repository
import app.core.infrastructure.models.sqlalchemy.providers as sqlalchemy_providers

container = dishka.make_async_container(
    dishka.integrations.fastapi.FastapiProvider(),
    client_repository.repository_provider,
    app.core.domain.client.service.usecases.usecase_provider,
    sqlalchemy_providers.EngineProvider(app.core.config.psycopg_url),
    sqlalchemy_providers.SessionProvider(),
)


@contextlib.asynccontextmanager
async def lifespan(app: fastapi.FastAPI) -> contextlib.asynccontextmanager:
    yield
    await app.state.dishka_container.close()


main_router = fastapi.APIRouter(
    route_class=dishka.integrations.fastapi.DishkaRoute,
)

fastapi_app = fastapi.FastAPI(lifespan=lifespan)

fastapi_app.include_router(main_router)
fastapi_app.include_router(app.adapters.fastapi.api.routes.api_router)

dishka.integrations.fastapi.setup_dishka(container, fastapi_app)
