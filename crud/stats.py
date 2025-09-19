from sqlalchemy import (
    Float,
    and_,
    cast,
    desc,
    exists,
    func,
    select,
    case,
)
from sqlalchemy.orm import Session, joinedload
from models.area import Area
from models.boulder import Boulder
from models.boulder_style import boulder_style_table
from models.boulder_setter import boulder_setter_table
from models.grade import Grade
from models.ascent import Ascent
from models.style import Style
from models.user import User
from schemas.area import AreaAscent
from schemas.boulder import (
    BoulderAreaGradeStyleAscent,
    BoulderByGrade,
    RatingCount,
)
from schemas.grade import GradeDistribution, GradeAscents
from schemas.ascent import AscentsPerMonth, AscentsPerYear
from schemas.style import StyleDistribution
from schemas.user import UserBoulderCount, UserAscentVolume


def get_general_best_rated_boulders_per_grade(db: Session, grade: str):
    result = (
        db.execute(
            select(Boulder, func.count(Ascent.user_id).label("ascents"))
            .where(
                and_(
                    Grade.value == grade,
                    Boulder.number_of_rating >= 10,
                    Boulder.rating >= 4.6,
                )
            )
            .join(Grade, Boulder.grade_id == Grade.id)
            .join(Ascent, Ascent.boulder_id == Boulder.id)
            .options(joinedload(Boulder.area), joinedload(Boulder.styles))
            .group_by(Boulder.id)
            .order_by(desc(Boulder.rating))
        )
        .unique()
        .all()
    )

    return [
        BoulderAreaGradeStyleAscent(
            id=boulder.id,
            name=boulder.name,
            rating=boulder.rating,
            number_of_rating=boulder.number_of_rating,
            url=boulder.url,
            area=boulder.area,
            styles=boulder.styles,
            ascents=ascents,
        )
        for boulder, ascents in result
    ]


