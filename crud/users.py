from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from models.boulder import Boulder
from models.repetition import Repetition
from models.user import User
from models.boulder_setter import boulder_setter_table


def get_all_users(
    db: Session, skip: int = 0, limit: int = 20, username: str = None
):
    query = select(User)
    if username:
        query = query.where(User.username.ilike(f"%{username}%"))
    return db.scalars(query.offset(skip).limit(limit))


def get_user(db: Session, id: int):
    return db.scalar(select(User).where(User.id == id))


def get_boulders_set_by(db: Session, user_id: int):
    return db.scalars(
        select(Boulder)
        .where(boulder_setter_table.c.user_id == user_id)
        .join(
            boulder_setter_table,
            Boulder.id == boulder_setter_table.c.boulder_id,
        )
    )


def get_boulders_repeated_by(db: Session, user_id: int):
    return db.scalars(
        select(Boulder)
        .where(Repetition.user_id == user_id)
        .join(Repetition, Boulder.id == Repetition.boulder_id)
    )
