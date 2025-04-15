from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.stats import (
    get_best_rated_boulders,
    get_most_repeated_boulders,
    get_hardest_boulders,
    get_grade_distribution
)
from database import get_db_session
from schemas.boulder import Boulder, BoulderRepetition
from schemas.grade import GradeDistribution

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/boulders/best-rated")
def read_boulders_best_rated(
    db: Session = Depends(get_db_session), grade: str = None
) -> List[Boulder]:
    if grade is None:
        raise HTTPException(status_code=422, detail="A grade must be provided")
    boulders = get_best_rated_boulders(db=db, grade=grade)
    return boulders


@router.get("/boulders/most-repeats")
def get_boulders_most_repeated(
    db: Session = Depends(get_db_session), grade: str = None
) -> List[BoulderRepetition]:
    if grade is None:
        raise HTTPException(status_code=422, detail="A grade must be provided")
    boulders = get_most_repeated_boulders(db=db, grade=grade)
    return boulders


@router.get("/boulders/hardest")
def read_boulders_hardest(
    db: Session = Depends(get_db_session), exclude_traverse: bool = False
) -> List[Boulder]:
    boulders = get_hardest_boulders(db=db, exclude_traverse=exclude_traverse)
    return boulders


@router.get("/grades/distribution")
def read_grade_distribution(
    db: Session = Depends(get_db_session),
) -> List[GradeDistribution]:
    boulders = get_grade_distribution(db=db)
    return boulders
