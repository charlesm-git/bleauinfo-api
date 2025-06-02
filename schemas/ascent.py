from datetime import date
from pydantic import BaseModel

from schemas.user import User


class Ascent(BaseModel):
    boulder_id: int
    user_id: int
    log_date: date

    class Config:
        from_attributes = True


class AscentRead(BaseModel):
    user: User
    log_date: date

    class Config:
        from_attributes = True


class AscentsPerMonth(BaseModel):
    month: str
    percentage: float

    class Config:
        from_attributes = True


class AscentsPerYear(BaseModel):
    year: int
    ascents: int

    class Config:
        from_attributes = True
