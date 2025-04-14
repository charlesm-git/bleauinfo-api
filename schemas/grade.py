from pydantic import BaseModel


class Grade(BaseModel):
    id: int
    value: str
    correspondence: int

    class Config:
        from_attributes = True
