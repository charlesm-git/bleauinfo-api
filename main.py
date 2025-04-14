from sqlalchemy.orm import Session


from fastapi import FastAPI
from crud.users import (
    get_average_grade,
    get_grade_distribution,
    get_hardest_grade,
    get_area_distribution,
    get_total_boulder_repeated,
    get_username_from_id,
)
from database import engine
from routers import areas, boulders, regions, users

app = FastAPI()

app.include_router(boulders.router)
app.include_router(areas.router)
app.include_router(regions.router)
app.include_router(users.router)

# if __name__ == "__main__":
#     session = Session(engine)
#     print(get_username_from_id(db=session, user_id=12))
#     print(get_total_boulder_repeated(db=session, user_id=12))
#     print(get_grade_distribution(db=session, user_id=12))
#     print(get_average_grade(db=session, user_id=12))
#     print(get_hardest_grade(db=session, user_id=12))
#     print(get_area_distribution(db=session, user_id=12))
