from sqlalchemy import and_, select, func
from sqlalchemy.orm import Session, joinedload
from models.boulder_style import boulder_style_table
from models.boulder import Boulder
from models.repetition import Repetition
from models.style import Style
from schemas.boulder import BoulderDetail
from schemas.ascent import AscentDate


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
    boulder = db.scalar(
        select(Boulder)
        .where(Boulder.id == id)
        .options(
            joinedload(Boulder.grade),
            joinedload(Boulder.slash_grade),
            joinedload(Boulder.area),
            joinedload(Boulder.styles),
            joinedload(Boulder.repetitions),
            joinedload(Boulder.repetitions).joinedload(Repetition.user),
        )
    )
    aggregated_ascents = db.execute(
        select(
            func.extract("month", Repetition.log_date).label("month"),
            func.count(Repetition.user_id),
        )
        .where(Repetition.boulder_id == boulder.id)
        .group_by("month")
        .order_by("month")
    ).all()

    aggregated_ascents = [
        AscentDate(date=date, ascents=ascents)
        for date, ascents in aggregated_ascents
    ]

    return BoulderDetail(
        id=boulder.id,
        name=boulder.name,
        rating=boulder.rating,
        number_of_rating=boulder.number_of_rating,
        url=boulder.url,
        grade=boulder.grade,
        slash_grade=boulder.slash_grade,
        area=boulder.area,
        styles=boulder.styles,
        repetitions=boulder.repetitions,
        aggregated_ascents=aggregated_ascents,
    )
