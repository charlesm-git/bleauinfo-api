from typing import Dict, List, Tuple, Union
from pydantic import BaseModel

from schemas.area import Area
from schemas.grade import Grade


class User(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class UserDetail(BaseModel):
    id: int
    username: str
    url: str

    class Config:
        from_attributes = True


class UserStats(BaseModel):
    username: str
    total_boulders_repeated: int
    average_grade: Grade
    hardest_grade: Grade
    grade_distribution: List[Dict[str, Union[Grade, int]]]
    area_distribution: List[Dict[str, Union[Area, int]]]

    class Config:
        from_attributes = True
