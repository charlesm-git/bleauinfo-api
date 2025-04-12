from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from models.area import Area
from models.repetition import Repetition


def get_all_areas(db: Session, skip: int = 0, limit: int = 20):
    return db.scalars(select(Area).offset(skip).limit(limit)).all()


def get_area(db: Session, area_id: int):
    return (
        db.query(Area)
        .options(
            joinedload(Area.region)
        )
        .filter(Area.id == area_id)
        .first()
    )
