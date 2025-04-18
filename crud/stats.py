from sqlalchemy import and_, desc, exists, func, select, case
from sqlalchemy.orm import Session
from models.area import Area
from models.boulder import Boulder
from models.boulder_style import boulder_style_table
from models.boulder_setter import boulder_setter_table
from models.grade import Grade
from models.repetition import Repetition
from models.style import Style
from models.user import User
from schemas.area import AreaRepetition
from schemas.boulder import BoulderRepetition, RatingCount
from schemas.grade import GradeDistribution
from schemas.style import StyleDistribution
from schemas.user import UserBoulderCount


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


def get_boulders_rating_distribution(db: Session):
    result = db.execute(
        select(Boulder.rating, func.count(Boulder.id))
        .group_by(Boulder.rating)
        .order_by(desc(Boulder.rating))
    ).all()

    return [
        RatingCount(rating=rating, count=count) for rating, count in result
    ]


def get_most_repeated_areas(db: Session):
    result = db.execute(
        select(Area, func.count(Repetition.user_id).label("repetition_count"))
        .join(Boulder, Boulder.area_id == Area.id)
        .join(Repetition, Repetition.boulder_id == Boulder.id)
        .group_by(Area.id)
        .order_by(desc("repetition_count"))
        .limit(20)
    ).all()

    return [
        AreaRepetition(area=area, number_of_repetition=count)
        for area, count in result
    ]


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


def get_style_distribution(db: Session):
    result = db.execute(
        select(Style.style, func.count(Style.boulders).label("boulder_count"))
        .join(boulder_style_table, Style.id == boulder_style_table.c.style_id)
        .join(Boulder, Boulder.id == boulder_style_table.c.boulder_id)
        .order_by(desc("boulder_count"))
    ).all()

    return [
        StyleDistribution(style=style, boulder_count=boulder_count)
        for style, boulder_count in result
    ]


def get_top_repeaters(db: Session):
    result = db.execute(
        select(User, func.count(Repetition.boulder_id).label("boulder_count"))
        .join(Repetition, User.id == Repetition.user_id)
        .group_by(User.id)
        .order_by(desc("boulder_count"))
        .limit(20)
    ).all()

    return [
        UserBoulderCount(
            id=user.id, username=user.username, boulder_count=boulder_count
        )
        for user, boulder_count in result
    ]


def get_top_setters(db: Session):
    result = db.execute(
        select(
            User,
            func.count(boulder_setter_table.c.boulder_id).label(
                "boulder_count"
            ),
        )
        .join(boulder_setter_table, User.id == boulder_setter_table.c.user_id)
        .group_by(User.id)
        .order_by(desc("boulder_count"))
        .limit(20)
    ).all()

    return [
        UserBoulderCount(
            id=user.id, username=user.username, boulder_count=boulder_count
        )
        for user, boulder_count in result
    ]


def get_repeats_volume_distribution(db: Session):
    # Subquery: count repetitions per user
    user_counts = (
        select(
            Repetition.user_id,
            func.count(Repetition.boulder_id).label("repeat_count"),
        )
        .group_by(Repetition.user_id)
        .subquery()
    )

    # Categorize users by repetition count
    category_case = case(
        (user_counts.c.repeat_count < 10, "0–9"),
        (user_counts.c.repeat_count < 50, "10–49"),
        (user_counts.c.repeat_count < 2000, "50–1999"),
        else_="1999+",
    )

    # Final query: count users per range

    results = db.execute(
        select(category_case, func.count(category_case)).group_by(
            category_case
        )
    ).all()

    return results
