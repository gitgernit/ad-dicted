import uuid

import dishka

from app.core.domain.advertisers.entities.entities import Advertiser as DomainAdvertiser

if __name__ == '__main__':
    from app.core.infrastructure.models.advertiser.sqlalchemy.advertiser import (
        Advertiser,
    )

import sqlalchemy.ext.asyncio

from app.core.domain.advertisers.entities.repositories import AdvertiserRepository


class SQLAlchemyAdvertiserRepository(AdvertiserRepository):
    def __init__(
        self,
        session_factory: sqlalchemy.ext.asyncio.async_sessionmaker[
            sqlalchemy.ext.asyncio.AsyncSession
        ],
    ) -> None:
        self._session_factory = session_factory

    async def create_advertiser(
        self,
        advertiser: DomainAdvertiser,
        *,
        overwrite: bool = False,
    ) -> DomainAdvertiser:
        async with self._session_factory() as session, session.begin():
            new_advertiser = Advertiser(
                id=advertiser.id,
                name=advertiser.name,
            )

            if overwrite:
                new_advertiser = await session.merge(new_advertiser)

            session.add(new_advertiser)

            await session.flush()
            session.expunge_all()

            return DomainAdvertiser(
                id=new_advertiser.id,
                name=new_advertiser.name,
            )

    async def get_advertiser(self, advertiser_id: uuid.UUID) -> DomainAdvertiser | None:
        async with self._session_factory() as session, session.begin():
            stmt = sqlalchemy.select(Advertiser).where(Advertiser.id == advertiser_id)
            result = await session.execute(stmt)

            session.expunge_all()

            advertiser = result.scalars().first()

            if advertiser is None:
                return None

            return DomainAdvertiser(
                id=advertiser.id,
                name=advertiser.name,
            )


repository_provider = dishka.Provider(scope=dishka.Scope.REQUEST)
repository_provider.provide(
    SQLAlchemyAdvertiserRepository,
    provides=AdvertiserRepository,
)
