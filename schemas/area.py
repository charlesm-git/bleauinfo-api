from __future__ import annotations

from typing import Dict, List, Union
from pydantic import BaseModel


class Area(BaseModel):
    id: int
    name: str
    url: str
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
    id: int
    name: str
    number_of_boulders: int
    average_grade: "Grade"
    total_number_of_repetition: int
    grade_distribution: List[Dict[str, Union["Grade", int]]]
    most_climbed_boulders: List[Dict[str, Union["Boulder", int]]]



from schemas.grade import Grade
from schemas.region import Region
from schemas.boulder import Boulder
