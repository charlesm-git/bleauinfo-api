from __future__ import annotations

from typing import List, Union
from pydantic import BaseModel


class Boulder(BaseModel):
    id: int
    name: str
    rating: float | None = None
    number_of_rating: int = 0
    url: str

    class Config:
        from_attributes = True


class BoulderDetail(Boulder):
    grade: "Grade"
    slash_grade: Union["Grade", None] = None
    area: "Area"
    styles: List["Style"] = []
    ascents: List["AscentRead"] = []
    aggregated_ascents: List["AscentsPerMonthWithGeneral"]

    class Config:
        from_attributes = True


class BoulderGrade(Boulder):
    grade: "Grade"
    slash_grade: Union["Grade", None] = None


class BoulderArea(Boulder):
    area: "Area"


class BoulderGradeArea(Boulder):
    grade: "Grade"
    slash_grade: Union["Grade", None] = None
    area: Area


class BoulderGradeAscent(BaseModel):
    boulder: BoulderGrade
    ascents: int

    class Config:
        from_attributes = True


class BoulderAreaAscent(BaseModel):
    boulder: BoulderArea
    ascents: int

    class Config:
        from_attributes = True


class RatingCount(BaseModel):
    rating: float | None
    count: int


from schemas.area import Area
from schemas.grade import Grade
from schemas.ascent import AscentRead, AscentsPerMonthWithGeneral
from schemas.style import Style
