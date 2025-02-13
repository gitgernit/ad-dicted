import enum
import uuid

import pydantic


class Gender(enum.StrEnum):
    MALE = 'male'
    FEMALE = 'female'


class Client(pydantic.BaseModel):
    id: uuid.UUID
    login: str
    age: int
    location: str
    gender: Gender
