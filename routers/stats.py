from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.stats import (
    get_best_rated_boulders,
    get_most_ascents_areas,
    get_most_ascents_boulders,
    get_hardest_boulders,
    get_grade_distribution,
    get_boulders_rating_distribution,
    get_ascents_per_grade,
    get_repeats_volume_distribution,
    get_style_distribution,
    get_top_repeaters,
    get_top_setters,
    get_ascents_per_month,
    get_ascents_per_year,
)
from database import get_db_session
from schemas.area import AreaRepetition
from schemas.boulder import (
    Boulder,
    BoulderArea,
    BoulderRepetition,
    RatingCount,
)
from schemas.grade import GradeDistribution, GradeAscents
from schemas.ascent import AscentsPerMonth, AscentsPerYear
from schemas.style import StyleDistribution
from schemas.user import UserBoulderCount, UserRepetitionVolume

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/boulders/best-rated/{grade}")
def read_boulders_best_rated(
    db: Session = Depends(get_db_session), grade: str = None
) -> List[BoulderArea]:
    if grade is None:
        raise HTTPException(status_code=422, detail="A grade must be provided")
    boulders = get_best_rated_boulders(db=db, grade=grade)
    return boulders


@router.get("/boulders/most-repeats/{grade}")
def get_boulders_most_ascents(
    db: Session = Depends(get_db_session), grade: str = None
) -> List[BoulderRepetition]:
    if grade is None:
        raise HTTPException(status_code=422, detail="A grade must be provided")
    boulders = get_most_ascents_boulders(db=db, grade=grade)
    return boulders


@router.get("/boulders/hardest")
def read_boulders_hardest(
    db: Session = Depends(get_db_session), exclude_traverse: bool = False
) -> List[Boulder]:
    boulders = get_hardest_boulders(db=db, exclude_traverse=exclude_traverse)
    return boulders


@router.get("/boulders/ratings/distribution")
def read_rating_distribution(
    db: Session = Depends(get_db_session), exclude_traverse: bool = False
) -> List[RatingCount]:
    boulders = get_boulders_rating_distribution(db=db)
    return boulders


@router.get("/boulders/styles/distribution")
def read_style_distribution(
    db: Session = Depends(get_db_session),
) -> List[StyleDistribution]:
    boulders = get_style_distribution(db=db)
    return boulders


@router.get("/areas/most-repeats")
def read_area_with_most_ascents(
    db: Session = Depends(get_db_session),
) -> List[AreaRepetition]:
    boulders = get_most_ascents_areas(db=db)
    return boulders


@router.get("/grades/distribution")
def read_grade_distribution(
    db: Session = Depends(get_db_session),
) -> List[GradeDistribution]:
    boulders = get_grade_distribution(db=db)
    return boulders


@router.get("/users/top-repeaters")
def read_top_repeaters(
    db: Session = Depends(get_db_session),
) -> List[UserBoulderCount]:
    boulders = get_top_repeaters(db=db)
    return boulders


@router.get("/users/top-setters")
def read_top_setters(
    db: Session = Depends(get_db_session),
) -> List[UserBoulderCount]:
    boulders = get_top_setters(db=db)
    return boulders


@router.get("/users/repeats-volume")
def read_users_per_ascents_volume(
    db: Session = Depends(get_db_session),
) -> List[UserRepetitionVolume]:
    boulders = get_repeats_volume_distribution(db=db)
    return boulders


@router.get("/repeats/per-month")
def read_repeats_per_month(
    db: Session = Depends(get_db_session), grade: str = None
) -> List[AscentsPerMonth]:
    ascents = get_ascents_per_month(db=db, grade=grade)
    return ascents


@router.get("/repeats/per-year")
def read_repeats_per_year(
    db: Session = Depends(get_db_session), grade: str = None
) -> List[AscentsPerYear]:
    ascents = get_ascents_per_year(db=db, grade=grade)
    return ascents


@router.get("/repeats/per-grade")
def read_repeats_per_year(
    db: Session = Depends(get_db_session),
) -> List[GradeAscents]:
    grades = get_ascents_per_grade(db=db)
    return grades
