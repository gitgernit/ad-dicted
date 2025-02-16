import uuid

import dishka

from app.core.domain.campaign.entities.repositories import CampaignRepository
from app.core.domain.feed.entities.repositories import ClicksRepository
from app.core.domain.feed.entities.repositories import ImpressionsRepository
from app.core.domain.options.entities.entities import AvailableOptions
from app.core.domain.options.entities.repositories import OptionsRepository
from app.core.domain.stats.service.dto import CampaignStatsDTO


class CampaignNotFoundError(Exception):
    def __init__(self) -> None:
        super().__init__('No such campaign found.')


class StatsUsecase:
    def __init__(
        self,
        campaign_repository: CampaignRepository,
        options_repository: OptionsRepository,
        impressions_repository: ImpressionsRepository,
        clicks_repository: ClicksRepository,
    ) -> None:
        self.campaign_repository = campaign_repository
        self.options_repository = options_repository
        self.impressions_repository = impressions_repository
        self.clicks_repository = clicks_repository

    async def get_campaign_stats_by_day(
        self,
        campaign_id: uuid.UUID,
        day: int,
    ) -> CampaignStatsDTO:
        if await self.campaign_repository.get_campaign(campaign_id) is None:
            raise CampaignNotFoundError

        impressions = await self.impressions_repository.get_campaign_impressions(
            campaign_id,
            day,
        )
        clicks = await self.clicks_repository.get_campaign_clicks(campaign_id, day)

        conversion = len(clicks) / len(impressions) * 100

        spent_impressions = 0
        spent_clicks = 0

        for impression in impressions:
            spent_impressions += impression.cost

        for click in clicks:
            spent_clicks += click.cost

        spent_total = spent_impressions + spent_clicks

        return CampaignStatsDTO(
            impressions_count=len(impressions),
            clicks_count=len(clicks),
            conversion=conversion,
            spent_impressions=spent_impressions,
            spent_clicks=spent_clicks,
            spent_total=spent_total,
        )

    async def get_daily_campaign_stats(
        self,
        campaign_id: uuid.UUID,
    ) -> list[CampaignStatsDTO]:
        current_day = int(
            (await self.options_repository.get_option(AvailableOptions.DAY)).value,
        )
        stats: list[CampaignStatsDTO] = [
            await self.get_campaign_stats_by_day(campaign_id, day)
            for day in range(current_day + 1)
        ]

        return stats

    async def get_total_campaign_stats(
        self,
        campaign_id: uuid.UUID,
    ) -> CampaignStatsDTO:
        stats = await self.get_daily_campaign_stats(campaign_id)
        total_stats = CampaignStatsDTO(
            impressions_count=0,
            clicks_count=0,
            conversion=0,
            spent_impressions=0,
            spent_clicks=0,
            spent_total=0,
        )

        for stat in stats:
            total_stats.impressions_count += stat.impressions_count
            total_stats.clicks_count += stat.clicks_count

            total_stats.spent_impressions += stat.spent_impressions
            total_stats.spent_clicks += stat.spent_clicks

        total_stats.conversion = (
            total_stats.clicks_count / total_stats.impressions_count * 100
        )
        total_stats.spent_total = (
            total_stats.spent_clicks + total_stats.spent_impressions
        )

        return total_stats


usecase_provider = dishka.Provider(scope=dishka.Scope.REQUEST)
usecase_provider.provide(StatsUsecase)
