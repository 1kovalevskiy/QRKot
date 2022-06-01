from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import Column, ForeignKey, Text

from app.core.db import Base
from app.models.base import PostBase


class Donation(Base, PostBase):
    user_id = Column(GUID, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return (
            f'Создано {self.create_date.isoformat(timespec="minutes")}'
            f'Нехватает {self.full_amount - self.invested_amount}'
        )
