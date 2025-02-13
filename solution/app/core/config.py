import secrets

import pydantic
import pydantic_settings


class Config(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_file='.env',
        env_ignore_empty=True,
        extra='ignore',
    )

    POSTGRES_USERNAME: str = pydantic.Field(default='postgres')
    POSTGRES_PASSWORD: str = pydantic.Field(default='postgres')
    POSTGRES_HOST: str = pydantic.Field(default='localhost')
    POSTGRES_PORT: int = pydantic.Field(default=5432)
    POSTGRES_DATABASE: str = pydantic.Field(default='postgres')

    DEBUG: bool = pydantic.Field(default=False)


config = Config()

psycopg_url = f'postgresql+psycopg://{config.POSTGRES_USERNAME}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DATABASE}'
