from pydantic import BaseModel


class Region(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
