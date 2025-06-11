from __future__ import annotations

from typing import List, Union
from pydantic import BaseModel


class Area(BaseModel):
    id: int
    name: str
    url: str
    status: str | None = None
    region_id: int

    class Config:
        from_attributes = True


class AreaDetail(BaseModel):
    id: int
    name: str
    url: str
    status: str | None = None
    region: "Region"

    class Config:
        from_attributes = True


class AreaStats(BaseModel):
    area: "AreaDetail"
    number_of_boulders: int
    average_grade: Union["Grade", None]
    ascents: int
    grade_distribution: List["GradeDistribution"]
    most_climbed_boulders: List["BoulderGradeAscent"]
    best_rated_boulders: List["BoulderGradeAscent"]

    class Config:
        from_attributes = True


class AreaAscent(BaseModel):
    area: Area
    ascents: int

    class Config:
        from_attributes = True


from schemas.grade import Grade, GradeDistribution
from schemas.region import Region
from schemas.boulder import BoulderGradeAscent
