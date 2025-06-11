from typing import List
from pydantic import BaseModel


class SearchBoulderArea(BaseModel):
    boulders: List["BoulderGradeArea"]
    areas: List["Area"]

    class Config:
        from_attributes = True


from schemas.boulder import BoulderGradeArea
from schemas.area import Area
