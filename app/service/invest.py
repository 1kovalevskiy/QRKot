from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation
from app.schemas.charity_project import CharityProjectDB
from app.schemas.donation import DonationDB


async def check_obj_is_fully(
        session: AsyncSession,
        obj
):
    if obj.full_amount == obj.invested_amount:
        obj.fully_invested = True
        obj.close_date = datetime.now()
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


async def get_unfinished_charity_project(
        session: AsyncSession,
) -> list[CharityProjectDB]:
    charity_project = await session.execute(
        select(
            CharityProject
        ).where(
            CharityProject.fully_invested == False  # noqa
        ).order_by(
            CharityProject.create_date
        )
    )
    return charity_project.scalars().all()


async def get_unfinished_donation(
        session: AsyncSession,
) -> list[DonationDB]:
    donation = await session.execute(
        select(
            Donation
        ).where(
            Donation.fully_invested == False  # noqa
        ).order_by(
            Donation.create_date
        )
    )
    return donation.scalars().all()


async def invest_when_new_charity_project(
        cp: CharityProjectDB,
        session: AsyncSession,
) -> CharityProjectDB:
    donations = await get_unfinished_donation(session)
    for dn in donations:
        charity_delta = cp.full_amount - cp.invested_amount
        donation_delta = dn.full_amount - dn.invested_amount
        if donation_delta == charity_delta:
            dn, cp = make_investment_when_donation_equal_charity(
                dn, cp, donation_delta
            )
            session.add(dn)
            break
        elif donation_delta < charity_delta:
            dn, cp = make_investment_when_donation_less_charity(
                dn, cp, donation_delta
            )
            session.add(dn)
        else:
            dn, cp = make_investment_when_donation_more_charity(
                dn, cp, charity_delta
            )
            session.add(dn)
            break
    session.add(cp)
    await session.commit()
    await session.refresh(cp)
    return cp


async def invest_when_new_donation(
        dn: DonationDB,
        session: AsyncSession,
) -> CharityProjectDB:
    charity_projects = await get_unfinished_charity_project(session)
    for cp in charity_projects:
        charity_delta = cp.full_amount - cp.invested_amount
        donation_delta = dn.full_amount - dn.invested_amount
        if donation_delta == charity_delta:
            dn, cp = make_investment_when_donation_equal_charity(
                dn, cp, donation_delta
            )
            session.add(cp)
            break
        elif donation_delta > charity_delta:
            dn, cp = make_investment_when_donation_more_charity(
                dn, cp, charity_delta
            )
            session.add(cp)
        else:
            dn, cp = make_investment_when_donation_less_charity(
                dn, cp, donation_delta
            )
            session.add(cp)
            break
    session.add(dn)
    await session.commit()
    await session.refresh(dn)
    return dn


def make_investment_when_donation_equal_charity(
        dn: DonationDB,
        cp: CharityProjectDB,
        delta: int,
):
    cp.invested_amount += delta
    cp.fully_invested = True
    cp.close_date = datetime.now()
    dn.invested_amount += delta
    dn.fully_invested = True
    dn.close_date = datetime.now()
    return dn, cp


def make_investment_when_donation_more_charity(
        dn: DonationDB,
        cp: CharityProjectDB,
        delta: int,
):
    cp.invested_amount += delta
    cp.fully_invested = True
    cp.close_date = datetime.now()
    dn.invested_amount += delta
    return dn, cp


def make_investment_when_donation_less_charity(
        dn: DonationDB,
        cp: CharityProjectDB,
        delta: int,
):
    cp.invested_amount += delta
    dn.invested_amount += delta
    dn.fully_invested = True
    dn.close_date = datetime.now()
    return dn, cp
