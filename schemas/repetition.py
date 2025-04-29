from datetime import date
from pydantic import BaseModel

from schemas.user import User


class Repetition(BaseModel):
    boulder_id: int
    user_id: int
    log_date: date

    class Config:
        from_attributes = True


class RepetitionRead(BaseModel):
    user: User
    log_date: date

    class Config:
        from_attributes = True

class RepetitionPerMonth(BaseModel):
    month: int
    pourcentage: float
    class Config:
        from_attributes = True
        
class RepetitionPerYear(BaseModel):
    year: int
    number_of_repetition: int
    class Config:
        from_attributes = True