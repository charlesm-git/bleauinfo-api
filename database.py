from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from scipy.sparse import load_npz


db_path = "bleau_info-17-09-2025.db"

DATABASE_URL = f"sqlite:///{db_path}"
engine = create_engine(DATABASE_URL, echo=False)

RECOMMENDATION_MATRICES = {}


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
