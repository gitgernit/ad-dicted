import uuid

import pytest
from app.core.domain.campaign.service.usecases import CampaignUsecase
from app.core.domain.campaign.service.dto import CampaignDTO, TargetingDTO


@pytest.mark.asyncio
class TestCampaignsUsecase:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, campaign_usecase: UserWarning):
        self.usecase = campaign_usecase
