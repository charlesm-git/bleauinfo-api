from sqlalchemy import create_engine
from sqlalchemy.orm import Session


DB_PATH = "bleau_info-17-09-2025.db"

DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(DATABASE_URL, echo=False)

RECOMMENDATION_MATRICES = {}

MONTH_LIST = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def get_db_session():
    with Session(engine) as session:
        yield session


def get_recommendation_matrices():
    """Dependency that return the cached recommendation matrices"""
    return (
        RECOMMENDATION_MATRICES["ascents"],
        RECOMMENDATION_MATRICES["style"],
        RECOMMENDATION_MATRICES["grade"],
    )
