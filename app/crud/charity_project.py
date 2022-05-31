from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectDB


class CRUDCharityProject(CRUDBase):

    async def get_charity_project_by_name(
            self,
            name: str,
            session: AsyncSession,
    ) -> Optional[CharityProjectDB]:
        charity_project = await session.execute(
            select(
                CharityProject
            ).where(
                CharityProject.name == name
            )
        )
        return charity_project.scalars().first()


charity_project_crud = CRUDCharityProject(CharityProject)
