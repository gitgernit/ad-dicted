import pytest

import app.core.config
from app.core.infra.moderation.yandexgpt import YandexGPTModerator
from app.core.infra.text_generators.yandexgpt import YandexGPTTextGenerator
from app.core.infra.yandexgpt.interactors import YandexGPTInteractor


@pytest.fixture
def yandex_gpt_interactor() -> YandexGPTInteractor:
    return YandexGPTInteractor(
        catalog_identifier=app.core.config.config.YANDEX_GPT_CATALOG_IDENTIFIER,
        api_key=app.core.config.config.YANDEX_GPT_API_KEY,
    )


@pytest.fixture
def yandex_gpt_text_generator(
    yandex_gpt_interactor: YandexGPTInteractor,
) -> YandexGPTTextGenerator:
    return YandexGPTTextGenerator(yandex_gpt_interactor=yandex_gpt_interactor)


@pytest.fixture
def yandex_gpt_moderator(
    yandex_gpt_interactor: YandexGPTInteractor,
) -> YandexGPTModerator:
    return YandexGPTModerator(yandex_gpt_interactor=yandex_gpt_interactor)
