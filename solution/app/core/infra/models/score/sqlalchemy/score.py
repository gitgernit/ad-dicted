import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.infra.models.sqlalchemy import Base


class Score(Base):
    __tablename__ = 'score'

    client_id = sa.Column(
        UUID(as_uuid=True),
        sa.ForeignKey('clients.id'),
        primary_key=True,
        nullable=False,
    )
    advertiser_id = sa.Column(
        UUID(as_uuid=True),
        sa.ForeignKey('advertisers.id'),
        primary_key=True,
        nullable=False,
    )
    score = sa.Column(sa.Integer, nullable=False)

    client = relationship('Client', back_populates='score')
    advertiser = relationship('Advertiser', back_populates='score')
