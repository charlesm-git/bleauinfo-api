from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.stats import (
    get_general_best_rated_boulders,
    get_general_best_rated_boulders_per_grade,
    get_general_most_ascents_boulders,
    get_general_statistics,
    get_most_ascents_areas,
    get_general_most_ascents_boulders_per_grade,
    get_general_hardest_boulders,
    get_general_grade_distribution,
    get_general_rating_distribution,
    get_general_ascents_per_grade,
    get_ascents_volume_distribution,
    get_general_style_distribution,
    get_top_repeaters,
    get_top_setters,
    get_general_ascents_per_month,
    get_general_ascents_per_year,
)
from database import get_db_session
from schemas.area import AreaAscent
from schemas.boulder import (
    Boulder,
    BoulderGradeAreaStyleAscent,
    BoulderByGrade,
    RatingCount,
)
from schemas.general import GeneralStatistics
from schemas.grade import GradeDistribution, GradeAscents
from schemas.ascent import AscentsPerMonth, AscentsPerYear
from schemas.style import StyleDistribution
from schemas.user import UserBoulderCount, UserAscentVolume

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/boulders/best-rated/{grade}")
def read_general_best_rated_boulders_per_grade(
    db: Session = Depends(get_db_session), grade: str = None
) -> List[BoulderGradeAreaStyleAscent]:
    if grade is None:
        raise HTTPException(status_code=422, detail="A grade must be provided")
    boulders = get_general_best_rated_boulders_per_grade(db=db, grade=grade)
    return boulders


@router.get("/boulders/best-rated")
def read_general_best_rated_boulders(
    db: Session = Depends(get_db_session),
) -> List[BoulderByGrade]:
    boulders = get_general_best_rated_boulders(db=db)
    return boulders


@router.get("/boulders/most-ascents/{grade}")
def read_general_most_ascents_boulders_per_grade(
    db: Session = Depends(get_db_session), grade: str = None
) -> List[BoulderGradeAreaStyleAscent]:
    if grade is None:
        raise HTTPException(status_code=422, detail="A grade must be provided")
    boulders = get_general_most_ascents_boulders_per_grade(db=db, grade=grade)
    return boulders


@router.get("/boulders/most-ascents")
def read_general_most_ascents_boulders(
    db: Session = Depends(get_db_session),
) -> List[BoulderByGrade]:
    boulders = get_general_most_ascents_boulders(db=db)
    return boulders

@router.get("/general")
def read_general_statistics(db: Session = Depends(get_db_session)) -> GeneralStatistics:
    return  get_general_statistics(db=db)
    

@router.get("/boulders/hardest")
def read_general_hardest_boulders(
    db: Session = Depends(get_db_session), exclude_traverse: bool = False
) -> List[Boulder]:
    boulders = get_general_hardest_boulders(
        db=db, exclude_traverse=exclude_traverse
    )
    return boulders


@router.get("/boulders/ratings/distribution")
def read_general_rating_distribution(
    db: Session = Depends(get_db_session), exclude_traverse: bool = False
) -> List[RatingCount]:
    boulders = get_general_rating_distribution(db=db)
    return boulders


@router.get("/boulders/styles/distribution")
def read_general_style_distribution(
    db: Session = Depends(get_db_session),
) -> List[StyleDistribution]:
    boulders = get_general_style_distribution(db=db)
    return boulders


@router.get("/areas/most-ascents")
def read_general_most_ascents_areas(
    db: Session = Depends(get_db_session),
) -> List[AreaAscent]:
    boulders = get_most_ascents_areas(db=db)
    return boulders


@router.get("/grades/distribution")
def read_general_grade_distribution(
    db: Session = Depends(get_db_session),
) -> List[GradeDistribution]:
    boulders = get_general_grade_distribution(db=db)
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
def read_ascents_volume_distribution(
    db: Session = Depends(get_db_session),
) -> List[UserAscentVolume]:
    boulders = get_ascents_volume_distribution(db=db)
    return boulders


@router.get("/ascents/per-month")
def read_general_repeats_per_month(
    db: Session = Depends(get_db_session), grade: str = None
) -> List[AscentsPerMonth]:
    ascents = get_general_ascents_per_month(db=db, grade=grade)
    return ascents


@router.get("/ascents/per-year")
def read_general_repeats_per_year(
    db: Session = Depends(get_db_session), grade: str = None
) -> List[AscentsPerYear]:
    ascents = get_general_ascents_per_year(db=db, grade=grade)
    return ascents


@router.get("/ascents/per-grade")
def read_general_ascents_per_grade(
    db: Session = Depends(get_db_session),
) -> List[GradeAscents]:
    grades = get_general_ascents_per_grade(db=db)
    return grades
