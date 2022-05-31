from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt, UUID4


class DonationBase(BaseModel):
    pass


class DonationCreate(BaseModel):
    pass


class DonationUpdate(BaseModel):
    pass


class DonationPartDB(BaseModel):
    id: int
    comment: str
    full_amount: PositiveInt
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(BaseModel):
    pass

    class Config:
        orm_mode = True

