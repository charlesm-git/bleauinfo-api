from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db_session
from crud.users import (
    get_all_users,
    get_user,
    get_boulders_set_by,
    get_boulders_repeated_by,
)
from schemas.user import User, UserDetail
from schemas.boulder import Boulder

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def read_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db_session),
    username: str = None,
) -> List[User]:
    return get_all_users(db=db, skip=skip, limit=limit, username=username)


@router.get("/{id}")
def read_user(
    id: int,
    db: Session = Depends(get_db_session),
) -> UserDetail:
    boulder = get_user(db=db, id=id)
    return boulder


@router.get("/{id}/boulders/set")
def read_boulders_set_by(
    id: int, db: Session = Depends(get_db_session)
) -> List[Boulder]:
    boulders = get_boulders_set_by(db=db, user_id=id)
    return boulders


@router.get("/{id}/boulders/repeats")
def read_boulders_repeated_by(
    id: int, db: Session = Depends(get_db_session)
) -> List[Boulder]:
    boulders = get_boulders_repeated_by(db=db, user_id=id)
    return boulders
