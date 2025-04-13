from sqlalchemy import create_engine
from sqlalchemy.orm import Session

db_path = "bleau_info.db"

DATABASE_URL = f"sqlite:///{db_path}"
engine = create_engine(DATABASE_URL, echo=False)


def get_db_session():
    with Session(engine) as session:
        yield session
