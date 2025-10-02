from __future__ import annotations

from typing import List
from pydantic import BaseModel

from schemas.area import Area
from schemas.grade import Grade


class RecommendationRequest(BaseModel):
    boulder_ids: List[int]
    ascent_weight: float = 0.6
    style_weight: float = 0.2
    grade_weight: float = 0.2
    top_N: int = 10
