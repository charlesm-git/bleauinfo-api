from typing import List
from pydantic import BaseModel

from schemas.area import Area
from schemas.grade import Grade
from schemas.repetition import RepetitionRead
from schemas.style import Style


class Boulder(BaseModel):
    id: int
    name: str
    grade_id: int
    slash_grade_id: int | None = None
    area_id: int
    url: str

    class Config:
        from_attributes = True


class BoulderDetail(BaseModel):
    id: int
    name: str
    grade: Grade
    slash_grade: Grade | None = None
    area: Area
    styles: List[Style] = []
    rating: float | None = None
    number_of_rating: int = 0
    url: str
    repetitions: List[RepetitionRead] = []

    class Config:
        from_attributes = True
