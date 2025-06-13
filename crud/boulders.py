from sqlalchemy import select, func, cast, Float, text
from sqlalchemy.orm import Session, joinedload
from crud.stats import get_general_ascents_per_month
from models.boulder_style import boulder_style_table
from models.boulder import Boulder
from models.repetition import Repetition
from models.style import Style
from schemas.boulder import BoulderDetail
from schemas.ascent import AscentsPerMonth, AscentsPerMonthWithGeneral


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

    # Total ascents for percentage calculation
    boulder_total_repeats = (
        select(func.count(Repetition.user_id))
        .where(Repetition.boulder_id == boulder.id)
        .scalar_subquery()
    )
    total_ascents = select(func.count(Repetition.boulder_id)).scalar_subquery()

    # Monthly ascent distribution
    aggregated_ascents = db.execute(
        select(
            func.extract("month", Repetition.log_date).label("month"),
            func.round(
                (
                    func.count(Repetition.user_id)
                    * 100
                    / cast(boulder_total_repeats, Float)
                ),
                1,
            ).label("boulder"),
        )
        .select_from(Repetition)
        .where(Repetition.boulder_id == boulder.id)
        .group_by("month")
        .order_by("month")
    ).all()

    general_month_distribution = db.scalars(
        select(
            func.round(
                (
                    func.count(Repetition.user_id)
                    * 100
                    / cast(total_ascents, Float)
                ),
                1,
            ).label("general"),
        )
        .group_by(func.extract("month", Repetition.log_date))
        .order_by(func.extract("month", Repetition.log_date))
    ).all()

    months_with_ascents = {item[0] for item in aggregated_ascents}

    for month in range(1, 13):
        if month not in months_with_ascents:
            aggregated_ascents.append((month, 0))
    aggregated_ascents = sorted(aggregated_ascents, key=lambda x: x[0])

    month_list = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]

    aggregated_ascents = [
        AscentsPerMonthWithGeneral(
            month=month_list[month],
            boulder=aggregated_ascents[month][1],
            general=general_month_distribution[month],
        )
        for month in range(12)
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
