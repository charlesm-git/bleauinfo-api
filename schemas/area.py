from pydantic import BaseModel

from schemas.region import Region


class Area(BaseModel):
    id: int
    name: str
    url: str
    region_id: int

    class Config:
        from_attributes = True


class AreaDetail(BaseModel):
    id: int
    name: str
    url: str
    status: str | None = None
    region: Region

    class Config:
        from_attributes = True
