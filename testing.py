from sqlalchemy.orm import Session


from crud.stats import (
    get_best_rated_boulders,
    get_most_repeated_boulders,
    get_hardest_boulders,
    get_grade_distribution,
)
from database import engine

if __name__ == "__main__":
    session = Session(engine)
    print(get_grade_distribution(session))
