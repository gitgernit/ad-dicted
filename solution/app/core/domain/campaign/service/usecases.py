import uuid

import dishka

from app.core.domain.campaign.entities.entities import Campaign
from app.core.domain.campaign.entities.repositories import CampaignRepository
from app.core.domain.campaign.service.dto import CampaignDTO


class CampaignUsecase:
    def __init__(self, campaign_repository: CampaignRepository) -> None:
        self.campaign_repository = campaign_repository

    async def create_campaign(
        self,
        dto: CampaignDTO,
        *,
        overwrite: bool = False,
    ) -> CampaignDTO:
        campaign = Campaign(
            impressions_limit=dto.impressions_limit,
            clicks_limit=dto.clicks_limit,
            cost_per_impression=dto.cost_per_impression,
            cost_per_click=dto.cost_per_click,
            ad_title=dto.ad_title,
            ad_text=dto.ad_text,
            start_date=dto.start_date,
            end_date=dto.end_date,
            advertiser_id=dto.advertiser_id,
        )
        new_campaign = await self.campaign_repository.create_campaign(
            campaign,
            overwrite=overwrite,
        )

        return CampaignDTO(
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

    async def get_campaign(self, campaign_id: uuid.UUID) -> CampaignDTO:
        campaign = await self.campaign_repository.get_campaign(campaign_id)

        return CampaignDTO(
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

    async def patch_campaign(
        self,
        campaign_id: uuid.UUID,
        new_campaign_dto: CampaignDTO,
    ) -> CampaignDTO:
        campaign = Campaign(
            impressions_limit=new_campaign_dto.impressions_limit,
            clicks_limit=new_campaign_dto.clicks_limit,
            cost_per_impression=new_campaign_dto.cost_per_impression,
            cost_per_click=new_campaign_dto.cost_per_click,
            ad_title=new_campaign_dto.ad_title,
            ad_text=new_campaign_dto.ad_text,
            start_date=new_campaign_dto.start_date,
            end_date=new_campaign_dto.end_date,
            advertiser_id=new_campaign_dto.advertiser_id,
        )
        existing_campaign = await self.campaign_repository.get_campaign(campaign_id)

        campaign_dict = campaign.model_dump()
        existing_campaign_dict = existing_campaign.model_dump(
            exclude_none=True,
            exclude_unset=True,
        )

        new_campaign_dict = campaign_dict | existing_campaign_dict
        new_campaign = Campaign(**new_campaign_dict)

        new_campaign = await self.campaign_repository.create_campaign(
            new_campaign,
            overwrite=True,
        )

        return CampaignDTO(
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

    async def delete_campaign(self, campaign_id: uuid.UUID) -> None:
        await self.campaign_repository.delete_campaign(campaign_id)

    async def get_advertiser_campaigns(
        self,
        advertiser_id: uuid.UUID,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[CampaignDTO]:
        campaigns = await self.campaign_repository.get_advertiser_campaigns(
            advertiser_id=advertiser_id,
            limit=limit,
            offset=offset,
        )

        return [
            CampaignDTO(
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


usecase_provider = dishka.Provider(scope=dishka.Scope.REQUEST)
usecase_provider.provide(CampaignUsecase)
