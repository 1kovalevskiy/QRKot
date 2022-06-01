from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel, Field, NonNegativeInt, PositiveInt, root_validator, Extra
)


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    """
    В CharityProjectBase поля необязательные
    А в CharityProjectCreate - обязательные
    """
    name: str = Field(None, min_length=1, max_length=100)
    description: str
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    pass

    @root_validator(skip_on_failure=True)
    def check_from_reserve_before_to_reserve(cls, values):
        for value in values:
            if value == "":
                raise ValueError("Нельзя менять значения на пустые")
        return values


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
