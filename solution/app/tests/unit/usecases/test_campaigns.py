import pytest


@pytest.mark.asyncio
class TestCampaignsUsecase:
    @pytest.fixture(autouse=True)
    def setup(self, campaign_usecase: UserWarning) -> None:
        self.usecase = campaign_usecase
