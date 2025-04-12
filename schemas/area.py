from pydantic import BaseModel

from schemas.region import Region


class Area(BaseModel):
    id: int
    name: str
    url: str

    class Config:
        orm_mode = True


class AreaDetail(BaseModel):
    id: int
    name: str
    url: str
    status: str | None = None
    region: Region

    class Config:
        orm_mode = True
