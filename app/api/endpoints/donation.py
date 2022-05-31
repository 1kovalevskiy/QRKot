from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.schemas.donation import DonationPartDB, DonationCreate, DonationDB
from app.schemas.user import UserDB
from app.service.invest import invest_when_new_donation

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
    response_model_exclude_none=True,
    response_model=DonationPartDB
)
async def create_donations(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: UserDB = Depends(current_user),
):
    donation = await donation_crud.create(
        obj_in=donation, session=session, user=user
    )
    await invest_when_new_donation(donation, session)
    return donation


@router.get(
    '/',
    response_model_exclude_none=True,
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    donation = await donation_crud.get_multi(session=session)
    return donation
