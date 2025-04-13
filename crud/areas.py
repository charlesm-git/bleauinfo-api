from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from models.area import Area
from models.boulder import Boulder


def get_all_areas(db: Session, skip: int = 0, limit: int = 20):
    return db.scalars(select(Area).offset(skip).limit(limit))


def get_area(db: Session, id: int):
    return db.scalar(
        select(Area).where(Area.id == id).options(joinedload(Area.region))
    )


def get_boulders_from_area(db: Session, area_id: int):
    return db.scalars(select(Boulder).where(Boulder.area_id == area_id))
