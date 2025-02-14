import enum
import uuid

import pydantic


class Gender(enum.StrEnum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    ALL = 'ALL'


class TargetingSchema(pydantic.BaseModel):
    gender: Gender | None = pydantic.Field(default=None)
    age_from: int | None = pydantic.Field(default=None)
    age_to: int | None = pydantic.Field(default=None)
    location: str | None = pydantic.Field(default=None)


class CampaignInputSchema(pydantic.BaseModel):
    impressions_limit: int
    clicks_limit: int

    cost_per_impression: float
    cost_per_click: float

    ad_title: str
    ad_text: str

    start_date: int
    end_date: int

    targeting: TargetingSchema | None = pydantic.Field(default=None)


class CampaignOutputSchema(CampaignInputSchema):
    campaign_id: uuid.UUID
    advertiser_id: uuid.UUID


class CampaignPatchSchema(pydantic.BaseModel):
    impressions_limit: int | None = pydantic.Field(default=None)
    clicks_limit: int | None = pydantic.Field(default=None)

    cost_per_impression: float | None = pydantic.Field(default=None)
    cost_per_click: float | None = pydantic.Field(default=None)

    ad_title: str | None = pydantic.Field(default=None)
    ad_text: str | None = pydantic.Field(default=None)

    start_date: int | None = pydantic.Field(default=None)
    end_date: int | None = pydantic.Field(default=None)

    targeting: TargetingSchema | None = pydantic.Field(default=None)
