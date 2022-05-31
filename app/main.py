import uvicorn
from fastapi import FastAPI

from app.api.router import main_router
from app.core.config import settings
# from app.core.init_db import create_first_superuser

app = FastAPI(title=settings.app_title, description=settings.description)
app.include_router(main_router)


# Не работает на площадке Yandex.Practicum
# @app.on_event('startup')
# async def startup():
#     await create_first_superuser()


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)