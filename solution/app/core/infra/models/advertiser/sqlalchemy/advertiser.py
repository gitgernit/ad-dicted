import uuid

import sqlalchemy as sa
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.infra.models.sqlalchemy import Base


class Advertiser(Base):
    __tablename__ = 'advertisers'

    id: Mapped[uuid.UUID] = mapped_column(
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
    )
    name: Mapped[str] = mapped_column(sa.String, nullable=False)

    scores: Mapped[list['Score']] = relationship(
        'Score',
        back_populates='advertiser',
        cascade='all, delete-orphan',
    )
    campaigns: Mapped[list['Campaign']] = relationship(
        'Campaign',
        back_populates='advertiser',
        cascade='all, delete-orphan',
    )
