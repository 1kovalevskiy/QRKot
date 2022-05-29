from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core.db import Base


class UserTable(SQLAlchemyBaseUserTable, Base):
    pass
