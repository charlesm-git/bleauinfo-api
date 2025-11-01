from sqlalchemy import Float, cast, desc, func, select
from sqlalchemy.orm import Session

from scipy.sparse import load_npz

from crud.search import search
from crud.area import get_area_best_rated
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
    get_general_statistics_home_page,
    get_general_style_distribution,
    get_top_repeaters,
    get_top_setters,
    get_general_ascents_per_grade,
)
from database import engine, get_recommendation_matrices
from routers.recommendation import recommendation_extraction_algorithm


if __name__ == "__main__":
    session = Session(engine)
    get_general_statistics_home_page(session)
    # result = search(db=session, text="")
    # print(result)
    # matrices = {}
    # matrices["ascents"] = load_npz("./similarity_ascent.npz")
    # matrices["style"] = load_npz("./similarity_style.npz")
    # matrices["grade"] = load_npz("./similarity_grade.npz")
    # result = recommendation_extraction_algorithm(
    #     boulder_ids=[35240],
    #     ascent_weight=0.5,
    #     grade_weight=0.25,
    #     style_weight=0.25,
    #     top_N=5,
    #     matrices=(
    #         matrices["ascents"],
    #         matrices["style"],
    #         matrices["grade"],
    #     ),
    # )
    # print(result)
