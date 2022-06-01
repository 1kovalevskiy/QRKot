from sqlalchemy import Column, String, Text

from app.core.db import Base
from app.models.base import PostBase


class CharityProject(Base, PostBase):
    name = Column(String(100), unique=True)
    description = Column(Text)

    def __repr__(self):
        return (
            f'Создано {self.create_date.isoformat(timespec="minutes")} '
            f'Нехватает {self.full_amount - self.invested_amount}'
        )
