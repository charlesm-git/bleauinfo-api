from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    url: str

    class Config:
        orm_mode = True
