from sqlalchemy import Float, cast, desc, func, select
from sqlalchemy.orm import Session


from crud.stats import (
    get_best_rated_boulders,
    get_most_ascents_boulders,
    get_hardest_boulders,
    get_grade_distribution,
    get_boulders_rating_distribution,
    get_ascents_per_month,
    get_ascents_per_year,
    get_repeats_volume_distribution,
    get_style_distribution,
    get_top_repeaters,
    get_top_setters,
    get_ascents_per_grade,
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

    get_ascents_per_grade(session)
