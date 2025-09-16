import numpy as np
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.recommendation import get_recommended_boulder
from database import get_db_session, get_recommendation_matrices
from schemas.recommendation import BoulderRecommendation, RecommendationRequest


router = APIRouter(prefix="/recommendation", tags=["recommendation"])


@router.post("/")
def post_recommendation(
    request: RecommendationRequest,
    db: Session = Depends(get_db_session),
    matrices=Depends(get_recommendation_matrices),
) -> List[BoulderRecommendation]:

    # Get similarity matrices
    ascents, style, grade = matrices

    ascents = ascents[:, request.boulder_ids].sum(axis=1).A1
    style = style[:, request.boulder_ids].sum(axis=1).A1
    grade = grade[:, request.boulder_ids].sum(axis=1).A1

    # Remove input boulders from the recommendation
    ascents[request.boulder_ids] = 0
    style[request.boulder_ids] = 0
    grade[request.boulder_ids] = 0

    # Compute total similarity score
    sim_scores = (
        request.ascent_weight * ascents
        + request.style_weight * style
        + request.grade_weight * grade
    )

    # Get the top N most similar boulders for recommendation
    recommended_boulder_ids = np.argsort(-sim_scores)[:request.top_N]
    recommended_boulder_ids = recommended_boulder_ids.tolist()

    # Retrieve recommended boulders from the database
    recommended_boulders = get_recommended_boulder(
        db=db, boulder_ids=recommended_boulder_ids
    )

    # Order recommended boulders
    recommended_boulders = {
        boulder.id: boulder for boulder in recommended_boulders
    }
    ordered_boulders = [
        recommended_boulders[boulder_id]
        for boulder_id in recommended_boulder_ids
    ]

    return ordered_boulders
