import datetime
import enum
import uuid

import sqlalchemy as sa
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.infra.models.sqlalchemy import Base


class Gender(enum.Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'


class Client(Base):
    __tablename__ = 'clients'

    id: Mapped[uuid.UUID] = mapped_column(
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
    )
    login: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)
    age: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    location: Mapped[str] = mapped_column(sa.String, nullable=False)
    gender: Mapped[Gender] = mapped_column(sa.Enum(Gender), nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.sql.func.now(),
    )

    scores: Mapped[list['Score']] = relationship(
        'Score',
        back_populates='client',
        cascade='all, delete-orphan',
    )
