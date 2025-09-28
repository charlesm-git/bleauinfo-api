from typing import List
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from helper import text_normalizer
from models.ascent import Ascent
from models.boulder import Boulder
from schemas.boulder import BoulderGradeAreaStyleAscent


def get_recommended_boulder(db: Session, boulder_ids: List[int]):
    result = (
        db.execute(
            select(Boulder, func.count(Ascent.user_id).label("ascents"))
            .filter(Boulder.id.in_(boulder_ids))
            .outerjoin(Ascent, Ascent.boulder_id == Boulder.id)
            .options(
                joinedload(Boulder.grade),
                joinedload(Boulder.slash_grade),
                joinedload(Boulder.area),
                joinedload(Boulder.styles),
            )
            .group_by(Boulder.id)
        )
        .unique()
        .all()
    )
    return [
        BoulderGradeAreaStyleAscent(
            id=boulder.id,
            name=boulder.name,
            grade=boulder.grade,
            slash_grade=boulder.slash_grade,
            rating=boulder.rating,
            number_of_rating=boulder.number_of_rating,
            url=boulder.url,
            area=boulder.area,
            styles=boulder.styles,
            ascents=ascents,
        )
        for boulder, ascents in result
    ]


def get_selected_boulder(db: Session, text: str):
    normalized_text = text_normalizer(text)
    result = (
        db.execute(
            select(Boulder, func.count(Ascent.user_id).label("ascents"))
            .where(Boulder.name_normalized.ilike(f"%{normalized_text}%"))
            .outerjoin(Ascent, Ascent.boulder_id == Boulder.id)
            .options(
                joinedload(Boulder.grade),
                joinedload(Boulder.slash_grade),
                joinedload(Boulder.area),
                joinedload(Boulder.styles),
            )
            .group_by(Boulder.id)
            .limit(20)
        )
        .unique()
        .all()
    )
    return [
        BoulderGradeAreaStyleAscent(
            id=boulder.id,
            name=boulder.name,
            grade=boulder.grade,
            slash_grade=boulder.slash_grade,
            rating=boulder.rating,
            number_of_rating=boulder.number_of_rating,
            url=boulder.url,
            area=boulder.area,
            styles=boulder.styles,
            ascents=ascents,
        )
        for boulder, ascents in result
    ]
