import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.infrastructure.models.sqlalchemy import Base


class Advertiser(Base):
    __tablename__ = 'advertisers'

    id: Mapped[uuid.UUID] = mapped_column(
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
