from sqlalchemy import and_, desc, exists, func, select
from sqlalchemy.orm import Session
from models.boulder import Boulder
from models.boulder_style import boulder_style_table
from models.grade import Grade
from models.repetition import Repetition
from models.style import Style
from schemas.boulder import BoulderRepetition
from schemas.grade import GradeDistribution


def get_best_rated_boulders(db: Session, grade: str):
    return db.scalars(
        select(Boulder)
        .where(
            and_(
                Grade.value == grade,
                Boulder.number_of_rating >= 10,
                Boulder.rating >= 4.7,
            )
        )
        .join(Boulder.grade)
        .order_by(desc(Boulder.rating))
    ).all()


def get_most_repeated_boulders(db: Session, grade: str):
    result = db.execute(
        select(
            Boulder,
            func.count(Repetition.user_id).label("number_of_repetition"),
        )
        .join(Repetition, Boulder.id == Repetition.boulder_id)
        .join(Grade, Boulder.grade_id == Grade.id)
        .where(Grade.value == grade)
        .group_by(Repetition.boulder_id)
        .order_by(desc("number_of_repetition"))
        .limit(10)
    ).all()

    return [
        BoulderRepetition(
            boulder=boulder, number_of_repetition=number_of_repetition
        )
        for boulder, number_of_repetition in result
    ]


def get_hardest_boulders(db: Session, exclude_traverse: bool):
    query = select(Boulder)
    if exclude_traverse:
        subquery_traverse = (
            select(1)
            .select_from(boulder_style_table)
            .join(Style, Style.id == boulder_style_table.c.style_id)
            .where(
                and_(
                    Boulder.id == boulder_style_table.c.boulder_id,
                    Style.style.in_(
                        [
                            "traversée",
                            "traversée d-g",
                            "traversée g-d",
                            "boucle",
                        ]
                    ),
                )
            )
        )
        query = query.where(~exists(subquery_traverse))

    subquery = (
        select(Grade.correspondence)
        .where(Grade.value == "8c")
        .scalar_subquery()
    )

    query = (
        query.where(Grade.correspondence >= subquery)
        .join(Grade, Boulder.grade_id == Grade.id)
        .order_by(desc(Grade.correspondence), Boulder.name)
    )

    return db.scalars(query).all()


def get_grade_distribution(db: Session):
    result = db.execute(
        select(Grade, func.count(Boulder.id))
        .join(Boulder, Boulder.grade_id == Grade.id)
        .group_by(Grade.correspondence)
    ).all()

    return [
        GradeDistribution(grade=grade, boulder_count=boulder_count)
        for grade, boulder_count in result
    ]
