from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from models.area import Area
from models.boulder import Boulder
from schemas.search import SearchBoulderArea


def search(db: Session, text: str):
    boulders = db.scalars(
        select(Boulder)
        .where(Boulder.name_normalized.ilike(f"%{text}%"))
        .options(
            joinedload(Boulder.area),
            joinedload(Boulder.grade),
            joinedload(Boulder.slash_grade),
        )
        .order_by(Boulder.name)
    ).all()

    areas = db.scalars(
        select(Area)
        .where(Area.name_normalized.ilike(f"%{text}%"))
        .order_by(Area.name)
    ).all()

    return SearchBoulderArea(boulders=boulders, areas=areas)
