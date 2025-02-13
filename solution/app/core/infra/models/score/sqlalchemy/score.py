import uuid

import sqlalchemy as sa
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.infra.models.sqlalchemy import Base


class Score(Base):
    __tablename__ = 'score'

    client_id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey('clients.id'),
        primary_key=True,
        nullable=False,
    )
    advertiser_id: Mapped[uuid.UUID] = mapped_column(
        sa.ForeignKey('advertisers.id'),
        primary_key=True,
        nullable=False,
    )
    score: Mapped[int] = mapped_column(sa.Integer, nullable=False)

    client = relationship('Client', back_populates='score')
    advertiser = relationship('Advertiser', back_populates='score')
