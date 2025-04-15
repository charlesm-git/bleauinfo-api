from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.regions import get_all_regions, get_areas_from_region
from database import get_db_session
from schemas.area import Area
from schemas.region import Region

router = APIRouter(prefix="/regions", tags=["regions"])


@router.get("/")
def read_regions(
    db: Session = Depends(get_db_session),
) -> List[Region]:
    return get_all_regions(db=db)


@router.get("/{id}/areas")
def read_areas_from_regions(
    id: int,
    db: Session = Depends(get_db_session),
) -> List[Area]:
    boulder = get_areas_from_region(db=db, region_id=id)
    return boulder
