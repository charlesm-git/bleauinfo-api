from sqlalchemy.orm import Session

from crud.areas import (
    get_average_grade,
    get_most_climbed_boulders,
    get_number_of_boulders,
    get_grade_distribution,
    get_total_repetition,
)
from database import engine

if __name__ == "__main__":
    session = Session(engine)
    print(get_number_of_boulders(session, 1))

    grade_distrib = get_grade_distribution(session, 1)
    for grade in grade_distrib:
        print(grade)
    print()

    most_climbed_boulders = get_most_climbed_boulders(session, 1)
    for boulder in most_climbed_boulders:
        print(boulder)

    print(get_average_grade(session, 1))

    print(get_total_repetition(session, 228))
