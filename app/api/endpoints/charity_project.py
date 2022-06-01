from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_name_is_available,
    check_charity_project_before_delete,
    check_object_exist, check_charity_project_could_update,
    check_object_dont_close)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectDB, CharityProjectCreate, CharityProjectUpdate
)
from app.service.invest import (
    check_obj_is_fully, invest_when_new_charity_project
)

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_project(
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await charity_project_crud.get_multi(session=session)
    return charity_project


@router.post(
    '/',
    response_model_exclude_none=True,
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_charity_project_name_is_available(charity_project.name, session)
    charity_project = await charity_project_crud.create(
        charity_project, session
    )
    await invest_when_new_charity_project(charity_project, session)
    return charity_project


@router.delete(
    '/{charity_project_id}',
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_meeting_room(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_before_delete(
        charity_project_id, session
    )
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project


@router.patch(
    '/{charity_project_id}',
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_meeting_room(
        charity_project_id: int,
        update_charity_project: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await charity_project_crud.get(
        obj_id=charity_project_id, session=session
    )
    check_object_exist(charity_project, 'Такого проекта не существует')
    check_object_dont_close(charity_project)
    await check_charity_project_could_update(
        old_obj=charity_project,
        new_data=update_charity_project,
        session=session
    )
    charity_project = await charity_project_crud.update(
        db_obj=charity_project,
        obj_in=update_charity_project,
        session=session,
    )
    charity_project = await check_obj_is_fully(
        session=session, obj=charity_project
    )
    return charity_project
