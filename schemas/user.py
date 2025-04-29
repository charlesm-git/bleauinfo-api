from typing import List
from pydantic import BaseModel

from schemas.grade import Grade, GradeRepetition
from schemas.area import AreaRepetition


class User(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class UserDetail(User):
    url: str


class UserStats(BaseModel):
    username: str
    total_boulders_repeated: int
    average_grade: Grade
    hardest_grade: Grade
    grade_distribution: List[GradeRepetition]
    area_distribution: List[AreaRepetition]

    class Config:
        from_attributes = True


class UserBoulderCount(User):
    boulder_count: int

class UserRepetitionVolume(BaseModel):
    group: str
    number_of_users: int
    class Config:
        from_attributes = True