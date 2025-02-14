import uuid

import sqlalchemy as sa
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.infra.models.sqlalchemy import Base


class Campaign(Base):
    __tablename__ = 'campaigns'

    id: Mapped[uuid.UUID] = mapped_column(sa.UUID, primary_key=True, default=uuid.uuid4)

    impressions_limit: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    clicks_limit: Mapped[int] = mapped_column(sa.Integer, nullable=False)

    cost_per_impression: Mapped[float] = mapped_column(sa.Float, nullable=False)
    cost_per_click: Mapped[float] = mapped_column(sa.Float, nullable=False)

    ad_title: Mapped[str] = mapped_column(sa.String, nullable=False)
    ad_text: Mapped[str] = mapped_column(sa.Text, nullable=False)

    start_date: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    end_date: Mapped[int] = mapped_column(sa.Integer, nullable=False)

    advertiser_id: Mapped[uuid.UUID] = mapped_column(
        sa.UUID,
        sa.ForeignKey('advertisers.id'),
        nullable=False,
    )
    advertiser: Mapped['Advertiser'] = relationship(
        'Advertiser',
        back_populates='campaigns',
    )
