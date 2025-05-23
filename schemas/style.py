from pydantic import BaseModel


class Style(BaseModel):
    id: int
    style: str

    class Config:
        from_attributes = True


class StyleDistribution(BaseModel):
    style: str
    boulder_count: int

    class Config:
        from_attributes = True
