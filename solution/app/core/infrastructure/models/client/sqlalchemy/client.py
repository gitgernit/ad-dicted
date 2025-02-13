import enum
import uuid

from sqlalchemy import Enum
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.infrastructure.models.sqlalchemy import Base


class Gender(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'


class Client(Base):
    __tablename__ = 'clients'

    id: Mapped[uuid.UUID] = mapped_column(
        default=uuid.uuid4,
        primary_key=True,
        unique=True,
    )
    login: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)
    gender: Mapped[Gender] = mapped_column(Enum(Gender), nullable=False)
