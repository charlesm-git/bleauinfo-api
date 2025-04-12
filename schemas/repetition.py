from datetime import date
from pydantic import BaseModel

from schemas.user import User


class Repetition(BaseModel):
    boulder_id: int
    user_id: int
    log_date: date

    class Config:
        orm_mode = True
