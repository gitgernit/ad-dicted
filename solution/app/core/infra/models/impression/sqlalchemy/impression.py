import uuid

import sqlalchemy as sa
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.infra.models.sqlalchemy import Base


class Impression(Base):
    __tablename__ = 'impressions'

    id: Mapped[uuid.UUID] = mapped_column(
        sa.Uuid,
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )

    day: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    cost: Mapped[float] = mapped_column(sa.Float, nullable=False)

    client_id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey('clients.id'),
        nullable=False,
    )
    campaign_id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey('campaigns.id'),
        nullable=False,
    )

    client = relationship('Client', back_populates='impressions')
    campaign = relationship('Campaign', back_populates='impressions')
