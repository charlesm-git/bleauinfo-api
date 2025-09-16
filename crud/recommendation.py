from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from models.boulder import Boulder


def get_recommended_boulder(db: Session, boulder_ids: List[int]):
    boulders = db.scalars(
        select(Boulder)
        .filter(Boulder.id.in_(boulder_ids))
        .options(joinedload(Boulder.grade), joinedload(Boulder.area))
    ).all()
    return boulders