def get_general_best_rated_boulders(db: Session):
    grades = db.scalars(
        select(Grade)
        .join(Boulder, Boulder.grade_id == Grade.id)
        .where(
            and_(
                Boulder.number_of_rating >= 10,
                Boulder.rating >= 4.6,
            )
        )
        .group_by(Grade.id)
        .order_by(desc(Grade.correspondence))
    ).all()

    result = []

    for grade in grades:
        boulder_result = (
            db.execute(
                select(Boulder, func.count(Ascent.user_id).label("ascents"))
                .where(
                    and_(
                        Grade.id == grade.id,
                        Boulder.number_of_rating >= 10,
                        Boulder.rating >= 4.6,
                    )
                )
                .join(Grade, Boulder.grade_id == Grade.id)
                .join(Ascent, Ascent.boulder_id == Boulder.id)
                .options(
                    joinedload(Boulder.area),
                    joinedload(Boulder.styles),
                    joinedload(Boulder.grade),
                    joinedload(Boulder.slash_grade),
                )
                .group_by(Boulder.id)
                .order_by(desc(Boulder.rating))
            )
            .unique()
            .all()
        )

        boulder_result = [
            BoulderAreaGradeStyleAscent(
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
            for boulder, ascents in boulder_result
        ]
        result.append(BoulderByGrade(grade=grade, boulders=boulder_result))

    return result


def get_general_most_ascents_boulders_per_grade(db: Session, grade: str):
    result = db.execute(
        select(Boulder, func.count(Ascent.user_id).label("ascents"))
        .join(Boulder.ascents)
        .join(Boulder.grade)
        .options(
            joinedload(Boulder.area),
        )
        .where(Grade.value == grade)
        .group_by(Ascent.boulder_id)
        .order_by(desc("ascents"))
        .limit(10)
    ).all()

    return [
        BoulderAreaGradeStyleAscent(
            id=boulder.id,
            name=boulder.name,
            rating=boulder.rating,
            number_of_rating=boulder.number_of_rating,
            url=boulder.url,
            area=boulder.area,
            styles=boulder.styles,
            ascents=ascents,
        )
        for boulder, ascents in result
    ]


def get_general_most_ascents_boulders(db: Session):
    grades = db.scalars(
        select(Grade).order_by(desc(Grade.correspondence))
    ).all()

    result = []

    for grade in grades:
        boulder_result = (
            db.execute(
                select(Boulder, func.count(Ascent.user_id).label("ascents"))
                .join(Boulder.ascents)
                .join(Boulder.grade)
                .options(
                    joinedload(Boulder.area),
                    joinedload(Boulder.grade),
                    joinedload(Boulder.slash_grade),
                    joinedload(Boulder.styles),
                )
                .where(Grade.id == grade.id)
                .group_by(Ascent.boulder_id)
                .order_by(desc("ascents"))
                .limit(10)
            )
            .unique()
            .all()
        )

        boulder_result = [
            BoulderAreaGradeStyleAscent(
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
            for boulder, ascents in boulder_result
        ]

        result.append(BoulderByGrade(grade=grade, boulders=boulder_result))

    return result


def get_general_hardest_boulders(db: Session, exclude_traverse: bool):
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


def get_general_rating_distribution(db: Session):
    result = db.execute(
        select(Boulder.rating, func.count(Boulder.id))
        .group_by(Boulder.rating)
        .order_by(desc(Boulder.rating))
    ).all()

    return [
        RatingCount(rating=rating, count=count) for rating, count in result
    ]


def get_most_ascents_areas(db: Session):
    result = db.execute(
        select(Area, func.count(Ascent.user_id).label("ascents_count"))
        .join(Boulder, Boulder.area_id == Area.id)
        .join(Ascent, Ascent.boulder_id == Boulder.id)
        .group_by(Area.id)
        .order_by(desc("ascents_count"))
        .limit(10)
    ).all()

    return [AreaAscent(area=area, ascents=count) for area, count in result]


def get_general_grade_distribution(db: Session):
    result = db.execute(
        select(Grade, func.count(Boulder.id))
        .join(Boulder, Boulder.grade_id == Grade.id)
        .group_by(Grade.correspondence)
    ).all()

    return [
        GradeDistribution(grade=grade, boulders=boulder_count)
        for grade, boulder_count in result
    ]


def get_general_style_distribution(db: Session):
    result = db.execute(
        select(Style.style, func.count(Boulder.id).label("boulder_count"))
        .join(boulder_style_table, Style.id == boulder_style_table.c.style_id)
        .join(Boulder, Boulder.id == boulder_style_table.c.boulder_id)
        .group_by(Style.style)
        .order_by(desc("boulder_count"))
    ).all()

    return [
        StyleDistribution(style=style, boulders=boulder_count)
        for style, boulder_count in result
    ]


def get_top_repeaters(db: Session):
    result = db.execute(
        select(User, func.count(Ascent.boulder_id).label("boulder_count"))
        .join(Ascent, User.id == Ascent.user_id)
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


def get_ascents_volume_distribution(db: Session):
    # Subquery: count ascents per user
    user_counts = (
        select(
            Ascent.user_id,
            func.count(Ascent.boulder_id).label("repeat_count"),
        )
        .group_by(Ascent.user_id)
        .subquery()
    )

    # Categorize users by ascent count
    category_case = case(
        (user_counts.c.repeat_count < 20, "1–19"),
        (user_counts.c.repeat_count < 50, "20–49"),
        (user_counts.c.repeat_count < 100, "50–99"),
        (user_counts.c.repeat_count < 200, "100–199"),
        (user_counts.c.repeat_count < 500, "200–499"),
        (user_counts.c.repeat_count < 1000, "500–999"),
        else_="1000+",
    )

    # Final query: count users per range

    results = db.execute(
        select(category_case, func.count(category_case).label("count"))
        .group_by(category_case)
        .order_by(desc("count"))
    ).all()

    return [
        UserAscentVolume(group=group, number_of_users=count)
        for group, count in results
    ]


def get_general_ascents_per_month(db: Session, grade: str = None):
    query_filter = []
    join_clause = Ascent

    if grade:
        grade_subquery = (
            select(Grade.correspondence)
            .where(Grade.value == grade)
            .scalar_subquery()
        )

        query_filter.append(Grade.correspondence >= grade_subquery)

        join_clause = Ascent.__table__.join(
            Boulder, Ascent.boulder_id == Boulder.id
        ).join(Grade, Boulder.grade_id == Grade.id)

    total_repeats = (
        select(func.count(Ascent.user_id))
        .select_from(join_clause)
        .where(*query_filter)
        .scalar_subquery()
    )
    main_query = (
        select(
            func.extract("month", Ascent.log_date).label("month"),
            func.round(
                (
                    func.count(Ascent.user_id)
                    * 100
                    / cast(total_repeats, Float)
                ),
                1,
            ),
        )
        .select_from(join_clause)
        .where(*query_filter)
        .group_by("month")
        .order_by("month")
    )

    result = db.execute(main_query).all()

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

    data = [
        (month_list[month - 1], percentage) for month, percentage in result
    ]

    return [
        AscentsPerMonth(month=month, percentage=pourcentage)
        for month, pourcentage in data
    ]


def get_general_ascents_per_year(db: Session, grade: str = None):
    query_filter = []
    join_clause = Ascent

    if grade:
        grade_subquery = (
            select(Grade.correspondence)
            .where(Grade.value == grade)
            .scalar_subquery()
        )

        query_filter.append(Grade.correspondence >= grade_subquery)

        join_clause = Ascent.__table__.join(
            Boulder, Ascent.boulder_id == Boulder.id
        ).join(Grade, Boulder.grade_id == Grade.id)

    main_query = (
        select(
            func.extract("year", Ascent.log_date).label("year"),
            func.count(Ascent.user_id),
        )
        .select_from(join_clause)
        .where(
            and_(*query_filter, func.extract("year", Ascent.log_date) >= 1995)
        )
        .group_by("year")
        .order_by("year")
    )
    result = db.execute(main_query).all()
    return [
        AscentsPerYear(year=year, ascents=number_of_ascents)
        for year, number_of_ascents in result
    ]


def get_general_ascents_per_grade(db: Session):
    result = db.execute(
        select(Grade, func.count(Ascent.boulder_id))
        .join(Boulder, Boulder.grade_id == Grade.id)
        .join(Ascent, Boulder.id == Ascent.boulder_id)
        .group_by(Grade.value)
        .order_by(Grade.correspondence)
    ).all()

    return [
        GradeAscents(grade=grade, ascents=ascents) for grade, ascents in result
    ]
