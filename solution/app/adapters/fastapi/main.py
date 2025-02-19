import asyncio
import contextlib
import sys

import dishka.integrations.fastapi
import fastapi

import app.adapters.fastapi.api.routes
import app.core.config
import app.core.domain.advertiser.service.usecases
import app.core.domain.campaign.service.usecases
import app.core.domain.client.service.usecases
import app.core.domain.feed.service.usecases
import app.core.domain.options.service.dto
import app.core.domain.options.service.usecases
import app.core.domain.score.service.usecases
import app.core.domain.stats.service.usecases
import app.core.domain.storage.service.usecases
import app.core.infra.models.advertiser.sqlalchemy.repository as advertiser_repository
import app.core.infra.models.campaign.sqlalchemy.repository as campaign_repository
import app.core.infra.models.click.sqlalchemy.repository as clicks_repository
import app.core.infra.models.client.sqlalchemy.repository as client_repository
import app.core.infra.models.impression.sqlalchemy.repository as impressions_repository
import app.core.infra.models.options.sqlalchemy.repository as options_repository
import app.core.infra.models.score.sqlalchemy.repository as score_repository
import app.core.infra.models.sqlalchemy.providers as sqlalchemy_providers
import app.core.infra.moderation.yandexgpt as moderator_providers
import app.core.infra.storage.s3.repository as storage_providers
import app.core.infra.text_generators.yandexgpt as generator_providers
import app.core.infra.yandexgpt.interactors as yandexgpt_providers

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

container = dishka.make_async_container(
    dishka.integrations.fastapi.FastapiProvider(),
    client_repository.repository_provider,
    advertiser_repository.repository_provider,
    score_repository.repository_provider,
    campaign_repository.repository_provider,
    options_repository.repository_provider,
    impressions_repository.repository_provider,
    clicks_repository.repository_provider,
    app.core.domain.client.service.usecases.usecase_provider,
    app.core.domain.advertiser.service.usecases.usecase_provider,
    app.core.domain.score.service.usecases.usecase_provider,
    app.core.domain.campaign.service.usecases.usecase_provider,
    app.core.domain.options.service.usecases.usecase_provider,
    app.core.domain.feed.service.usecases.usecase_provider,
    app.core.domain.stats.service.usecases.usecase_provider,
    app.core.domain.storage.service.usecases.usecase_provider,
    sqlalchemy_providers.EngineProvider(app.core.config.psycopg_url),
    sqlalchemy_providers.SessionProvider(),
    yandexgpt_providers.InteractorProvider(
        catalog_identifier=app.core.config.config.YANDEX_GPT_CATALOG_IDENTIFIER,
        api_key=app.core.config.config.YANDEX_GPT_API_KEY,
    ),
    moderator_providers.moderator_provider,
    generator_providers.generator_provider,
    storage_providers.StorageProvider(
        app.core.config.config.S3_KEY_IDENTIFIER,
        app.core.config.config.S3_KEY,
        app.core.config.config.S3_BUCKET,
    ),
)


@contextlib.asynccontextmanager
async def lifespan(fastapi_app: fastapi.FastAPI) -> contextlib.asynccontextmanager:
    async with container() as request_container:
        options_usecase = await request_container.get(
            app.core.domain.options.service.usecases.OptionsUsecase,
        )
        day = await options_usecase.get_option(
            app.core.domain.options.service.dto.AvailableOptionsDTO.DAY,
        )

        if day is None:
            await options_usecase.set_option(
                app.core.domain.options.service.dto.OptionDTO(
                    option=app.core.domain.options.service.dto.AvailableOptionsDTO.DAY,
                    value=str(0),
                ),
            )

    yield
    await fastapi_app.state.dishka_container.close()


main_router = fastapi.APIRouter(
    route_class=dishka.integrations.fastapi.DishkaRoute,
)

fastapi_app = fastapi.FastAPI(lifespan=lifespan)

fastapi_app.include_router(main_router)
fastapi_app.include_router(app.adapters.fastapi.api.routes.api_router)

dishka.integrations.fastapi.setup_dishka(container, fastapi_app)
