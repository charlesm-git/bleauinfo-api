from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class UserDetail(BaseModel):
    id: int
    username: str
    url: str

    class Config:
        orm_mode = True
