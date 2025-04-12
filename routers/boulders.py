from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from crud.boulders import get_all_boulders, get_boulder
from database import get_db_session
from schemas.boulder import Boulder, BoulderDetail

router = APIRouter()


@router.get("/boulders/")
def read_boulders(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db_session),
) -> List[Boulder]:
    return get_all_boulders(db=db, skip=skip, limit=limit)


@router.get("/boulders/{id}")
def read_boulder(
    id: int,
    db: Session = Depends(get_db_session),
) -> BoulderDetail:
    boulder = get_boulder(db=db, boulder_id=id)
    return boulder
