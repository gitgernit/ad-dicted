import uuid

import dishka
import sqlalchemy.ext.asyncio

from app.core.domain.campaign.entities.entities import Campaign as DomainCampaign
from app.core.domain.campaign.entities.repositories import CampaignRepository
from app.core.infra.models.campaign.sqlalchemy.campaign import Campaign


class SQLAlchemyCampaignRepository(CampaignRepository):
    def __init__(
        self,
        session_factory: sqlalchemy.ext.asyncio.async_sessionmaker[
            sqlalchemy.ext.asyncio.AsyncSession
        ],
    ) -> None:
        self._session_factory = session_factory

    async def create_campaign(
        self,
        campaign: DomainCampaign,
        *,
        overwrite: bool = False,
    ) -> DomainCampaign:
        async with self._session_factory() as session, session.begin():
            new_campaign = Campaign(
                impressions_limit=campaign.impressions_limit,
                clicks_limit=campaign.clicks_limit,
                cost_per_impression=campaign.cost_per_impression,
                cost_per_click=campaign.cost_per_click,
                ad_title=campaign.ad_title,
                ad_text=campaign.ad_text,
                start_date=campaign.start_date,
                end_date=campaign.end_date,
                advertiser_id=campaign.advertiser_id,
            )

            if overwrite:
                new_campaign = await session.merge(new_campaign)

            session.add(new_campaign)

            await session.flush()
            session.expunge_all()

            return DomainCampaign(
                id=new_campaign.id,
                impressions_limit=new_campaign.impressions_limit,
                clicks_limit=new_campaign.clicks_limit,
                cost_per_impression=new_campaign.cost_per_impression,
                cost_per_click=new_campaign.cost_per_click,
                ad_title=new_campaign.ad_title,
                ad_text=new_campaign.ad_text,
                start_date=new_campaign.start_date,
                end_date=new_campaign.end_date,
                advertiser_id=new_campaign.advertiser_id,
            )

    async def get_campaign(self, campaign_id: uuid.UUID) -> DomainCampaign | None:
        async with self._session_factory() as session, session.begin():
            stmt = sqlalchemy.select(Campaign).where(Campaign.id == campaign_id)
            result = await session.execute(stmt)

            campaign = result.scalars().first()

            if campaign is None:
                return None

            return DomainCampaign(
                id=campaign.id,
                impressions_limit=campaign.impressions_limit,
                clicks_limit=campaign.clicks_limit,
                cost_per_impression=campaign.cost_per_impression,
                cost_per_click=campaign.cost_per_click,
                ad_title=campaign.ad_title,
                ad_text=campaign.ad_text,
                start_date=campaign.start_date,
                end_date=campaign.end_date,
                advertiser_id=campaign.advertiser_id,
            )

    async def delete_campaign(self, campaign_id: uuid.UUID) -> None:
        async with self._session_factory() as session, session.begin():
            campaign = await session.get(Campaign, campaign_id)
            await session.delete(campaign)

            await session.flush()

    async def get_advertiser_campaigns(
        self,
        advertiser_id: uuid.UUID,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[DomainCampaign]:
        async with self._session_factory() as session, session.begin():
            stmt = (
                sqlalchemy.select(Campaign)
                .where(Campaign.advertiser_id == advertiser_id)
                .offset(offset)
                .limit(limit)
            )

            result = await session.execute(stmt)
            campaigns = result.scalars().all()

            return [
                DomainCampaign(
                    id=campaign.id,
                    impressions_limit=campaign.impressions_limit,
                    clicks_limit=campaign.clicks_limit,
                    cost_per_impression=campaign.cost_per_impression,
                    cost_per_click=campaign.cost_per_click,
                    ad_title=campaign.ad_title,
                    ad_text=campaign.ad_text,
                    start_date=campaign.start_date,
                    end_date=campaign.end_date,
                    advertiser_id=campaign.advertiser_id,
                )
                for campaign in campaigns
            ]


repository_provider = dishka.Provider(scope=dishka.Scope.REQUEST)
repository_provider.provide(SQLAlchemyCampaignRepository, provides=CampaignRepository)
