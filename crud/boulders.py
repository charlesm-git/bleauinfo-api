from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from models.boulder import Boulder
from models.repetition import Repetition


def get_all_boulders(db: Session, skip: int = 0, limit: int = 20):
    return db.scalars(select(Boulder).offset(skip).limit(limit)).all()


def get_boulder(db: Session, boulder_id: int):
    return (
        db.query(Boulder)
        .options(
            joinedload(Boulder.grade),
            joinedload(Boulder.area),
            joinedload(Boulder.styles),
            joinedload(Boulder.repetitions).joinedload(Repetition.user),
        )
        .filter(Boulder.id == boulder_id)
        .first()
    )
