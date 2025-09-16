from __future__ import annotations

from typing import List
from pydantic import BaseModel

from schemas.area import Area
from schemas.grade import Grade


class RecommendationRequest(BaseModel):
    boulder_ids: List[int]
    ascent_weight: float = .5
    style_weight: float = .25
    grade_weight: float = .25
    top_N: int = 20

class BoulderRecommendation(BaseModel):
    id: int
    name: str
    area: "Area"
    grade: "Grade"
    url: str
    
    class Config:
        from_attributes = True
