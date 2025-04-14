from pydantic import BaseModel


class Style(BaseModel):
    id: int
    style: str

    class Config:
        from_attributes = True
