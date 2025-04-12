from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from crud.areas import get_all_areas, get_area
from database import get_db_session
from schemas.area import Area, AreaDetail

router = APIRouter()


@router.get("/areas/")
def read_areas(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db_session),
) -> List[Area]:
    return get_all_areas(db=db, skip=skip, limit=limit)


@router.get("/areas/{id}")
def read_area(
    id: int,
    db: Session = Depends(get_db_session),
) -> AreaDetail:
    boulder = get_area(db=db, area_id=id)
    return boulder
