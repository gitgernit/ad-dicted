import dishka
import sqlalchemy.ext.asyncio


class EngineProvider(dishka.Provider):
    scope = dishka.Scope.APP

    @dishka.provide
    async def get_engine(self, uri: str) -> sqlalchemy.ext.asyncio.engine:
        return sqlalchemy.ext.asyncio.create_async_engine(url=uri)


class SessionProvider(dishka.Provider):
    scope = dishka.Scope.REQUEST

    @dishka.provide
    async def get_async_session_factory(
        self,
        engine: sqlalchemy.ext.asyncio.engine,
    ) -> sqlalchemy.ext.asyncio.async_sessionmaker[
        sqlalchemy.ext.asyncio.AsyncSession
    ]:
        return sqlalchemy.ext.asyncio.async_sessionmaker(bind=engine)
