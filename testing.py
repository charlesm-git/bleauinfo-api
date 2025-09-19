from sqlalchemy import Float, cast, desc, func, select
from sqlalchemy.orm import Session


from crud.areas import get_area_best_rated
from crud.recommendation import get_recommended_boulder
from crud.stats import (
    get_general_best_rated_boulders,
    get_general_best_rated_boulders_per_grade,
    get_general_most_ascents_boulders_per_grade,
    get_general_hardest_boulders,
    get_general_grade_distribution,
    get_general_rating_distribution,
    get_general_ascents_per_month,
    get_general_ascents_per_year,
    get_ascents_volume_distribution,
    get_general_style_distribution,
    get_top_repeaters,
    get_top_setters,
    get_general_ascents_per_grade,
)
from database import engine


if __name__ == "__main__":
    session = Session(engine)
    result = get_general_best_rated_boulders(db=session)
    for boulder in result:
        print(boulder)
    print(len(result))
