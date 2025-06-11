from sqlalchemy import Float, cast, desc, func, select
from sqlalchemy.orm import Session


from crud.areas import get_area_best_rated
from crud.stats import (
    get_general_best_rated_boulders,
    get_general_most_ascents_boulders,
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
from models.area import Area
from models.boulder import Boulder
from models.grade import Grade
from models.repetition import Repetition
from models.boulder_setter import boulder_setter_table
from models.user import User

if __name__ == "__main__":
    session = Session(engine)
    print(get_area_best_rated(session, 1))
