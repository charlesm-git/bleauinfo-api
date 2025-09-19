from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.search import search
from database import get_db_session
from helper import text_normalizer
from schemas.search import SearchBoulderArea


router = APIRouter(prefix="/search", tags=["search"])


@router.get("/{text}")
def read_research(
    text: str,
    db: Session = Depends(get_db_session),
) -> SearchBoulderArea:
    return search(db=db, text=text_normalizer(text))
