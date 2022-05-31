from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.schemas.donation import DonationPartDB
from app.schemas.user import UserDB

router = APIRouter()


@router.get(
    '/my',
    response_model_exclude_none=True,
    response_model=list[DonationPartDB]
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: UserDB = Depends(current_user),
):
    donation = await donation_crud.get_donation_by_user(
        session=session, user=user
    )
    return donation


@router.post(
    '/',
)
async def create_donations(
        session: AsyncSession = Depends(get_async_session),
        user: UserDB = Depends(current_user),
):
    pass


@router.get(
    '/',
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    pass
