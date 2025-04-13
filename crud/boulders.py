from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from models.boulder_style import boulder_style_table
from models.boulder import Boulder
from models.repetition import Repetition
from models.style import Style


def get_all_boulders(db: Session, skip: int = 0, limit: int = 20, style=None):
    query = select(Boulder)
    if style:
        query = (
            query.where(Style.style == style)
            .join(
                boulder_style_table,
                Boulder.id == boulder_style_table.c.boulder_id,
            )
            .join(Style, Style.id == boulder_style_table.c.style_id)
        )
    return db.scalars(query.offset(skip).limit(limit))


def get_boulder(db: Session, id: int):
    return db.scalar(
        select(Boulder)
        .where(Boulder.id == id)
        .options(
            joinedload(Boulder.grade),
            joinedload(Boulder.area),
            joinedload(Boulder.styles),
            joinedload(Boulder.repetitions),
            joinedload(Boulder.repetitions).joinedload(Repetition.user),
        )
    )
