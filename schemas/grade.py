from pydantic import BaseModel


class Grade(BaseModel):
    id: int
    value: str
    correspondence: int

    class Config:
        from_attributes = True


class GradeDistribution(BaseModel):
    grade: Grade
    boulder_count: int

    class Config:
        from_attributes = True


class GradeRepetition(BaseModel):
    grade: Grade
    number_of_repetition: int

    class Config:
        from_attributes = True
