from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt, UUID4, NonNegativeInt


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationCreate(DonationBase):
    pass


class DonationPartDB(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationPartDB):
    user_id: UUID4
    invested_amount: NonNegativeInt
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
