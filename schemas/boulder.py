from __future__ import annotations

from typing import List
from pydantic import BaseModel


class Boulder(BaseModel):
    id: int
    name: str
    grade_id: int
    slash_grade_id: int | None = None
    area_id: int
    rating: float | None = None
    url: str

    class Config:
        from_attributes = True


class BoulderDetail(BaseModel):
    id: int
    name: str
    grade: "Grade"
    slash_grade: "Grade" = None
    area: "Area"
    styles: List["Style"] = []
    rating: float | None = None
    number_of_rating: int = 0
    url: str
    repetitions: List["RepetitionRead"] = []

    class Config:
        from_attributes = True


class BoulderRepetition(BaseModel):
    boulder: Boulder
    number_of_repetition: int

    class Config:
        from_attributes = True


class RatingCount(BaseModel):
    rating: float | None
    count: int


from schemas.area import Area
from schemas.grade import Grade
from schemas.repetition import RepetitionRead
from schemas.style import Style
