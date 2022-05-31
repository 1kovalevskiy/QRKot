from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation
from app.schemas.donation import DonationPartDB
from app.schemas.user import UserDB


class CRUDDonation(CRUDBase):

    async def get_donation_by_user(
            self,
            session: AsyncSession,
            user: UserDB
    ) -> list[DonationPartDB]:
        donation = await session.execute(
            select(
                Donation
            ).where(
                Donation.user_id == user.id
            )
        )
        return donation.scalars().all()


donation_crud = CRUDDonation(Donation)
