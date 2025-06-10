from pydantic import BaseModel


class Style(BaseModel):
    id: int
    style: str

    class Config:
        from_attributes = True


class StyleDistribution(BaseModel):
    style: str
    boulders: int

    class Config:
        from_attributes = True
