from datetime import datetime

from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import Column, ForeignKey, Text, Integer, Boolean, DateTime

from app.core.db import Base


class Donation(Base):
    user_id = Column(GUID, ForeignKey('user.id'))
    comment = Column(Text)
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now())
    close_date = Column(DateTime)