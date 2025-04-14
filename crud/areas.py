from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session, joinedload
from models.area import Area
from models.boulder import Boulder
from models.grade import Grade
from models.repetition import Repetition
from schemas.area import AreaStats


def get_all_areas(db: Session, skip: int = 0, limit: int = 20):
    return db.scalars(select(Area).offset(skip).limit(limit))


def get_area(db: Session, id: int):
    return db.scalar(
        select(Area).where(Area.id == id).options(joinedload(Area.region))
    )


def get_boulders_from_area(db: Session, area_id: int):
    return db.scalars(select(Boulder).where(Boulder.area_id == area_id))


def get_area_stats(db: Session, area_id: int):
    name = get_area(db, area_id).name
    number_of_boulder = get_number_of_boulders(db, area_id)
    grade_distribution = get_grade_distribution(db, area_id)
    most_climbed_boulders = get_most_climbed_boulders(db, area_id)
    average_grade = get_average_grade(db, area_id)
    total_repetition = get_total_repetition(db, area_id)
    return AreaStats(
        id=area_id,
        name=name,
        number_of_boulders=number_of_boulder,
        grade_distribution=grade_distribution,
        most_climbed_boulders=most_climbed_boulders,
        average_grade=average_grade,
        total_number_of_repetition=total_repetition,
    )


def get_name_from_id(db: Session, area_id: int):
    return db.scalar(select(Area.name).where(Area.id == area_id))


def get_number_of_boulders(db: Session, area_id: int):
    return db.scalar(
        select(func.count(Boulder.id)).where(Boulder.area_id == area_id)
    )


def get_grade_distribution(db: Session, area_id: int):
    result = db.execute(
        select(Grade, func.count(Boulder.id))
        .where(Boulder.area_id == area_id)
        .group_by(Grade.id)
        .join(Boulder, Boulder.grade_id == Grade.id)
    ).all()

    return [{"grade": grade, "count": count} for grade, count in result]


def get_most_climbed_boulders(db: Session, area_id: int, limit: int = 10):
    result = db.execute(
        select(
            Boulder,
            func.count(Repetition.user_id).label("number_of_repetition"),
        )
        .where(Boulder.area_id == area_id)
        .order_by(desc("number_of_repetition"))
        .join(Repetition, Boulder.id == Repetition.boulder_id)
        .group_by(Repetition.boulder_id)
        .limit(limit)
    ).all()

    return [
        {"boulder": boulder, "number_of_repetition": number_of_repetition}
        for boulder, number_of_repetition in result
    ]


def get_average_grade(db: Session, area_id: int):
    subquery = (
        select(func.avg(Grade.correspondence))
        .where(Boulder.area_id == area_id)
        .join(Boulder, Boulder.grade_id == Grade.id)
    ).scalar_subquery()

    return db.scalar(
        select(Grade).where(Grade.correspondence == func.round(subquery))
    )


def get_total_repetition(db: Session, area_id: int):
    return db.scalar(
        select(func.count(Repetition.user_id))
        .where(Boulder.area_id == area_id)
        .join(Boulder, Boulder.id == Repetition.boulder_id)
    )
